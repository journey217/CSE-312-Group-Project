import React from "react";
import {Link} from 'react-router-dom';
import "../styles/login.css";

export default function Login(page) {

    const handleSubmission = (e) =>{
        
    }
    return (
        <div class="login">
            <ul>
                <header class="header">JESSBAY</header>
                <div class="login-form">
                    <form class="login-inputs" onSubmit={handleSubmission}>
                        <label for="email"></label>
                        <input type="email" placeholder="Email" name="email" />
                        <label for="password"></label>
                        <input type="password" placeholder="Password" name="password" required />
                        <button>Login</button>
                    </form>
                    <button class="forgot-button">
                        <Link to="/forgot">Forgot Password</Link>
                    </button>
                    <button class="signup-button">
                        <Link to="/registration">Sign Up</Link>
                    </button>
                </div>
            </ul>
        </div>
    );
}