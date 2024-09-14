import { useState } from 'react';
import './Navbar.css';
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
                    <li><a href="/home/#">Home</a></li>
                    <li><a href="/home/#">Events</a></li>
                    <li><a href="/home/#">About</a></li>
                    <li><a href="/home/#">Profile</a></li>
                </ul>
            </nav>
        </div>
    );
};
export default Navbar;
