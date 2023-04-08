import React, { useState } from "react";
import Dropdown from "../components/dropdown";
import "../styles/landingPage.css"
import AddListingPopup from "../components/AddListingPopup";

export default function LandingPage(page) {
    const [searchText, setSearchText] = useState("");
    const [auctionItems, setAuctionItems] = useState([{
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }, {
        "image": "dummy.png",
        "name": "name",
        "higherBid": "10000000"
    }]);
    const handleChange = (e) => {
        setSearchText(e.target.value);
    };
    const searchOptions = [
        "Item Name",
        "User Name"
    ];

    const categories = [
        "c1",
        "c2",
        "c3",
        "c4"
    ]
    const [showAddListingPopup, setShowAddListingPopup] = useState(false);

    const handleOpenAddListingPopup = () => {
        setShowAddListingPopup(true);
    };

    const handleCloseAddListingPopup = () => {
        setShowAddListingPopup(false);
    };

    const handleAddListing = (formData) => {
        // Handle submitting the form data (e.g. send it to your server)
        console.log(formData);

        // Close the popup form
        setShowAddListingPopup(false);
    };
    return (
        <div className="landing_page">
            <div className="landing_serach_container">
                <Dropdown searchOptions={searchOptions} width="145px"></Dropdown>
                <input className="landing_search_textfield" type="text" value={searchText} onChange={handleChange}></input>
                <button className="landing_search_button">Search</button>
            </div>
            <div className="landing_category">
                <div className="landing_category_title_floor">
                    <div>
                        <p className="landing_category_container_title">Category</p>
                        <hr style={{ width: "105px", margin: "5px 0px 0px 0px", alignSelf: "flex-start" }}></hr>
                    </div>
                    <div>
                        <button className="landing_category_new_item" onClick={handleOpenAddListingPopup}>Add Listing</button>
                        {showAddListingPopup && (
                            <AddListingPopup onClose={handleCloseAddListingPopup} onSubmit={handleAddListing} />
                        )}
                    </div>

                </div>
                <div className="landing_category_container">
                    <Category categories={categories}></Category>
                </div>
            </div>
            <div className="landing_items_container">
                {auctionItems.map((item, index) => (
                    <div className="landing_items_item" key={index}>
                        <img className="landing_items_item_img" src={require("../assets/item/" + item.image)} alt="Item Image"></img>
                        <p className="landing_items_item_p">{item.name}</p>
                        <p className="landing_items_item_p">${item.higherBid}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

function Category(props) {
    return (
        <div className="landing_categories">
            {props.categories.map((item, index) => (
                <div className="landing_category_item" key={index}>
                    <p>{item}</p>
                    <hr></hr>
                </div>
            ))}
        </div>
    );
}