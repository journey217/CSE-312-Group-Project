import React, {useEffect, useState} from "react";
import { Link, useNavigate } from 'react-router-dom';
import "../styles/login.css";

export default function Login(page) {

    const navigate = useNavigate();

    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");

    const handleSubmission = (e) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({'email': email, 'password': password})
        };
        fetch('/login-user', requestOptions)
            .then(response => response.json())
            .then(response => console.log(response))
        console.log("a")
    }
    return (
        <div className="login">
            <ul>
                <header className="header">JBAY</header>
                <div className="login-form">
                    <form className="login-inputs" onSubmit={handleSubmission}>
                        <header className="formheader">Login</header>
                        <label htmlFor="email"></label>
                        <input type="email" placeholder="Email" name="email" value={email} onChange={(e) => {setEmail(e.target.value)}} required/>
                        <label htmlFor="password"></label>
                        <input type="password" placeholder="Password" name="password" value={password} onChange={(e) => {setPassword(e.target.value)}} required />
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