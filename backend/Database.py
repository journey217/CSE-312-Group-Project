from pymongo import MongoClient
from uuid import uuid4
import datetime
from enum import Enum


class DBType(Enum):
    User = "Users"
    Auction = "Auctions"
    Bid = "Bids"


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
        mongo_client = MongoClient("mongo")
        self.db = mongo_client["CSE312-Group-Project-Test"]
        self.auctions_collection = self.db["Auctions"]
        self.users_collection = self.db["Users"]
        self.bids_collection = self.db["Bids"]

    # type_ has to be DBType.User, DBType.Auction, or DBType.Bid
    def find_by_ID(self, ID, type_):
        return self.db[type_.value].find_one({'ID': ID, 'deleted': False})

    def find_user_by_email(self, email):
        return self.users_collection.find_one({"Email": email, 'deleted': False})

    def add_bid_to_db(self, userID, auctionID, price):
        bidID = uuid4()
        new_bid = {"ID": bidID,
                   "userID": userID,
                   "auctionID": auctionID,
                   "price": price,
                   "timestamp": datetime.datetime.now()
                   }
        # Add bid to Bids
        # Add bidID to User.bids_history
        # Add bidID to Auction.bid_history
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
        # Add auctionID to User.auctions_made
        return new_auction

    def add_user_to_db(self, username, email, hashed_password, profile_pic, bio, name):
        user_id = uuid4()
        new_user = {"ID": uuid4(),
                    "username": username,
                    "email": email,
                    "hashed_password": hashed_password,
                    "profile_pic": profile_pic,
                    "bio": bio,
                    "name": name,
                    "auctions_made": [],
                    "bid_history": []}
        # Add User to Users
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
        bid_list = self.users_collection.find_one({})
