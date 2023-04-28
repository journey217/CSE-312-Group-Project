import React, { useEffect, useState, useRef } from 'react';
import "../styles/auction_detail.css"
import {io} from "socket.io-client";

let socket = io.connect(`http://${window.location.hostname}:5000/item`)

export default function Auction_detail() {
    const itemID = window.location.href.split('/')[4]
    const userID = document.cookie;
    const [item, setItem] = useState(null)
    const [vendor, setVendor] = useState(null)
    const [countDownString, setCountDownString] = useState('00:00:00')
    // const socketRef = useRef(null);
    useEffect(() => {
        fetch(`${itemID}`)
            .then(response => response.json())
            .then(data => {
                setItem(data.item)
                fetch(`/users/${data.item.creatorID}`)
                    .then(response => response.json())
                    .then(data => {
                        setVendor(data.user)
                    })
                    .catch(error => {
                        console.log(error);
                    })
            })
            .catch(error => {
                console.log(error);
            });


        // if (!socketRef.current) {
        //     // const socket = new WebSocket('ws://' + window.location.host + '/websocket');
        //     socketRef.current = io.connect(`http://${window.location.hostname}:5000/item`)
        //     // socketRef.current = new WebSocket(`ws://${window.location.hostname}:5000/item`);
        //     socketRef.current.onopen = () => {
        //         console.log("connected to ws://localhost:5000/item");
        //     }
        //     socketRef.current.onclose = error => {
        //         console.log("disconnect from ws://localhost:5000/item");
        //         console.log(error);
        //     };
        //     socketRef.current.onerror = error => {
        //         console.log("connection error ws://localhost:5000/item");
        //         console.log(error);
        //     };
        // }
    }, []);

    const countDown = () => {
        const countDownDate = new Date(item.end_time).getTime();

        const x = setInterval(() => {
            const now = new Date().getTime();
            const distance = countDownDate - now;

            if (distance < 0) {
                clearInterval(x);
                setCountDownString('Time Expired');
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
        const price = input.value;


        socket.emit("message",{'item': itemID, 'price': price})
        
        // const interval = setInterval(() => {
        //     if (socketRef.current.readyState === 1) {
        //         socketRef.current.send(JSON.stringify({ type: 'bid', data: { price: price } }));
        //         clearInterval(interval);
        //     }
        // }, 100);
        
    }

    return (
        <div className='auction_detail_popup_background'>
            <div className='auction_detail_popup'>
                <div className='auction_detail_title'>
                    <h2 className='auction_detail_item_name'>{item && item.name}</h2>
                </div>
                <hr className='auction_detail_hr' />
                <img className='auction_detail_image' src={item && `/image/${item.image}`}></img>
                <p className='auction_detail_vendor'>{vendor && `vendor : ${vendor.username}`}</p>
                <b className='auction_detial_time_left'>{countDownString}</b>
                <input className='auction_detial_bid_input' type="number"></input>
                <button className="auction_detial_bid_button" type='submit' onClick={handleBid}>BID</button>
                <div className='auction_detail_bid_history'>
                    {item && item.bid_history.map((item, index) => (
                        <div className='auction_detail_bid_history_item' key={index}>
                            <p className='auction_detail_bid_user_id'>{item.user_id}</p>
                            <p className='auction_detail_price'> ${item.price} </p>
                            <p className='auction_detail_timestamp'>{item.timestamp}</p>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    )
}