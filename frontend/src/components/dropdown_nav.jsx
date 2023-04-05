import { dropDown } from "./navItems";
import React, { useState } from "react";
import { Link } from 'react-router-dom';
import "../styles/dropdown_nav.css"
function Dropdown() {
    const [dropdown, setDropdown] = useState(false);

    return (
        <>
            <ul className={dropdown ?"dropdown clicked" : "dropdown"} onClick={() => setDropdown(!dropdown)}>
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