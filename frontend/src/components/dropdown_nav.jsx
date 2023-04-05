import { dropDown } from "./navItems";
import React, { useState } from "react";
import { Link } from 'react-router-dom';
import "../styles/dropdown_nav.css"
function Dropdown() {
    const [dropdown_nav, setDropdown] = useState(false);

    return (
        <>
            <ul className={dropdown_nav ?"dropdown clicked" : "dropdown_nav"} onClick={() => setDropdown(!dropdown_nav)}>
                {dropDown.map((item) => {
                    return (
                        <li key={item.id}>
                            <Link to={item.path} className={item.cName} onClick={() => setDropdown(false)}>
                                {item.title}
                            </Link>
                        </li>
                    );
                })}
            </ul>
        </>
    )
}
export default Dropdown;