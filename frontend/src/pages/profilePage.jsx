import React, {useEffect, useState} from "react";
import "../styles/profilePage.css";
import {useNavigate} from 'react-router-dom';


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
                if (data.status === 0) {
                    navigate('/login')
                }
                else {
                    setImageName(data.user.image)
                    setUsername(data.user.username)
                    setAuctionHistory(data.user.auctionHistory)
                    console.log(auctionHistory)
                    setBidHistory(data.user.bidHistory)
                }
            })
    })

    return (
        <div className="profile_background">
            <div className="profile_profile_area">
                <img src={imageName} alt='profile picture'
                    className="profile_profile_area_profileImage"
                ></img>
                <div className="profile_profile_area_name_desc">
                    <h2>{username}</h2>
                </div>
            </div>
            <div className="profile_bid_history">
                <div className="profile_bid_container">
                    <h2>Selling list</h2>
                    <div className="item_row_top">
                        <p className="item_row_title">Name:</p>
                        <p className="item_row_title">Time Ends:</p>
                        <p className="item_row_title">Status:</p>
                        <p className="item_row_title">Amount Bid:</p>
                    </div>
                    {auctionHistory && auctionHistory.map(item => (

                        <div key={item.id} className="item_row" style={{
                            backgroundColor: item.ongoing ? '#9AFF86' : '#CCCCCC',
                            borderColor: item.ongoing ? '#43ac2d' : '#8E8E8E',
                        }}>

                            <div className="item_row_bottom">
                                <p className="item_row_value">{item.name}</p>
                                <p className="item_row_value">{item.endtime}</p>
                                <p className="item_row_value">{item.ongoing ? "On Going" : "Ended"}</p>
                                <p className="item_row_value">{item.price}</p>
                            </div>
                        </div>


                    ))}
                </div>
                <div className="profile_bid_container">
                    <h2>Bids history</h2>
                    {bidHistory && bidHistory.map(item => (
                        <div key={item.id} className="item_row">
                            <p>Name: {item.name}</p>
                            <p>Time Remaining: {item.endtime}</p>
                            <p>Status: {item.ongoing}</p>
                            <p>Amount Bid: {item.bid}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}