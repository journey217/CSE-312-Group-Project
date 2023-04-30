import React, {useEffect, useState} from "react";
import "../styles/profilePage.css";
import BasicProfile from "../assets/Profile_img.png"
import { Link, useNavigate } from 'react-router-dom';

export default function Login(page) {
    const [imageName, setImageName] = useState("")
    const [username, setUsername] = useState("")
    const [bidHistory, setBidHistory] = useState([])
    const [auctionHistory, setAuctionHistory] = useState([])

    const navigate = useNavigate()
    useEffect(() => {
        fetch('/profile')
            .then(res => res.json())
            .then(data => {
                console.log(data)
                if(data.status === 0){
                    navigate('/login')
                }
                else {
                    setImageName(data.user.image)
                    setUsername(data.user.username)
                    
                }
            })
    }, [])
    return(
        <div className="profile_background">
            <div className="profile_profile_area"> 
                <img src={imageName}
                className="profile_profile_area_profileImage"
                ></img>
                <div className="profile_profile_area_name_desc">
                    <h2>{username}</h2>
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