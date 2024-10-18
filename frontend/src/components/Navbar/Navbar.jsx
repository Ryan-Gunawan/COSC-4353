import { useState } from 'react';
import './Navbar.css';
import NotificationBell from '../NotificationBell/NotificationBell';
import logo from '../Assets/handslogo.jpg'

const Navbar = () => {
    const [isActive, setIsActive] = useState(false);

    const handleHamburgerClick = () => {
        setIsActive(!isActive);
    };

    return (
        <div className="nav-container">
            <div className="logo">
                <a href="/home">
                    <img src={logo} alt="logo" />
                    VolunteerMatcher
                </a>
            </div>
            <div className="hamburger" onClick={handleHamburgerClick}>
                <div className="line"></div>
                <div className="line"></div>
                <div className="line"></div>
            </div>
            <nav className={`navbar ${isActive ? 'active' : ''}`}>
                <ul>
                    <li><a href="/home">Home</a></li>
                    <li><a href="/eventlist">Events</a></li>
                    <li><a href="/eventmatch">Find Volunteers</a></li>
                    <li><a href="/volunteerhistory">History</a></li>
                    <li><a href="/userprofile">Profile</a></li>
                    <li><a href="/">Sign Up</a></li>
                    <li><a href="/notifications"><NotificationBell /></a></li>
                </ul>
            </nav>
        </div >
    );
};
export default Navbar;
