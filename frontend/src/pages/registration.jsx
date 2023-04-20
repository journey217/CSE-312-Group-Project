import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import "../styles/registration.css";

function Register() {
    const [errors, setErrors] = useState({});
    const [success, setSuccess] = useState(false);
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
                const errors = data.errors
                console.log(errors)
                if (data.errors) {
                    setErrors(data.errors);
                    setSuccess(false);
                } else {
                    setErrors({});
                    setSuccess(true);
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
                        <input type="text" placeholder='Username' name='username' required />
                        {errors.username && <div className="error-message">{errors.username}</div>}
                        <input type="email" placeholder="Email" name="email" required />
                        {errors.email && <div className="error-message">{errors.email}</div>}
                        <input type="password" placeholder="Password" name="password1" required />
                        {errors.password && <div className="error-message">{errors.password}</div>}
                        <input type="password" placeholder="Confirm Password" name="password2" required />
                        {errors.confirm_password && <div className="error-message">{errors.confirm_password}</div>}

                        <button className="register-button" type="submit" >Register</button>
                        {errors.submit && <div className="error-message">{errors.submit}</div>}
                        {success && <div>Account Creation Success!</div>}
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