import React from "react";
import { Link, useNavigate } from 'react-router-dom';
import "../styles/registration.css";

export default function Registration(page) {
    const navigate = useNavigate()
    return (
        <div className='register'>
            <ul>
                <header className="header">JBAY</header>
                <div className="register-form">
                    <form className="reg-inputs" action= "/register-user" method="post">
                        <header className="formheader">Create New Account</header>\
                        <input type="text" placeholder='Username' name='username' required />
                        <input type="email" placeholder="Email" name="email" required />
                        <input type="password" placeholder="Password" name="password1" required />
                        <input type="password" placeholder="Confirm Password" name="password2" required />
                        <button className="register-button" type="submit" >Register</button>
                    </form>
                    <button className="login-redirect-button" onClick={() => {navigate("/login")}}>
                        Have An Account? Click Here
                    </button>
                    
                </div>
            </ul>
        </div>
    );
}