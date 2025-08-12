from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, date
from app.models import OrganizationType, RegistrationStatus

# Base schemas
class BaseRegistration(BaseModel):
    class Config:
        from_attributes = True

# Step 1: Aadhaar Verification Schemas
class AadhaarVerificationRequest(BaseModel):
    aadhaar_number: str = Field(..., min_length=12, max_length=12, description="12-digit Aadhaar number")
    entrepreneur_name: str = Field(..., min_length=1, max_length=255, description="Name of entrepreneur as per Aadhaar")
    consent_given: bool = Field(True, description="Consent for Aadhaar usage")

    @validator('aadhaar_number')
    def validate_aadhaar(cls, v):
        if not v.isdigit() or len(v) != 12:
            raise ValueError('Aadhaar number must be exactly 12 digits')
        return v

    @validator('entrepreneur_name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Entrepreneur name cannot be empty')
        return v.strip()

class AadhaarVerificationResponse(BaseModel):
    success: bool
    message: str
    registration_id: Optional[int] = None
    otp_sent: bool = False

# OTP Validation Schemas
class OTPValidationRequest(BaseModel):
    registration_id: int = Field(..., description="Registration ID from step 1")
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP")

    @validator('otp_code')
    def validate_otp(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError('OTP must be exactly 6 digits')
        return v

class OTPValidationResponse(BaseModel):
    success: bool
    message: str
    aadhaar_verified: bool = False

# Step 2: PAN Validation Schemas
class PANValidationRequest(BaseModel):
    registration_id: int = Field(..., description="Registration ID from step 1")
    pan_number: str = Field(..., min_length=10, max_length=10, description="10-character PAN")
    pan_name: str = Field(..., min_length=1, max_length=255, description="Name as per PAN")
    date_of_incorporation: Optional[date] = Field(None, description="Date of incorporation")
    organization_type: Optional[OrganizationType] = Field(None, description="Type of organization")

    @validator('pan_number')
    def validate_pan(cls, v):
        import re
        pan_pattern = r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$'
        if not re.match(pan_pattern, v):
            raise ValueError('PAN must be in format: ABCDE1234F')
        return v.upper()

    @validator('pan_name')
    def validate_pan_name(cls, v):
        if not v.strip():
            raise ValueError('PAN name cannot be empty')
        return v.strip()

class PANValidationResponse(BaseModel):
    success: bool
    message: str
    pan_verified: bool = False
    registration_number: Optional[str] = None

# Complete Registration Schema
class CompleteRegistrationRequest(BaseModel):
    # Step 1
    aadhaar_number: str
    entrepreneur_name: str
    consent_given: bool = True
    
    # Step 2
    pan_number: Optional[str] = None
    pan_name: Optional[str] = None
    date_of_incorporation: Optional[date] = None
    organization_type: Optional[OrganizationType] = None
    
    # Additional fields
    gstin: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_type: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: int
    aadhaar_number: str
    entrepreneur_name: str
    pan_number: Optional[str]
    status: RegistrationStatus
    registration_number: Optional[str]
    submitted_at: datetime
    aadhaar_verified: bool
    otp_verified: bool
    pan_verified: bool

    class Config:
        from_attributes = True

# Validation Response Schemas
class ValidationResponse(BaseModel):
    is_valid: bool
    message: str
    field_name: Optional[str] = None
    validation_type: Optional[str] = None

# Error Response Schema
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None

# Success Response Schema
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None 