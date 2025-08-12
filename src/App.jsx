import React, { useState } from 'react'
import Nav from './Component/nav'
import Footer from './Component/footer'
import './App.css'

function App() {
  const [aadhaarNumber, setAadhaarNumber] = useState('');
  const [entrepreneurName, setEntrepreneurName] = useState('');
  const [showOtpSection, setShowOtpSection] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [showErrors, setShowErrors] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);

  // Form validation patterns
  const aadhaarPattern = /^\d{12}$/;
  const otpPattern = /^\d{6}$/;

  // Validation functions
  const validateAadhaar = (value) => aadhaarPattern.test(value);
  const validateOTP = (value) => otpPattern.test(value);

  const handleValidateAndGenerateOTP = () => {
    setHasInteracted(true);
    if (aadhaarNumber.trim() && entrepreneurName.trim() && validateAadhaar(aadhaarNumber)) {
      setIsValidating(true);
      setShowErrors(false);
      // Simulate API call
      setTimeout(() => {
        setShowOtpSection(true);
        setIsValidating(false);
      }, 1000);
    } else {
      setShowErrors(true);
    }
  };

  // Clear errors when user starts typing
  const handleAadhaarChange = (e) => {
    setAadhaarNumber(e.target.value);
    setHasInteracted(true);
    if (showErrors) {
      setShowErrors(false);
    }
  };

  const handleEntrepreneurNameChange = (e) => {
    setEntrepreneurName(e.target.value);
    setHasInteracted(true);
    if (showErrors) {
      setShowErrors(false);
    }
  };

  const handleOtpChange = (e) => {
    setOtpCode(e.target.value);
    setHasInteracted(true);
    if (showErrors) {
      setShowErrors(false);
    }
  };

  const handleValidateOTP = () => {
    setHasInteracted(true);
    if (otpCode.trim() && validateOTP(otpCode)) {
      // Handle OTP validation
      console.log('Validating OTP:', otpCode);
      setTimeout(() => {
        alert('Aadhaar verification completed successfully!');
        setShowOtpSection(false);
        setOtpCode('');
      }, 1000);
    } else {
      setShowErrors(true);
    }
  };

  return (
    <div className="App">
      <Nav />
      <div className="content">
        <div className="form-container">
          <div className="heading">
            <h1 className="form-title">Aadhaar Verification With OTP</h1>
          </div>

          <div className="aadhaar-section">
            <div className="form-fields">
              <div className="field-group">
                <label htmlFor="aadhaar">1. Aadhaar Number / आधार संख्या</label>
                <input
                  type="text"
                  id="aadhaar"
                  placeholder="Your Aadhaar No"
                  className={`form-input ${showErrors && (!aadhaarNumber.trim() || !validateAadhaar(aadhaarNumber)) ? 'error' : ''}`}
                  value={aadhaarNumber}
                  onChange={handleAadhaarChange}
                  maxLength={12}
                />
                {showErrors && !aadhaarNumber.trim() && (
                  <span className="error-text">*Required</span>
                )}
                {showErrors && aadhaarNumber.trim() && !validateAadhaar(aadhaarNumber) && (
                  <span className="error-text">*Please enter a valid 12-digit Aadhaar number</span>
                )}
              </div>

              <div className="field-group">
                <label htmlFor="entrepreneur">2. Name of Entrepreneur / उद्यमी का नाम</label>
                <input
                  type="text"
                  id="entrepreneur"
                  placeholder="Name as per Aadhaar"
                  className={`form-input ${showErrors && !entrepreneurName.trim() ? 'error' : ''}`}
                  value={entrepreneurName}
                  onChange={handleEntrepreneurNameChange}
                />
                {showErrors && !entrepreneurName.trim() && (
                  <span className="error-text">*Required</span>
                )}
              </div>
            </div>

            <div className="instructions">
              <ul>
                <li>Aadhaar number shall be required for Udyam Registration.</li>
                <li>The Aadhaar number shall be of the proprietor in the case of a proprietorship firm, of the managing partner in the case of a partnership firm and of a karta in the case of a Hindu Undivided Family (HUF).</li>
                <li>In case of a Company or a Limited Liability Partnership or a Cooperative Society or a Society or a Trust, the organisation or its authorised signatory shall provide its GSTIN(As per applicablity of CGST Act 2017 and as notified by the ministry of MSME <a href="#" className="link">vide S.O. 1055(E) dated 05th March 2021</a>) and PAN along with its Aadhaar number.</li>
              </ul>
            </div>

            <div className="consent-section">
              <label className="consent-checkbox">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                <span className="consent-text">
                  I, the holder of the above Aadhaar, hereby give my consent to Ministry of MSME, Government of India, for using my Aadhaar number as alloted by UIDAI for Udyam Registration. NIC / Ministry of MSME, Government of India, have informed me that my aadhaar data will not be stored/shared.
                  <br />
                  मैं, आधार धारक, इस प्रकार उद्यम पंजीकरण के लिए यूआईडीएआई के साथ अपने आधार संख्या का उपयोग करने के लिए सू०ल०म० उ० मंत्रालय, भारत सरकार को अपनी सहमति देता हूं। एनआईसी / सू०ल०म० उ० मंत्रालय, भारत सरकार ने मुझे सूचित किया है कि मेरा आधार डेटा संग्रहीत / साझा नहीं किया जाएगा।
                </span>
              </label>
            </div>

            {/* Show either the original button or the OTP section */}
            {!showOtpSection ? (
              <div className="button-section">
                <button
                  className="validate-button"
                  onClick={handleValidateAndGenerateOTP}
                  disabled={isValidating}
                >
                  {isValidating ? 'Validating...' : 'Validate & Generate OTP'}
                </button>
              </div>
            ) : (
              <div className="otp-section">
                <h3 className="otp-title">
                  <span className="required">*</span>Enter One Time Password(OTP) Code
                </h3>
                <div className="otp-input-group">
                  <input
                    type="text"
                    placeholder="Enter 6-digit OTP"
                    className={`otp-input ${showErrors && (!otpCode.trim() || !validateOTP(otpCode)) ? 'error' : ''}`}
                    value={otpCode}
                    onChange={handleOtpChange}
                    maxLength={6}
                  />
                  <p className="otp-message">OTP has been sent to ******0176</p>
                  {showErrors && !otpCode.trim() && (
                    <span className="error-text">*OTP is required</span>
                  )}
                  {showErrors && otpCode.trim() && !validateOTP(otpCode) && (
                    <span className="error-text">*Please enter a valid 6-digit OTP</span>
                  )}
                </div>
                <div className="otp-button-section">
                  <button
                    className="validate-otp-button"
                    onClick={handleValidateOTP}
                    disabled={!otpCode.trim()}
                  >
                    Validate OTP
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="footer-text">
            <div className="scrolling-text">
              Activities (NIC codes) not covered under MSMED Act, 2006 for Udyam Registration
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default App
