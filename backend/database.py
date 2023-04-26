from pymongo import MongoClient
from uuid import uuid4
import datetime
from enum import Enum
from os import environ as environment
import random
from datetime import datetime
import re
from hashlib import sha256


class DBType(Enum):
    User = "Users"
    Auction = "Auctions"
    Bid = "Bids"


class Database:
    def __init__(self):
        # Set By Docker to 1 to change MongoClient Address
        if environment.get('DOCKER') == '1':
            mongo_client = MongoClient('mongo', uuidRepresentation='standard')
        else:  # Otherwise None
            mongo_client = MongoClient(
                'localhost', uuidRepresentation='standard')
        self.db = mongo_client["CSE312-Group-Project-Test"]
        self.auctions_collection = self.db["Auctions"]
        self.users_collection = self.db["Users"]
        self.bids_collection = self.db["Bids"]
        self.image_collection = self.db["Images"]

    # type_ has to be DBType.User, DBType.Auction, or DBType.Bid
    def find_by_ID(self, ID, type_):
        return self.db[type_.value].find_one({"ID": ID}, projection={"_id": False, "ID": False})

    def find_user_by_ID(self, ID):
        return self.users_collection.find_one({"ID": ID}, projection={"_id": False, "ID": False})

    def find_user_by_email(self, email):
        return self.users_collection.find_one({"email": email}, projection={"_id": False, "ID": False, "hashed_password": False, "auctions_made": False, "bid_history": False})

    def find_user_by_token(self, token):
        token = str(token)
        token = sha256(token.encode()).hexdigest()
        print(token)
        return self.users_collection.find_one({"token": token}, projection={"_id": False, 'token': False, 'hashed_password': False})

    def find_user_by_username(self, username):
        return self.users_collection.find_one({"username": username}, projection={"_id": False, "ID": False})

    def add_bid_to_db(self, userID, auctionID, price):
        bidID = uuid4()
        new_bid = {"ID": bidID,
                   "userID": userID,
                   "auctionID": auctionID,
                   "price": price,
                   "timestamp": datetime.now()
                   }
        # Add bid to Bids
        self.bids_collection.insert_one(new_bid)
        # Add bidID to User.bids_history
        self.users_collection.update_one(
            {"ID": userID}, {"$push": {"bid_history": bidID}})
        # Add bidID to Auction.bid_history
        self.auctions_collection.update_one(
            {"ID": auctionID}, {"$push": {"bid_history": bidID}})
        return new_bid

    def add_auction_to_db(self, creatorID, name, desc, end_time, price, image_name="NoImage.jpg", condition="New"):
        auctionID = uuid4()
        new_auction = {"ID": auctionID,
                       "creatorID": creatorID,
                       "name": name,
                       "description": desc,
                       "price": price,
                       "condition": condition,
                       "image": image_name,
                       "start_time": datetime.now(),
                       "end_time": end_time,
                       "bid_history": []}
        # Add Auction to Auctions
        self.auctions_collection.insert_one(new_auction)
        # Add auctionID to User.auctions_made
        self.users_collection.update_one(
            {"ID": creatorID}, {"$push": {"auctions_made": auctionID}})
        return new_auction

    def add_user_to_db(self, username, email, hashed_password, profile_pic="NoUser.jpg"):
        user_id = uuid4()
        new_user = {"ID": user_id,
                    "username": username,
                    "email": email,
                    "hashed_password": hashed_password,
                    "profile_pic": profile_pic,
                    "auctions_made": [],
                    "bid_history": []}
        # Add User to Users
        self.users_collection.insert_one(new_user)
        return new_user

    # Returns list of bids for a user
    # If there are multiple bids for an item, only have the newest bid in the return list
    def find_unique_item_bids_for_user(self, userID):
        unique_bids = {}  # auctionIDs -> bid
        users_bidIDs = self.users_collection.find_one({"ID": userID})[
            "bid_history"]
        for bidID in users_bidIDs:
            bid = self.find_by_ID(bidID, DBType.Bid)
            auctionID = bid["auctionID"]
            if auctionID in unique_bids.keys():
                current_bid_timestamp = unique_bids[auctionID]["timestamp"]
                new_bid_timestamp = bid["timestamp"]
                if new_bid_timestamp > current_bid_timestamp:
                    unique_bids[auctionID] = bid
            else:
                unique_bids[auctionID] = bid
        return [value for _, value in unique_bids.items()]

    def landing_page_items(self):
        find_items = self.auctions_collection.find({"end_time": {"$gt": datetime.utcnow()}},
                                                   projection={"_id": False, "creatorID": False, "start_time": False})
        items_list = [x for x in find_items]
        random.shuffle(items_list)
        return items_list

    def all_item_search(self):
        items_list = [x for x in self.auctions_collection.find(
            {}, projection={"_id": False})]
        return items_list

    def item_find(self, query):
        search_list = []
        items_list = self.all_item_search()
        for item in items_list:
            # The 're' library is used to find if a string contains a given substring while ignoring case
            if re.search(query, item.get("name"), re.IGNORECASE):
                search_list.append(item)
        return search_list

    def add_image(self, filename):
        self.image_collection.insert_one({'filename': filename})

    def image_exists(self, filename):
        if self.image_collection.count_documents({'filename': filename}) > 0:
            return True
        return False
