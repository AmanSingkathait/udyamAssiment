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

  const handleValidateAndGenerateOTP = () => {
    if (aadhaarNumber.trim() && entrepreneurName.trim()) {
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

  const handleValidateOTP = () => {
    if (otpCode.trim()) {
      // Handle OTP validation
      console.log('Validating OTP:', otpCode);
    }
  };

  const isFormValid = aadhaarNumber.trim() && entrepreneurName.trim();

  return (
    <div className="App">
      <Nav />
      <div className="content">
        <div className="form-container">
          <div className="heading">
            <h1 className="form-title">UDYAM REGISTRATION FORM - For New Enterprise who are not Registered yet as MSME</h1>
          </div>

          <div className="aadhaar-section">
            <div className="aadhaar-banner">
              <h2>Aadhaar Verification With OTP</h2>
            </div>
            
            <div className="form-fields">
              <div className="field-group">
                <label htmlFor="aadhaar">1. Aadhaar Number / आधार संख्या</label>
                <input 
                  type="text" 
                  id="aadhaar" 
                  placeholder="Your Aadhaar No"
                  className="form-input"
                  value={aadhaarNumber}
                  onChange={(e) => setAadhaarNumber(e.target.value)}
                />
                {showErrors && !aadhaarNumber.trim() && (
                  <span className="error-text">*Required</span>
                )}
              </div>
              
              <div className="field-group">
                <label htmlFor="entrepreneur">2. Name of Entrepreneur / उद्यमी का नाम</label>
                <input 
                  type="text" 
                  id="entrepreneur" 
                  placeholder="Name as per Aadhaar"
                  className="form-input"
                  value={entrepreneurName}
                  onChange={(e) => setEntrepreneurName(e.target.value)}
                />
                {showErrors && !entrepreneurName.trim() && (
                  <span className="error-text">*Required</span>
                )}
              </div>
            </div>
            
            <div className="instructions">
              <h3>Important Information:</h3>
              <ul>
                <li>The Aadhaar number shall be of the proprietor in the case of a proprietorship firm, of the managing partner in the case of a partnership firm and of a karta in the case of a Hindu Undivided Family (HUF).</li>
                <li>In case of a Company or a Limited Liability Partnership or a Cooperative Society or a Society or a Trust, the organisation or its authorised signatory shall provide its GSTIN(As per applicablity of CGST Act 2017 and as notified by the ministry of MSME vide S.O. 1055(E) dated 05th March 2021) and PAN along with its Aadhaar number.</li>
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
                    placeholder="OTP code"
                    className="otp-input"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value)}
                    maxLength={6}
                  />
                  <p className="otp-message">OTP has been sent to ******0176</p>
                </div>
                <div className="otp-button-section">
                  <button 
                    className="validate-otp-button"
                    onClick={handleValidateOTP}
                    disabled={!otpCode.trim()}
                  >
                    Validate
                  </button>
                </div>
              </div>
            )}
            
            <div className="footer-text">
              <div className="scrolling-text">
                Activities (NIC codes) not covered under MSMED Act, 2006 for Udyam Registration
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default App
