#!/usr/bin/env python3
"""
Simple test script for the Udyam Registration API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/registration/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_aadhaar_verification():
    """Test Aadhaar verification"""
    print("🔍 Testing Aadhaar verification...")
    
    data = {
        "aadhaar_number": "123456789012",
        "entrepreneur_name": "John Doe",
        "consent_given": True
    }
    
    response = requests.post(f"{BASE_URL}/registration/aadhaar-verification", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json().get("registration_id")
    return None

def test_otp_validation(registration_id):
    """Test OTP validation"""
    print("🔍 Testing OTP validation...")
    
    # Note: In a real scenario, you would get the OTP from SMS/email
    # For testing, we'll use a dummy OTP (you need to check the console output for the actual OTP)
    data = {
        "registration_id": registration_id,
        "otp_code": "123456"  # Replace with actual OTP from console
    }
    
    response = requests.post(f"{BASE_URL}/registration/otp-validation", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_pan_validation(registration_id):
    """Test PAN validation"""
    print("🔍 Testing PAN validation...")
    
    data = {
        "registration_id": registration_id,
        "pan_number": "ABCDE1234F",
        "pan_name": "John Doe",
        "date_of_incorporation": "2023-01-01",
        "organization_type": "proprietorship"
    }
    
    response = requests.post(f"{BASE_URL}/registration/pan-validation", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_registration(registration_id):
    """Test getting registration details"""
    print("🔍 Testing get registration...")
    
    response = requests.get(f"{BASE_URL}/registration/registration/{registration_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_validation_errors():
    """Test validation error handling"""
    print("🔍 Testing validation errors...")
    
    # Test invalid Aadhaar
    data = {
        "aadhaar_number": "123",  # Too short
        "entrepreneur_name": "John Doe",
        "consent_given": True
    }
    
    response = requests.post(f"{BASE_URL}/registration/aadhaar-verification", json=data)
    print(f"Invalid Aadhaar - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting Udyam Registration API Tests")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test validation errors
    test_validation_errors()
    
    # Test complete flow
    print("🔄 Testing complete registration flow...")
    registration_id = test_aadhaar_verification()
    
    if registration_id:
        print(f"✅ Registration created with ID: {registration_id}")
        print("⚠️  Check the console output for the OTP code!")
        print("⚠️  Update the OTP in test_otp_validation() function")
        
        # Uncomment these lines after updating the OTP
        # test_otp_validation(registration_id)
        # test_pan_validation(registration_id)
        # test_get_registration(registration_id)
    else:
        print("❌ Failed to create registration")
    
    print("=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main() 