import React from 'react'

const Footer = () => {
    return (
        <footer className="footer">
            {/* Main Footer Content */}
            <div className="footer-main">
                <div className="footer-container">
                    {/* Left Column - UDYAM REGISTRATION */}
                    <div className="footer-column">
                        <h3 className="footer-title">UDYAM REGISTRATION</h3>
                        <div className="contact-info">
                            <p>Ministry of MSME</p>
                            <p>Udyog bhawan - New Delhi</p>
                            <p>Email: <a href="mailto:champions@gov.in">champions@gov.in</a></p>
                        </div>
                        <div className="contact-links">
                            <p><strong>Contact Us</strong></p>
                            <p><strong>For Grievances / Problems</strong></p>
                        </div>
                    </div>

                    {/* Middle Column - Our Services */}
                    <div className="footer-column">
                        <h3 className="footer-title">Our Services</h3>
                        <ul className="services-list">
                            <li><a href="#">CHAMPIONS</a></li>
                            <li><a href="#">MSME Samadhaan</a></li>
                            <li><a href="#">MSME Sambandh</a></li>
                            <li><a href="#">MSME Dashboard</a></li>
                            <li><a href="#">Entrepreneurship Skill Development Programme (ESDP)</a></li>
                        </ul>
                    </div>

                    {/* Right Column - Video */}
                    <div className="footer-column">
                        <h3 className="footer-title">Video</h3>
                        <div className="video-container">
                            <div className="video-player">
                                <div className="video-thumbnail">
                                    <div className="video-content">
                                        <div className="video-title">Udyam Registration</div>
                                        <div className="video-url">www.udyamregistration.gov.in</div>
                                    </div>
                                </div>
                                <div className="video-controls">
                                    <div className="control-bar">
                                        <button className="play-btn">▶</button>
                                        <span className="time">0:00</span>
                                        <div className="progress-bar">
                                            <div className="progress-fill"></div>
                                            <div className="progress-scrubber"></div>
                                        </div>
                                        <span className="duration">0:47</span>
                                        <button className="volume-btn">🔊</button>
                                        <button className="fullscreen-btn">⛶</button>
                                        <button className="menu-btn">⋯</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Copyright Section */}
            <div className="footer-bottom">
                <div style={{display:"flex", alignItems:"center",width:"100%",justifyContent:"center"}}>
                    <div className="copyright-text">
                        <p>© Copyright <strong>Udyam Registration</strong>. All Rights Reserved, Website Content Managed by Ministry of Micro Small and Medium Enterprises, GoI</p>
                        <p>Website hosted & managed by <a href="#">National Informatics Centre</a>, <a href="#">Ministry of Communications and IT, Government of India</a></p>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer 