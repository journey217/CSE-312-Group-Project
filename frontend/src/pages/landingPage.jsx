import React, {useEffect, useState} from "react";
import Dropdown from "../components/dropdown";
import "../styles/landingPage.css"
import AddListingPopup from "../components/AddListingPopup";
import Auction_detail from "../components/auctionDetail";

export default function LandingPage(page) {
    const [searchText, setSearchText] = useState("");
    const [auctionItems, setAuctionItems] = useState([]);

    useEffect(() => {
        fetch("/landing_page_items")
            .then(res => res.json())
            .then(data => {
                console.log(data)
                setAuctionItems(data);
            })
    }, [])

    const handleChange = (e) => {
        setSearchText(e.target.value);
    };

    const categories = [
        "All",
        "Car Parts",
        "Electronics",
        "Home Decor",
        "Clothing",
        "Toys",
        "Sports",
        "Appliances"
    ]
    const [showAddListingPopup, setShowAddListingPopup] = useState(false);
    const [auctionDetailOn, setAuctionDetailOn] = useState(false)

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
    const auctionDetail_show = () => {
        setAuctionDetailOn(true)
    }
    const close_auction_detail = () => {
        setAuctionDetailOn(false)
    }
    return (
        <div className="landing_page">
            {
                auctionDetailOn && (
                    <Auction_detail close={close_auction_detail}/>
                )
            }
            <div className="landing_search_container">
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
                    <div className="landing_items_item" key={index} onClick={auctionDetail_show}>
                        <img className="landing_items_item_img" src={"/image/" + item.image} alt={item.name}></img>
                        <p className="landing_items_item_p">{item.name}</p>
                        <p className="landing_items_item_p">{item.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

function Category(props) {
    return (
        <div className="landing_categories">
            {props.categories.slice(0,-1).map((item, index) => (
                <div className="landing_category_item" key={index}>
                    <p>{item}</p>
                    <hr></hr>
                </div>
            ))}
            {<div className="landing_category_item" key={props.categories.length - 1}>
                <p>{props.categories.slice(-1)}</p>
            </div>
            }
        </div>
    );
}