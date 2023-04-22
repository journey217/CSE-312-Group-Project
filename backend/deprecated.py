

class Categories(Enum):
    Car_Parts = "Car Parts"
    Electronics = "Electronics"
    Home_Decor = "Home Decor"
    Clothing = "Clothing"
    Toys = "Toys"
    Sports = "Sports"
    Appliances = "Appliances"


def user_find(self, query):
    searchList = []
    findUser = self.users_collection.find({}, projection={"_id": False})
    userList = [x for x in findUser]
    for item in userList:
        if re.search(query, item.get("username"), re.IGNORECASE):
            searchList.append(item)
    return searchList



    # user_val is an enum of UserVal
    def update_user(self, userID, user_val, new_val):
        pass

    # auction_val is an enum of AuctionVal
    def update_auction(self, auctionID, auction_val, new_val):
        pass



class UserVal(Enum):  # Editable User Values
    Username = "username"
    Email = "email"
    Password = "hashed_password"  # Should be changed based on how we store passwords
    ProfilePicture = "profile_pic"
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