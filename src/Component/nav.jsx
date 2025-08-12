import React, { useState, useRef, useEffect } from 'react'
import logo from '../Image/MINISTRY_NAME.webp'

const Nav = () => {
    const [activeDropdown, setActiveDropdown] = useState(null);
    const [dropdownPosition, setDropdownPosition] = useState({});
    const dropdownRefs = useRef({});

    const handleDropdownToggle = (dropdownName) => {
        setActiveDropdown(activeDropdown === dropdownName ? null : dropdownName);
    };

    const handleMouseLeave = () => {
        setActiveDropdown(null);
    };

    const handleDropdownEnter = (dropdownName) => {
        setActiveDropdown(dropdownName);
        
        // Check if dropdown would overflow the right edge
        setTimeout(() => {
            const dropdownElement = dropdownRefs.current[dropdownName];
            if (dropdownElement) {
                const rect = dropdownElement.getBoundingClientRect();
                const windowWidth = window.innerWidth;
                const wouldOverflow = rect.right > windowWidth;
                
                setDropdownPosition(prev => ({
                    ...prev,
                    [dropdownName]: wouldOverflow ? 'left' : 'right'
                }));
            }
        }, 0);
    };

    return (
        <div className='navbar'>
            <div className='navbar-logo'>
                <img src={logo} alt='National Emblem' />
            </div>
            <div className='navbar-menu'>
                <a href="#" className='nav-link active'>Home</a>
                
                <a href="#" className='nav-link'>NIC Code</a>
                
                <div className='nav-dropdown' onMouseLeave={handleMouseLeave}>
                    <a 
                        href="#" 
                        className='nav-link dropdown-toggle active'
                        onClick={() => handleDropdownToggle('useful')}
                        onMouseEnter={() => handleDropdownEnter('useful')}
                    >
                        Useful Documents
                        <span className='dropdown-arrow'>▼</span>
                    </a>
                    {activeDropdown === 'useful' && (
                        <div 
                            ref={el => dropdownRefs.current['useful'] = el}
                            className={`dropdown-menu ${dropdownPosition['useful'] === 'left' ? 'dropdown-left' : ''}`}
                        >
                            <a href="#" className='dropdown-item'>Important</a>
                            <a href="#" className='dropdown-item'>
                                Udyam Registration Benefits
                                <span className='new-tag'>NEW</span>
                            </a>
                            <a href="#" className='dropdown-item'>Site Highlights</a>
                            <a href="#" className='dropdown-item'>Circulars & Orders</a>
                            <a href="#" className='dropdown-item'>Udyam Registration Sample form</a>
                            <a href="#" className='dropdown-item'>
                                Udyam Registration Bulletin
                                <span className='new-tag'>NEW</span>
                                <span className='chevron-left'>&lt;</span>
                            </a>
                            <a href="#" className='dropdown-item'>Metadata Compliance</a>
                        </div>
                    )}
                </div>
                
                <div className='nav-dropdown' onMouseLeave={handleMouseLeave}>
                    <a 
                        href="#" 
                        className='nav-link dropdown-toggle'
                        onClick={() => handleDropdownToggle('print')}
                        onMouseEnter={() => handleDropdownEnter('print')}
                    >
                        Print / Verify
                        <span className='dropdown-arrow'>▼</span>
                    </a>
                    {activeDropdown === 'print' && (
                        <div 
                            ref={el => dropdownRefs.current['print'] = el}
                            className={`dropdown-menu ${dropdownPosition['print'] === 'left' ? 'dropdown-left' : ''}`}
                        >
                            <a href="#" className='dropdown-item'>Print Certificate</a>
                            <a href="#" className='dropdown-item'>Verify Udyam</a>
                            <a href="#" className='dropdown-item'>Download</a>
                        </div>
                    )}
                </div>
                
                <div className='nav-dropdown' onMouseLeave={handleMouseLeave}>
                    <a 
                        href="#" 
                        className='nav-link dropdown-toggle'
                        onClick={() => handleDropdownToggle('update')}
                        onMouseEnter={() => handleDropdownEnter('update')}
                    >
                        Update Details
                        <span className='dropdown-arrow'>▼</span>
                    </a>
                    {activeDropdown === 'update' && (
                        <div 
                            ref={el => dropdownRefs.current['update'] = el}
                            className={`dropdown-menu ${dropdownPosition['update'] === 'left' ? 'dropdown-left' : ''}`}
                        >
                            <a href="#" className='dropdown-item'>Update Profile</a>
                            <a href="#" className='dropdown-item'>Change Address</a>
                            <a href="#" className='dropdown-item'>Update Contact</a>
                        </div>
                    )}
                </div>
                
                <div className='nav-dropdown' onMouseLeave={handleMouseLeave}>
                    <a 
                        href="#" 
                        className='nav-link dropdown-toggle'
                        onClick={() => handleDropdownToggle('login')}
                        onMouseEnter={() => handleDropdownEnter('login')}
                    >
                        Login
                        <span className='dropdown-arrow'>▼</span>
                    </a>
                    {activeDropdown === 'login' && (
                        <div 
                            ref={el => dropdownRefs.current['login'] = el}
                            className={`dropdown-menu ${dropdownPosition['login'] === 'left' ? 'dropdown-left' : ''}`}
                        >
                            <a href="#" className='dropdown-item'>Officer's Login</a>
                            <a href="#" className='dropdown-item'>
                                EFC's Login
                                <span className='new-tag yellow'>NEW</span>
                            </a>
                            <a href="#" className='dropdown-item'>
                                NSSH Officer's Login
                                <span className='new-tag yellow'>NEW</span>
                            </a>
                            <a href="#" className='dropdown-item'>Udyami Login</a>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Nav
