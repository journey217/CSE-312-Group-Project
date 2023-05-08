import React, {useEffect, useState} from "react";
import { Link } from 'react-router-dom';
import "../styles/navbar.css";
import Dropdown from "./dropdown_nav";


export default function Navbar() {
    const [dropdown, setDropdown] = useState(false);
    const [searchQuery] = useState("");
    const [username, setUsername] = useState('Login');

    useEffect(() => {
        fetch('/myUsername')
            .then(res => res.json())
            .then(data => {
                if(data.status){
                    setUsername(data.username)
                } else {
                    setUsername('Login')
                }
            })
    }, [])

    const navItems = [
    {
        id: 1,
        title: "Home",
        path: "./",
        cName: "nav-item"
    },
    {
        id: 2,
        title: "Profile",
        path: "./profile",
        cName: "nav-item"
    },
    {
        id: 3,
        title: 'Username',
        path: "",
        cName: "nav-item"
    },
]


    return (
        <nav className="navbar">
            <Link to="/" className="navbar-logo">
                <img className="navbar-logo" src="/logo.png" alt="jBay Logo" />
            </Link>
            <ul className="nav-items">
                {navItems.filter((item) => item.title.toLowerCase().includes(searchQuery.toLowerCase())).map((item) => {
                    if (item.id === 3) {
                        return (
                            <li
                                key={item.id}
                                className={item.cName}
                                onMouseEnter={() => setDropdown(true)}
                                onMouseLeave={() => setDropdown(false)}
                            >
                                <Link to={item.path}>{username}</Link>
                                {dropdown && <Dropdown username={username}/>}
                            </li>
                        );
                    }
                    return (
                        <li key={item.id} className={item.cName}>
                            <Link to={item.path}>{item.title}</Link>
                        </li>
                    );
                })}
            </ul>
        </nav>
    );
};
