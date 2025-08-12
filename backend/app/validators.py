import re
import requests
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import UdyamRegistration, ValidationLog, OTPLog
from app.schemas import ValidationResponse

class UdyamValidator:
    """Validator for Udyam registration form data"""
    
    def __init__(self):
        # Validation patterns extracted from scraper
        self.validation_rules = {
            "aadhaar": {
                "pattern": r"^\d{12}$",
                "description": "12-digit Aadhaar number",
                "max_length": 12
            },
            "pan": {
                "pattern": r"^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$",
                "description": "PAN format: ABCDE1234F",
                "max_length": 10
            },
            "otp": {
                "pattern": r"^\d{6}$",
                "description": "6-digit OTP",
                "max_length": 6
            },
            "gstin": {
                "pattern": r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$",
                "description": "GSTIN format: 22AAAAA0000A1Z5",
                "max_length": 15
            }
        }
    
    def validate_aadhaar(self, aadhaar_number: str) -> ValidationResponse:
        """Validate Aadhaar number"""
        if not aadhaar_number:
            return ValidationResponse(
                is_valid=False,
                message="Aadhaar number is required",
                field_name="aadhaar_number",
                validation_type="aadhaar"
            )
        
        if not re.match(self.validation_rules["aadhaar"]["pattern"], aadhaar_number):
            return ValidationResponse(
                is_valid=False,
                message="Aadhaar number must be exactly 12 digits",
                field_name="aadhaar_number",
                validation_type="aadhaar"
            )
        
        # Additional Aadhaar validation logic can be added here
        # For example, checksum validation, UIDAI API integration, etc.
        
        return ValidationResponse(
            is_valid=True,
            message="Aadhaar number is valid",
            field_name="aadhaar_number",
            validation_type="aadhaar"
        )
    
    def validate_entrepreneur_name(self, name: str) -> ValidationResponse:
        """Validate entrepreneur name"""
        if not name or not name.strip():
            return ValidationResponse(
                is_valid=False,
                message="Entrepreneur name is required",
                field_name="entrepreneur_name",
                validation_type="name"
            )
        
        if len(name.strip()) < 2:
            return ValidationResponse(
                is_valid=False,
                message="Entrepreneur name must be at least 2 characters",
                field_name="entrepreneur_name",
                validation_type="name"
            )
        
        if len(name.strip()) > 255:
            return ValidationResponse(
                is_valid=False,
                message="Entrepreneur name cannot exceed 255 characters",
                field_name="entrepreneur_name",
                validation_type="name"
            )
        
        # Check for valid characters (letters, spaces, dots)
        if not re.match(r"^[a-zA-Z\s\.]+$", name.strip()):
            return ValidationResponse(
                is_valid=False,
                message="Entrepreneur name can only contain letters, spaces, and dots",
                field_name="entrepreneur_name",
                validation_type="name"
            )
        
        return ValidationResponse(
            is_valid=True,
            message="Entrepreneur name is valid",
            field_name="entrepreneur_name",
            validation_type="name"
        )
    
    def validate_pan(self, pan_number: str) -> ValidationResponse:
        """Validate PAN number"""
        if not pan_number:
            return ValidationResponse(
                is_valid=False,
                message="PAN number is required",
                field_name="pan_number",
                validation_type="pan"
            )
        
        pan_upper = pan_number.upper()
        if not re.match(self.validation_rules["pan"]["pattern"], pan_upper):
            return ValidationResponse(
                is_valid=False,
                message="PAN must be in format: ABCDE1234F",
                field_name="pan_number",
                validation_type="pan"
            )
        
        return ValidationResponse(
            is_valid=True,
            message="PAN number is valid",
            field_name="pan_number",
            validation_type="pan"
        )
    
    def validate_otp(self, otp_code: str) -> ValidationResponse:
        """Validate OTP code"""
        if not otp_code:
            return ValidationResponse(
                is_valid=False,
                message="OTP is required",
                field_name="otp_code",
                validation_type="otp"
            )
        
        if not re.match(self.validation_rules["otp"]["pattern"], otp_code):
            return ValidationResponse(
                is_valid=False,
                message="OTP must be exactly 6 digits",
                field_name="otp_code",
                validation_type="otp"
            )
        
        return ValidationResponse(
            is_valid=True,
            message="OTP format is valid",
            field_name="otp_code",
            validation_type="otp"
        )
    
    def validate_gstin(self, gstin: str) -> ValidationResponse:
        """Validate GSTIN (optional field)"""
        if not gstin:
            return ValidationResponse(
                is_valid=True,
                message="GSTIN is optional",
                field_name="gstin",
                validation_type="gstin"
            )
        
        gstin_upper = gstin.upper()
        if not re.match(self.validation_rules["gstin"]["pattern"], gstin_upper):
            return ValidationResponse(
                is_valid=False,
                message="GSTIN must be in format: 22AAAAA0000A1Z5",
                field_name="gstin",
                validation_type="gstin"
            )
        
        return ValidationResponse(
            is_valid=True,
            message="GSTIN is valid",
            field_name="gstin",
            validation_type="gstin"
        )
    
    def check_duplicate_aadhaar(self, db: Session, aadhaar_number: str, exclude_id: Optional[int] = None) -> bool:
        """Check if Aadhaar number is already registered"""
        query = db.query(UdyamRegistration).filter(
            UdyamRegistration.aadhaar_number == aadhaar_number
        )
        
        if exclude_id:
            query = query.filter(UdyamRegistration.id != exclude_id)
        
        return query.first() is not None
    
    def check_duplicate_pan(self, db: Session, pan_number: str, exclude_id: Optional[int] = None) -> bool:
        """Check if PAN number is already registered"""
        if not pan_number:
            return False
            
        query = db.query(UdyamRegistration).filter(
            UdyamRegistration.pan_number == pan_number.upper()
        )
        
        if exclude_id:
            query = query.filter(UdyamRegistration.id != exclude_id)
        
        return query.first() is not None
    
    def validate_otp_with_database(self, db: Session, aadhaar_number: str, otp_code: str) -> Tuple[bool, str]:
        """Validate OTP against database records"""
        # Find the most recent OTP for this Aadhaar number
        otp_record = db.query(OTPLog).filter(
            OTPLog.aadhaar_number == aadhaar_number,
            OTPLog.otp_code == otp_code,
            OTPLog.is_used == False,
            OTPLog.is_expired == False,
            OTPLog.expires_at > datetime.utcnow()
        ).order_by(OTPLog.created_at.desc()).first()
        
        if not otp_record:
            return False, "Invalid or expired OTP"
        
        # Mark OTP as used
        otp_record.is_used = True
        otp_record.used_at = datetime.utcnow()
        db.commit()
        
        return True, "OTP validated successfully"
    
    def log_validation(self, db: Session, registration_id: int, field_name: str, 
                      validation_type: str, is_valid: bool, error_message: Optional[str] = None):
        """Log validation results to database"""
        validation_log = ValidationLog(
            registration_id=registration_id,
            field_name=field_name,
            validation_type=validation_type,
            is_valid=is_valid,
            error_message=error_message
        )
        db.add(validation_log)
        db.commit()
    
    def generate_otp(self) -> str:
        """Generate a 6-digit OTP"""
        import random
        return str(random.randint(100000, 999999))
    
    def create_otp_record(self, db: Session, aadhaar_number: str) -> str:
        """Create OTP record in database"""
        otp_code = self.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # OTP expires in 10 minutes
        
        otp_record = OTPLog(
            aadhaar_number=aadhaar_number,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        db.add(otp_record)
        db.commit()
        
        return otp_code

# Global validator instance
validator = UdyamValidator() 