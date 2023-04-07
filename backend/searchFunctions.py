from backend.app import auctions_collection, users_collection
import re
import random
from datetime import datetime



def allItemSearch():
    items_list = []
    find_items = auctions_collection.find()
    for doc in find_items:
        items_list.append(
            {"ID": doc.get("ID"),
             "creatorID": doc.get("creatorID"),
             "name": doc.get("name"),
             "description": doc.get("description"),
             "category": doc.get("category"),
             "images": doc.get("images"),
             "start_time": doc.get("start_time"),
             "end_time": doc.get("end_time"),
             "bid_history": doc.get("bid_history")}
        )
    return items_list


def itemFind(query):
    search_list = []
    items_list = allItemSearch()
    for item in items_list:
        # The 're' library is used to find if a string contains a given substring while ignoring case
        if re.search(query, item.get("name"), re.IGNORECASE):
            search_list.append(item)
    return search_list


def userFind(query):
    searchList = []
    userList = []
    findUser = users_collection.find()
    for doc in findUser:
        userList.append(
            {"ID": doc.get("ID"),
             "username": doc.get("username"),
             "email": doc.get("email"),
             "profile_pic": doc.get("profile_pic"),
             "bio": doc.get("bio"),
             "name": doc.get("name"),
             "auctions_made": doc.get("auctions_made"),
             "bid_history": doc.get("bid_history")}
        )
    for item in userList:
        if re.search(query, item.get("username"), re.IGNORECASE):
            searchList.append(item)
    return searchList

def randomItemOrder():
    items_list = []
    find_items = auctions_collection.find({"end_time": {"$gt": datetime.utcnow()}})
    for doc in find_items:
        items_list.append(
            {"ID": doc.get("ID"),
             "creatorID": doc.get("creatorID"),
             "name": doc.get("name"),
             "description": doc.get("description"),
             "category": doc.get("category"),
             "images": doc.get("images"),
             "start_time": doc.get("start_time"),
             "end_time": doc.get("end_time"),
             "bid_history": doc.get("bid_history")}
        )
    random.shuffle(items_list)
    return items_list