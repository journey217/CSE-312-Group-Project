import React, {useEffect, useState} from "react";
import { Link } from 'react-router-dom';
import "../styles/registration.css";

export default function Registration(page) {

    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");

    const handleSubmission = (e) => {}

    return (
        <div className='register'>
            <ul>
                <header className="header">JBAY</header>
                <div className="register-form">
                    <form className="reg-inputs" onSubmit={handleSubmission}>
                        <header className="formheader">Create New Account</header>
                        <input type="name" placeholder='First Name' name='name' required />
                        <input type="name" placeholder='Last Name' name='name' required />
                        <input type="date" placeholder='Date of Birth' name='name' required />
                        <input type="email" placeholder="Email" name="email" required />
                        <input type="password" placeholder="Password" name="password" required />
                        <input type="password" placeholder="Confirm Password" name="password" required />
                        <button className="register-button">Register</button>
                    </form>
                    <button className="create-account-button" onClick={() => { window.location.href = "/login"; }}>
                        Have An Account? Click Here
                    </button>
                    
                </div>
            </ul>
        </div>
    );
}