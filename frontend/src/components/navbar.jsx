import React, { useState } from "react";
import { Link } from 'react-router-dom';
import "../styles/navbar.css";
import { navItems } from "./navItems";
import Dropdown from "./dropdown_nav";

/* implementation for navbar */
export default function Navbar() {
    const [dropdown, setDropdown] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
    };

    return (
        <nav className="navbar">
            <Link to="/" className="navbar-logo">
                LOGO IMAGE
            </Link>
            <ul className="nav-items">
                <li>
                    <form className="search-form">
                        <input type="text" placeholder="Search" onChange={handleSearchChange} />
                    </form>
                </li>
                {navItems.filter((item) => item.title.toLowerCase().includes(searchQuery.toLowerCase())).map((item) => {
                    if (item.title === "Profile") {
                        return (
                            <li
                                key={item.id}
                                className={item.cName}
                                onMouseEnter={() => setDropdown(true)}
                                onMouseLeave={() => setDropdown(false)}
                            >
                                <Link to={item.path}>{item.title}</Link>
                                {dropdown && <Dropdown />}
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