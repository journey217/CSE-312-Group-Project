import React, { useEffect, useState } from 'react';
import "../styles/auction_detail.css"
import { io } from "socket.io-client";
import { redirect } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

export let socket = io.connect(`https://${window.location.hostname}/item`, {
    transports: ['websocket']
})

socket.on('message', function (data) {
    addMessage(data)
});

socket.on('winner', function (data) {
    redirect('/')
    addWinner(data)
});

const addMessage = (data) => {
    const input1 = document.getElementById('error_string');
    input1.innerHTML = "<b class=\'auction_detial_time_left\'></b>"
    const input = document.querySelector('.ws_bids');
    const highest = document.getElementById('HighestBid_string');
    highest.innerHTML = "<b class=\'auction_detial_time_left\'> Current bid: " + data.bid_price.toString() + "</b>"
    const now = new Date();

    const formatter = new Intl.DateTimeFormat('en-US', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    });
    const formattedDate = formatter.format(now);

    input.innerHTML = "<div class='auction_detail_bid_history_item'>" +
        "<p class='auction_detail_bid_user_id'>" + data.username.toString() + "</p>" +
        "<p class='auction_detail_price'>" + "$" + data.bid_price.toString() + "</p>" +
        "<p class='auction_detail_timestamp'>" + formattedDate
        + "</p>" +
        "</div>" + input.innerHTML;
}

const addWinner = (data) => {
    const input = document.getElementById('winner_string');
    input.innerHTML = "<b class='auction_detial_time_left'>" + "Time expired. " + data.winner.toString() + " has won!" + "</b>"
}

socket.on('error', function (data) {
    redirect('/')
    add_error(data)
});

const changeToEST = (dateString) => {
    const date = new Date(dateString);

    const options = {
        weekday: 'short',
        month: 'short',
        day: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short',
        timeZone: 'America/New_York'
    };

    const formatter = new Intl.DateTimeFormat('en-US', options);
    const formattedDate = formatter.format(date);
    return formattedDate
}

const add_error = (data) => {
    const input = document.getElementById('error_string');
    input.innerHTML = "<b class=\'error_class\'>" + data + "</b>"
}

export default function Auction_detail() {
    const navigate = useNavigate()
    const itemID = window.location.href.split('/')[4]
    const [connected, setConnected] = useState(false)
    if (connected === false) {
        socket.emit("join", { 'room': itemID });
        setConnected(true)
    }
    const [item, setItem] = useState(null)
    const [current, setCurrent] = useState("")
    const [xsrf_token, setXSRFToken] = useState("")
    const [vendor, setVendor] = useState(null)
    const [countDownString, setCountDownString] = useState('00:00:00')


    const handleBid = () => {
        const input = document.querySelector('.auction_detial_bid_input');
        const token = document.getElementById('xsrf_token').value;
        const price = input.value;
        socket.emit("message", { 'type': 'bid', 'auctionID': itemID, 'price': price, "user": current, 'room': itemID, 'token': token });
    }

    useEffect(() => {
        fetch(`${itemID}`)
            .then(response => response.json())
            .then(data => {
                if (data.error === 1) {
                    navigate('/')
                }
                setCurrent(data.user)
                setItem(data.item)
                setXSRFToken(data.xsrf_token)
                setVendor(data.username)
                const highest = document.getElementById('HighestBid_string');

                const price = data.item.price ;

                highest.innerHTML = "<b class=\'auction_detial_time_left\'> Current bid: " + price + "</b>"
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
                socket.emit("end_auction", { 'auction_id': itemID });
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

    return (
        <div className='auction_detail_popup_background'>
            <div className='auction_detail_popup'>
                <div className='auction_detail_title'>
                    <h2 className='auction_detail_item_name'>{item && item.name}</h2>
                </div>
                <hr className='auction_detail_hr' />
                <div className='auction_detail_item_desc_container'>
                    <img className='auction_detail_image' alt="Item" src={item && `/image/${item.image}`}></img>
                    <div className='auction_detail_item_desc'>
                        <p className='auction_detail_vendor'>{item && `Description : ${item.description}`}</p>
                        <p className='auction_detail_vendor'>{item && `Condition : ${item.condition}`}</p>
                        <p className='auction_detail_vendor'>{vendor && `Vendor : ${vendor}`}</p>
                    </div>
                </div>
                <div id="error_string"></div>
                <div id="winner_string"></div>
                <div id="HighestBid_string">
                </div>
                <b className='auction_detial_time_left'>{countDownString}</b>
                <form onSubmit={(e) => e.preventDefault()}>
                    <input className='auction_detial_bid_input' type="number"></input>
                    <input hidden readOnly id="xsrf_token" value={xsrf_token}></input>
                    <button className="auction_detial_bid_button" type='submit' onClick={handleBid}>BID</button>
                </form>
                <div className='auction_detail_bid_history'>
                    <div className="ws_bids"></div>
                    {item && item.bid_history.map((bid, index) => (
                        <div className='auction_detail_bid_history_item' key={index}>
                            <p className='auction_detail_bid_user_id'>{bid.username}</p>
                            <p className='auction_detail_price'> ${bid.price} </p>
                            <p className='auction_detail_timestamp'>{changeToEST(bid.timestamp)}</p>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    )
}