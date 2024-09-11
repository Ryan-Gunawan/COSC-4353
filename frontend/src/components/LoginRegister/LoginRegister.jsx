import React, { useState } from 'react';
import './LoginRegister.css';
import { FaLock, FaEnvelope } from "react-icons/fa";

const LoginRegister = () => {

    const [action, setAction] = useState('');

    const registerLink = () => {
        setAction(' register');
    }

    const loginLink = () => {
        setAction(' login');
    }

    return (
        <div className={`container${action}`}>
            <div className="form-box login">
                <form action="">
                    <h1>Login</h1>
                    <div className="input-box">
                        <input type="email" maxLength="254" placeholder="Email" required />
                        <FaEnvelope className="icon" />
                    </div>
                    <div className="input-box">
                        <input type="password" maxLength="128" placeholder="Password" required />
                        <FaLock className="icon" />
                    </div>

                    <button type="submit">Log in</button>

                    <div className="register-link">
                        <p>Don&apos;t have an account? <a href="#" onClick={registerLink} className="signup">Register</a></p>
                    </div>
                </form>
            </div>

            <div className="form-box register">
                <form action="">
                    <h1>Register</h1>
                    <div className="input-box">
                        <input type="email" maxLength="254" placeholder="Email" required />
                        <FaEnvelope className="icon" />
                    </div>
                    <div className="input-box">
                        <input type="password" maxLength="128" placeholder="Password" required />
                        <FaLock className="icon" />
                    </div>

                    <div className="terms">
                        <p>By signing up, you agree to our Terms.</p>
                    </div>

                    <button type="submit">Register</button>

                    <div className="register-link">
                        <p>Already have an account? <a href="#" onClick={loginLink} className="signup">Log In</a></p>
                    </div>
                </form>
            </div>
        </div>
    );
};
export default LoginRegister;
