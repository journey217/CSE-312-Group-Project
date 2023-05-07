import React, {useEffect, useState} from "react";
import "../styles/landingPage.css"
import AddListingPopup from "../components/AddListingPopup";
import {useNavigate} from "react-router-dom";
import {socket} from "./auctionDetail";


export default function LandingPage(page) {
    const [auctionItems, setAuctionItems] = useState([]);
    const [showAddListingPopup, setShowAddListingPopup] = useState(false);
    const navigate = useNavigate();
    useEffect(() => {
        fetch("/landing_page_items")
            .then(res => res.json())
            .then(data => {
                setAuctionItems(data);
                console.log(data)
                for (let room of data) {
                    socket.emit('leave', {'room': room.ID})
                }
            })
    }, [])

    const handleOpenAddListingPopup = () => {
        setShowAddListingPopup(true);
    };

    const handleCloseAddListingPopup = () => {
        setShowAddListingPopup(false);
    };

    const handleAddListing = () => {
        setShowAddListingPopup(false);
    };

    const navigateToItem = (item) => {
        navigate(`/item/${item.ID}`, { item })
    }

    return (
        <div className="landing_page">
            <div className="landing_category">
                <div className="landing_category_title_floor">
                    <div>
                        <button className="landing_category_new_item" onClick={handleOpenAddListingPopup}>Add Listing</button>
                        {showAddListingPopup && (
                            <AddListingPopup onClose={handleCloseAddListingPopup} onSubmit={handleAddListing} />
                        )}
                    </div>
                </div>
            </div>
            <div className="landing_items_container">
                {auctionItems.map((item, index) => (
                    <div className="landing_items_item" key={index} onClick={() => navigateToItem(item)}>
                        <img className="landing_items_item_img" src={"/image/" + item.image} alt={item.name}></img>
                        <p className="landing_items_item_p">{item.name}</p>
                        <p className="landing_items_item_p">{'$' + item.price}</p>
                    </div>
                ))}
            </div>
        </div >
    );
}