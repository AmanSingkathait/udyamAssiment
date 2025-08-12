from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class OrganizationType(str, enum.Enum):
    PROPRIETORSHIP = "proprietorship"
    PARTNERSHIP = "partnership"
    PRIVATE_LIMITED = "private-limited"
    PUBLIC_LIMITED = "public-limited"
    LLP = "llp"
    HUF = "huf"
    COOPERATIVE = "cooperative"
    TRUST = "trust"

class RegistrationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    COMPLETED = "completed"

class UdyamRegistration(Base):
    __tablename__ = "udyam_registrations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Step 1: Aadhaar Verification
    aadhaar_number = Column(String(12), nullable=False, index=True)
    entrepreneur_name = Column(String(255), nullable=False)
    aadhaar_verified = Column(Boolean, default=False)
    otp_verified = Column(Boolean, default=False)
    
    # Step 2: PAN Validation
    pan_number = Column(String(10), nullable=True, index=True)
    pan_name = Column(String(255), nullable=True)
    date_of_incorporation = Column(DateTime, nullable=True)
    organization_type = Column(Enum(OrganizationType), nullable=True)
    pan_verified = Column(Boolean, default=False)
    
    # Additional Information
    gstin = Column(String(15), nullable=True)
    business_name = Column(String(255), nullable=True)
    business_address = Column(Text, nullable=True)
    business_type = Column(String(100), nullable=True)
    
    # Registration Details
    registration_number = Column(String(50), nullable=True, unique=True, index=True)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Audit Fields
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    consent_given = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<UdyamRegistration(id={self.id}, aadhaar={self.aadhaar_number}, status={self.status})>"

class ValidationLog(Base):
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    validation_type = Column(String(50), nullable=False)  # aadhaar, pan, otp, etc.
    is_valid = Column(Boolean, nullable=False)
    error_message = Column(Text, nullable=True)
    validated_at = Column(DateTime(timezone=True), server_default=func.now())

class OTPLog(Base):
    __tablename__ = "otp_logs"

    id = Column(Integer, primary_key=True, index=True)
    aadhaar_number = Column(String(12), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    is_expired = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True) 