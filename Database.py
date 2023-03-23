from pymongo import MongoClient
from uuid import uuid4
import datetime
from enum import Enum


class DBType(Enum):
    User = "Users"
    Auction = "Auctions"
    Bid = "Bids"


class UserVal(Enum):  # Editable User Values
    Username = "Username"
    Email = "Email"
    Password = "Password"  # Should be changed based on how we store passwords
    ProfilePicture = "ProfilePicture"
    Bio = "Bio"
    #  ID, Name cannot be changed after account creation
    #  auctions_made and bid_history are not directly changeable


class AuctionVal(Enum):  # Editable Auction Values
    ItemName = "Item_Name"
    Description = "Description"
    Category = "Category"
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

    def find_by_id(self, id_, type_):
        return self.db[type_.value].find_one({'ID': id_, 'deleted': False})

    def find_user_by_email(self, email):
        return self.users_collection.find_one({"Email": email, 'deleted': False})

    def add_bid_to_db(self):
        bid_id = uuid4()
        new_bid = {}
        # Add bidID to User.bids_history
        # Add bidID to Auction.bid_history
        pass

    def add_auction_to_db(self):
        auction_id = uuid4()
        new_auction = {}
        # Add auctionID to User.auctions_made
        pass

    def add_user_to_db(self):
        user_id = uuid4()
        new_user = {}
        pass

    def update_user(self, user_val, new_val):
        pass

    def update_auction(self, auction_val, new_val):
        pass

    def set_auction_images(self, images):   # Images is a list
        pass

    # Returns list of bids for a user
    # If there are multiple bids for an item, only have the newest bid in the return list
    def find_unique_item_bids_for_user(self):
        pass
