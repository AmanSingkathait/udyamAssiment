from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import UdyamRegistration, RegistrationStatus
from app.schemas import (
    AadhaarVerificationRequest, AadhaarVerificationResponse,
    OTPValidationRequest, OTPValidationResponse,
    PANValidationRequest, PANValidationResponse,
    RegistrationResponse, ErrorResponse, SuccessResponse
)
from app.validators import validator
from datetime import datetime

router = APIRouter()

@router.post("/aadhaar-verification", response_model=AadhaarVerificationResponse)
async def verify_aadhaar(
    request_data: AadhaarVerificationRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Step 1: Verify Aadhaar number and entrepreneur name
    """
    try:
        # Validate Aadhaar number
        aadhaar_validation = validator.validate_aadhaar(request_data.aadhaar_number)
        if not aadhaar_validation.is_valid:
            raise HTTPException(status_code=400, detail=aadhaar_validation.message)
        
        # Validate entrepreneur name
        name_validation = validator.validate_entrepreneur_name(request_data.entrepreneur_name)
        if not name_validation.is_valid:
            raise HTTPException(status_code=400, detail=name_validation.message)
        
        # Check for duplicate Aadhaar
        if validator.check_duplicate_aadhaar(db, request_data.aadhaar_number):
            raise HTTPException(status_code=409, detail="Aadhaar number already registered")
        
        # Create registration record
        registration = UdyamRegistration(
            aadhaar_number=request_data.aadhaar_number,
            entrepreneur_name=request_data.entrepreneur_name,
            consent_given=request_data.consent_given,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            status=RegistrationStatus.PENDING
        )
        
        db.add(registration)
        db.commit()
        db.refresh(registration)
        
        # Log validation
        validator.log_validation(db, registration.id, "aadhaar_number", "aadhaar", True)
        validator.log_validation(db, registration.id, "entrepreneur_name", "name", True)
        
        # Generate and store OTP
        otp_code = validator.create_otp_record(db, request_data.aadhaar_number)
        
        # In a real application, you would send OTP via SMS/email here
        # For demo purposes, we'll return the OTP in response
        print(f"OTP for {request_data.aadhaar_number}: {otp_code}")
        
        return AadhaarVerificationResponse(
            success=True,
            message="Aadhaar verification successful. OTP sent to registered mobile number.",
            registration_id=registration.id,
            otp_sent=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/otp-validation", response_model=OTPValidationResponse)
async def validate_otp(
    request_data: OTPValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Step 2: Validate OTP for Aadhaar verification
    """
    try:
        # Get registration record
        registration = db.query(UdyamRegistration).filter(
            UdyamRegistration.id == request_data.registration_id
        ).first()
        
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")
        
        # Validate OTP format
        otp_validation = validator.validate_otp(request_data.otp_code)
        if not otp_validation.is_valid:
            raise HTTPException(status_code=400, detail=otp_validation.message)
        
        # Validate OTP against database
        is_valid, message = validator.validate_otp_with_database(
            db, registration.aadhaar_number, request_data.otp_code
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Update registration
        registration.otp_verified = True
        registration.aadhaar_verified = True
        db.commit()
        
        # Log validation
        validator.log_validation(db, registration.id, "otp_code", "otp", True)
        
        return OTPValidationResponse(
            success=True,
            message="OTP validated successfully. Aadhaar verification completed.",
            aadhaar_verified=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/pan-validation", response_model=PANValidationResponse)
async def validate_pan(
    request_data: PANValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Step 3: Validate PAN details
    """
    try:
        # Get registration record
        registration = db.query(UdyamRegistration).filter(
            UdyamRegistration.id == request_data.registration_id
        ).first()
        
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")
        
        if not registration.aadhaar_verified:
            raise HTTPException(status_code=400, detail="Aadhaar must be verified before PAN validation")
        
        # Validate PAN number
        pan_validation = validator.validate_pan(request_data.pan_number)
        if not pan_validation.is_valid:
            raise HTTPException(status_code=400, detail=pan_validation.message)
        
        # Validate PAN name
        name_validation = validator.validate_entrepreneur_name(request_data.pan_name)
        if not name_validation.is_valid:
            raise HTTPException(status_code=400, detail=name_validation.message)
        
        # Check for duplicate PAN
        if validator.check_duplicate_pan(db, request_data.pan_number, registration.id):
            raise HTTPException(status_code=409, detail="PAN number already registered")
        
        # Update registration
        registration.pan_number = request_data.pan_number.upper()
        registration.pan_name = request_data.pan_name
        registration.date_of_incorporation = request_data.date_of_incorporation
        registration.organization_type = request_data.organization_type
        registration.pan_verified = True
        registration.status = RegistrationStatus.VERIFIED
        
        # Generate registration number
        registration.registration_number = f"UDYAM-{registration.id:06d}-{datetime.now().year}"
        
        db.commit()
        
        # Log validation
        validator.log_validation(db, registration.id, "pan_number", "pan", True)
        validator.log_validation(db, registration.id, "pan_name", "name", True)
        
        return PANValidationResponse(
            success=True,
            message="PAN validation successful. Registration completed.",
            pan_verified=True,
            registration_number=registration.registration_number
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/registration/{registration_id}", response_model=RegistrationResponse)
async def get_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):
    """
    Get registration details by ID
    """
    registration = db.query(UdyamRegistration).filter(
        UdyamRegistration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    return registration

@router.get("/registrations", response_model=List[RegistrationResponse])
async def get_registrations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all registrations with pagination
    """
    registrations = db.query(UdyamRegistration).offset(skip).limit(limit).all()
    return registrations

@router.get("/health", response_model=SuccessResponse)
async def health_check():
    """
    Health check endpoint
    """
    return SuccessResponse(
        success=True,
        message="Udyam Registration API is running",
        data={"status": "healthy", "timestamp": datetime.now().isoformat()}
    ) 