import React, { useState } from "react";
import { Link } from 'react-router-dom';
import "../styles/navbar.css";

export default function Navbar() {

    const [openLinks, setOpenLinks] = useState(false);

    const toggleNavbar = () => {
        setOpenLinks(!openLinks)
    };

    return (
        <div>
            Navbar
        </div>
    );
};
