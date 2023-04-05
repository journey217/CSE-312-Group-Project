import React, { useState } from "react";
import "../styles/dropdown.css"

function Dropdown(props) {
    const [selectedOption, setSelectedOption] = useState("option1");

    const handleChange = (e) => {
        setSelectedOption(e.target.value);
    };

    return (
        <div className="dropdown" style={{ width: props.width }}>
            <select className="dropdown_select" value={selectedOption} onChange={handleChange}>
                {props.searchOptions.map((item, index) => (
                    <option value={props.searchOptions[index]} key={index}>
                        {item}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default Dropdown;
