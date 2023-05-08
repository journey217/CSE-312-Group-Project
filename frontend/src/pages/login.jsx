import React, {useState} from "react";
import {useNavigate} from 'react-router-dom';
import "../styles/login.css";

function Login() {
    const navigate = useNavigate();
    const [errors, setError] = useState({submit: ''});

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/login-user', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data['status'] === '0') {
                    setError({ submit: data['error'] });
                } else {
                    setError({
                        submit: ''
                    });
                    navigate('/')
                    window.location.reload()
                }
            })
            .catch(error => console.error(error));
    };

    return (
        <div className="login">
            <ul>
                <header className="header">JBAY</header>
                <div className="login-form">
                    <form className="login-inputs" onSubmit={handleSubmit}>
                        <header className="formheader">Login</header>
                        <label htmlFor="email"></label>
                        <input type="email" placeholder="Email" name="email" required />
                        <label htmlFor="password"></label>
                        <input type="password" placeholder="Password" name="password" required />
                        <button className="login-button" type="submit">Login</button>
                        {errors.submit && <div className="error-message">{errors.submit}</div>}
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
export default Login;