import React, {useEffect, useState} from "react";
import { Link } from 'react-router-dom';
import "../styles/dropdown_nav.css"

export default function Dropdown({username}) {
    const [dropdown_nav, setDropdown] = useState(false);

    return (
        <ul className={dropdown_nav ? "dropdown clicked" : "dropdown_nav"} onClick={() => setDropdown(!dropdown_nav)}>
            {(username === 'Login'? dropDownItems1 : dropDownItems2).map((item) => {
                return (
                    <li key={item.id}>
                        <Link to={item.path} className={item.cName} onClick={() => setDropdown(false)}>
                            {item.title}
                        </Link>
                    </li>
                );
            })}
        </ul>
    )
}

const dropDownItems1 = [
    {
        id: 1,
        title: "Login",
        path: "./login",
        cName: "dd-item"
    },
    {
        id: 2,
        title: "Sign Up",
        path: "./registration",
        cName: "dd-item"
    }
]

const dropDownItems2 = [
    {
        id: 1,
        title: "Sign out",
        path: "./sign-out",
        cName: "dd-item"
    }
]