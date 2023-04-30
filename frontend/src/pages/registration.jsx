import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import "../styles/registration.css";

function Register() {
    const [errors, setErrors] = useState({
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        submit: ''
    });
    const navigate = useNavigate();
    const handleSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);

        fetch('/register-user', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.errors) {
                    const errors = data.errors;
                    let allErrors = {};
                    errors.forEach(error => {
                        const field = Object.keys(error)[0];
                        allErrors[field] = error[field];
                    });
                    setErrors({ ...allErrors, submit: 'Unable to create account, please check all fields' });
                } else {
                    setErrors({
                        username: '',
                        email: '',
                        password1: '',
                        password2: '',
                        submit: ''
                    });
                    navigate('/')
                    window.location.reload()
                }
            })
            .catch(error => console.error(error));
    };

    return (
        <div className='register'>
            <ul>
                <header className="header">JBAY</header>
                <div className="register-form">
                    <form className="reg-inputs" onSubmit={handleSubmit}>
                        <header className="formheader">Create New Account</header>
                        {errors.username && <div className="error-message">{errors.username}</div>}
                        <input type="text" placeholder='Username' name='username' required />
                        {errors.email && <div className="error-message">{errors.email}</div>}
                        <input type="email" placeholder="Email" name="email" required />
                        {errors.password1 && <div className="error-message">{errors.password1}</div>}
                        <input type="password" placeholder="Password" name="password1" required />
                        {errors.password2 && <div className="error-message">{errors.password2}</div>}
                        <input type="password" placeholder="Confirm Password" name="password2" required />
                        <button className="register-button" type="submit" >Register</button>
                        {errors.submit && <div className="error-message">{errors.submit}</div>}
                    </form>
                    <button className="login-redirect-button" onClick={() => { navigate("/login") }}>
                        Have An Account? Click Here
                    </button>
                </div>
            </ul>
        </div>
    );
}
export default Register;