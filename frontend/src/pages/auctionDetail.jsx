import React, { useState } from 'react';
import "../styles/auction_detail.css"


export default function auction_detail(page) {
    return (
        <div className='auction_detail_popup_background'>
            <div className='auction_detail_popup'>
                <div className='auction_detail_title'>
                    <h2 className='auction_detail_item_name'>name</h2>
                </div>
                <hr className='auction_detail_hr' />
                <img src={require("../assets/item/dummy.png")}></img>
                <p className='auction_detail_vendor'>vendor: xxxx</p>
                <b className='auction_detial_time_left'>00:00:00</b>
                <input className='auction_detial_bid_input' type="number"></input>
                <button className="auction_detial_bid_button" type='submit'>BID</button>
                <div className='auction_detail_bid_history'>
                    <div className='auction_detail_bid_history_item'>
                        <p className='auction_detail_bid_user_id'>name</p>
                        <p className='auction_detail_price'> $10000000 </p>
                        <p className='auction_detail_timestamp'> 12:13:21 jul.03.2021 </p>
                    </div>
                    <div className='auction_detail_bid_history_item'>
                    <p className='auction_detail_bid_user_id'>name</p>
                        <p className='auction_detail_price'> $9000000 </p>
                        <p className='auction_detail_timestamp'> 12:13:21 jul.03.2021 </p>

                    </div>
                    <div className='auction_detail_bid_history_item'>
                    <p className='auction_detail_bid_user_id'>name</p>
                        <p className='auction_detail_price'> $1 </p>
                        <p className='auction_detail_timestamp'> 12:13:21 jul.03.2021 </p>
                    </div>
                </div>

            </div>
        </div>
    )
}