import React from "react";
import { Link } from 'react-router-dom';
import "../styles/login.css";

export default function Registration(page) {

    const handleSubmission = (e) => {

    }

    return (
        < div class='register' >
            <ul>
                <header class="header">JESSBAY</header>
                <div class="register-form">
                    <form class="reg-inputs" onSubmit={handleSubmission}>
                        <header class="formheader">Create New Account</header>
                        <input type="name" placeholder='First Name' name='name' required />
                        <input type="name" placeholder='Last Name' name='name' required />
                        <input type="date" placeholder='Date of Birth' name='name' required />
                        <input type="email" placeholder="Email" name="email" required />
                        <input type="password" placeholder="Password" name="password" required />
                        <input type="password" placeholder="Confirm Password" name="password" required />
                        <button>Register</button>
                    </form>
                    <button class="create-account-button">
                        <Link to="/login">Have An Account? Click Here</Link>
                    </button>
                </div>
            </ul>
        </div >
        );
}