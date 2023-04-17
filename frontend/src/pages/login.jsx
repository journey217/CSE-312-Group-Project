import React from "react";
import { Link } from 'react-router-dom';
import "../styles/login.css";

export default function Login(page) {

    const handleSubmission = (e) => {

    }
    return (
        <div className="login">
            <ul>

                <header className="header">JBAY</header>
                <div className="login-form">
                    <form className="login-inputs" onSubmit={() => { window.location.href = "/login-user"; }}>
                        <header className="formheader">Login</header>
                        <label htmlFor="email"></label>
                        <input type="email" placeholder="Email" name="email" />
                        <label htmlFor="password"></label>
                        <input type="password" placeholder="Password" name="password" required />
                        <button className="login-button" type={"submit"} onClick={() => { window.location.href = "/login-user"; }}>Login</button>
                    </form>
                    <button className="forgot-button" onClick={() => { window.location.href = "/forgot"; }}>
                        Forgot Password
                    </button>
                    <button className="signup-button" onClick={() => { window.location.href = "/registration"; }}>
                        Sign Up
                    </button>
                </div>
            </ul>
        </div>
    );
}