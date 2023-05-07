import React, { useEffect, useState } from 'react';
import "../styles/auction_detail.css"
import { io } from "socket.io-client";
import {redirect} from "react-router-dom";

export let socket = io.connect(`http://${window.location.hostname}:5000/item`, {
    transports: ['websocket']
})

const addMessage = (data) => {
    const input = document.querySelector('.ws_bids');
    input.innerHTML = "<div class='auction_detail_bid_history_item'>" +
                            "<p class='auction_detail_bid_user_id'>" + data.username.toString() + "</p>" +
                            "<p class='auction_detail_price'>" +  "$" + data.bid_price.toString() + "</p>" +
                            "<p class='auction_detail_timestamp'>" + new Date() + "</p>" +
                        "</div>" + input.innerHTML;
}

socket.on('message', function (data) {
    addMessage(data)
});

socket.on('winner', function (data) {
    redirect('/')
    add_winner(data)
});

const add_winner = (data) => {
    const input = document.getElementById('winner_string');
    input.innerHTML = "<b class=\'auction_detial_time_left\'>" + "Time expired. " +  data.winner.toString() + " has won!" + "</b>"
}
export default function Auction_detail() {
    const itemID = window.location.href.split('/')[4]
    socket.emit("join", {'room': itemID});
    const [item, setItem] = useState(null)
    const [current, setCurrent] = useState("")
    const [xsrf_token, setXSRFToken] = useState("")
    const [vendor, setVendor] = useState(null)
    const [countDownString, setCountDownString] = useState('00:00:00')
    useEffect(() => {
        fetch(`${itemID}`)
            .then(response => response.json())
            .then(data => {
                setCurrent(data.user)
                setItem(data.item)
                setXSRFToken(data.xsrf_token)
                console.log(data)
                setVendor(data.username)
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    const countDown = () => {
        const countDownDate = new Date(item.end_time).getTime();

        const x = setInterval(() => {
            const now = new Date().getTime();
            const distance = countDownDate - now;

            if (distance < 0) {
                clearInterval(x);
                socket.emit("end_auction", { 'auction_id': itemID});
            } else {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                let cd;
                if (days > 0) {
                    cd = `${days} days `;
                } else {
                    cd = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                }

                setCountDownString(cd);
            }
        }, 1000);
    };

    useEffect(() => {
        if (item !== null) {
            countDown();
        }
    }, [item]);


    function handleBid() {
        const input = document.querySelector('.auction_detial_bid_input');
        const token = document.getElementById('xsrf_token').value;
        const price = input.value;

        console.log(itemID)

        socket.emit("message", { 'type': 'bid', 'auctionID': itemID, 'price': price, "user": current, 'room': itemID, 'token': token });
    }


    return (
        <div className='auction_detail_popup_background'>
            <div className='auction_detail_popup'>
                <div className='auction_detail_title'>
                    <h2 className='auction_detail_item_name'>{item && item.name}</h2>
                </div>
                <hr className='auction_detail_hr' />
                <div className='auction_detail_item_desc_container'>
                    <img className='auction_detail_image' src={item && `/image/${item.image}`}></img>
                    <div className='auction_detail_item_desc'>
                        <p className='auction_detail_vendor'>{item && `Description : ${item.description}`}</p>
                        <p className='auction_detail_vendor'>{item && `Condition : ${item.condition}`}</p>
                        <p className='auction_detail_vendor'>{vendor && `Vendor : ${vendor}`}</p>
                    </div>
                </div>
                <div id="winner_string"></div>
                <b className='auction_detial_time_left'>{countDownString}</b>
                <input className='auction_detial_bid_input' type="number"></input>
                <input hidden id="xsrf_token" value={xsrf_token}></input>
                <button className="auction_detial_bid_button" type='submit' onClick={handleBid}>BID</button>
                <div className='auction_detail_bid_history'>
                    <div className="ws_bids"></div>
                    {item && item.bid_history.map((bid, index) => (
                        <div className='auction_detail_bid_history_item' key={index}>
                            <p className='auction_detail_bid_user_id'>{bid.username}</p>
                            <p className='auction_detail_price'> ${bid.price} </p>
                            <p className='auction_detail_timestamp'>{bid.timestamp}</p>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    )
}