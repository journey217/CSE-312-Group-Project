import React from "react";
import {Link} from 'react-router-dom';
import "../styles/login.css";

export default function Login(page) {

    const handleSubmission = (e) =>{
        
    }
    return (
        <div className="login">
            <ul>
                <header className="header">PRODUCT NAME</header>
                <div className="login-form">
                    <form className="login-inputs" onSubmit={handleSubmission}>
                        <label htmlFor="email"></label>
                        <input type="email" placeholder="Email" name="email" />
                        <label htmlFor="password"></label>
                        <input type="password" placeholder="Password" name="password" required />
                        <button>Login</button>
                    </form>
                    <button className="forgot-button">
                        <Link to="/forgot">Forgot Password</Link>
                    </button>
                    <button className="signup-button">
                        <Link to="/register">Sign Up</Link>
                    </button>
                </div>
            </ul>
        </div>
    );
}