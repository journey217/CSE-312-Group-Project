import React, {useEffect, useState} from "react";
import "../styles/profilePage.css";
import BasicProfile from "../assets/Profile_img.png"

export default function Login(page) {
    return(
        <div className="profile_background">
            <div className="profile_profile_area"> 
                <img src={BasicProfile}
                className="profile_profile_area_profileImage"
                ></img>
                <div className="profile_profile_area_name_desc">
                    <h2>Name</h2>
                    <h3>desc</h3>
                </div>
            </div>
            <div className="profile_bid_history">
                <div className="profile_bid_container">
                    <h2>Selling list</h2>
                </div>
                <div className="profile_bid_container">
                    <h2>Bids history</h2>
                </div>
            </div>
        </div>
    );
}