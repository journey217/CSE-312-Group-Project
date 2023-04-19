import React, {useEffect, useState} from "react";
import { Link, useNavigate } from 'react-router-dom';
import "../styles/login.css";

export default function Login(page) {

    const navigate = useNavigate();

    return (
        <div className="login">
            <ul>
                <header className="header">JBAY</header>
                <div className="login-form">
                    <form className="login-inputs" action="/login-user" method="post">
                        <header className="formheader">Login</header>
                        <label htmlFor="email"></label>
                        <input type="email" placeholder="Email" name="email" required/>
                        <label htmlFor="password"></label>
                        <input type="password" placeholder="Password" name="password" required />
                        <button className="login-button" type="submit">Login</button>
                    </form>
                    <button className="forgot-button" onClick={() => { navigate("/forgot"); }}>
                        Forgot Password
                    </button>
                    <button className="signup-button" onClick={() => { navigate("/registration"); }}>
                        Sign Up
                    </button>
                </div>
            </ul>
        </div>
    );
}