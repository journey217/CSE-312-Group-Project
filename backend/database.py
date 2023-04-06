from pymongo import MongoClient
from uuid import uuid4
import datetime
from enum import Enum
from os import environ as environment


class DBType(Enum):
    User = "Users"
    Auction = "Auctions"
    Bid = "Bids"


class Categories(Enum):
    Car_Parts = "Car Parts"
    Electronics = "Electronics"
    Home_Decor = "Home Decor"
    Clothing = "Clothing"
    Toys = "Toys"
    Sports = "Sports"
    Appliances = "Appliances"


class UserVal(Enum):  # Editable User Values
    Username = "username"
    Email = "email"
    Password = "hashed_password"  # Should be changed based on how we store passwords
    ProfilePicture = "profile_pic"
    Bio = "bio"
    #  ID, Name cannot be changed after account creation
    #  auctions_made and bid_history are not directly changeable


class AuctionVal(Enum):  # Editable Auction Values
    Name = "name"
    Description = "description"
    Category = "category"
    # bid_history is not directly changeable. new_bid() changes it
    # Images Has Separate Function To Change
    # start_time, ID, creatorID are not changeable
    # end_time is currently not changeable but might be in the future

# Bids cannot be modified after creation


class Database:
    def __init__(self):
        if environment.get('DOCKER') == '1':  # Set By Docker to 1 to change MongoClient Address
            mongo_client = MongoClient('mongo', uuidRepresentation='standard')
        else:  # Otherwise None
            mongo_client = MongoClient('localhost', uuidRepresentation='standard')
        self.db = mongo_client["CSE312-Group-Project-Test"]
        self.auctions_collection = self.db["Auctions"]
        self.users_collection = self.db["Users"]
        self.bids_collection = self.db["Bids"]

    # type_ has to be DBType.User, DBType.Auction, or DBType.Bid
    def find_by_ID(self, ID, type_):
        return self.db[type_.value].find_one({"ID": ID}, projection={"_id": False, "ID": False})

    def find_user_by_email(self, email):
        return self.users_collection.find_one({"email": email}, projection={"_id": False, "ID": False})

    def add_bid_to_db(self, userID, auctionID, price):
        bidID = uuid4()
        new_bid = {"ID": bidID,
                   "userID": userID,
                   "auctionID": auctionID,
                   "price": price,
                   "timestamp": datetime.datetime.now()
                   }
        # Add bid to Bids
        self.bids_collection.insert_one(new_bid)
        # Add bidID to User.bids_history
        self.users_collection.update_one({"ID": userID}, {"$push": {"bid_history": bidID}})
        # Add bidID to Auction.bid_history
        self.auctions_collection.update_one({"ID": auctionID}, {"$push": {"bid_history": bidID}})
        return new_bid

    def add_auction_to_db(self, creatorID, name, desc, images, category, end_time):
        auctionID = uuid4()
        new_auction = {"ID": auctionID,
                       "creatorID": creatorID,
                       "name": name,
                       "description": desc,
                       "category": category,
                       "images": images,
                       "start_time": datetime.datetime.now(),
                       "end_time": end_time,
                       "bid_history": []}
        # Add Auction to Auctions
        self.auctions_collection.insert_one(new_auction)
        # Add auctionID to User.auctions_made
        self.users_collection.update_one({"ID": creatorID}, {"$push": {"auctions_made": auctionID}})
        return new_auction

    def add_user_to_db(self, username, email, hashed_password, bio, name, profile_pic="blank.jpeg"):
        user_id = uuid4()
        new_user = {"ID": user_id,
                    "username": username,
                    "email": email,
                    "hashed_password": hashed_password,
                    "profile_pic": profile_pic,
                    "bio": bio,
                    "name": name,
                    "auctions_made": [],
                    "bid_history": []}
        # Add User to Users
        self.users_collection.insert_one(new_user)
        return new_user

    # user_val is an enum of UserVal
    def update_user(self, userID, user_val, new_val):
        pass

    # auction_val is an enum of AuctionVal
    def update_auction(self, auctionID, auction_val, new_val):
        pass

    def set_auction_images(self, auction, images):   # Images is a list of filenames
        pass

    # Returns list of bids for a user
    # If there are multiple bids for an item, only have the newest bid in the return list
    def find_unique_item_bids_for_user(self, userID):
        unique_bids = {}  # auctionIDs -> bid
        users_bidIDs = self.users_collection.find_one({"ID": userID})["bid_history"]
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
        return [value for _, value in unique_bids.items()]  # In future needs to be sorted

    def home_page_items(self):
        pass
