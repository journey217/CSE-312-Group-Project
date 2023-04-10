from backend.app import auctions_collection, users_collection
import re
import random
from datetime import datetime


def allItemSearch():
    find_items = auctions_collection.find({}, projection={"_id": False})
    items_list = [x for x in find_items]
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
    findUser = users_collection.find({}, projection={"_id": False})
    userList = [x for x in findUser]
    for item in userList:
        if re.search(query, item.get("username"), re.IGNORECASE):
            searchList.append(item)
    return searchList


def randomItemOrder():
    find_items = auctions_collection.find({"end_time": {"$gt": datetime.utcnow()}}, {}, projection={"_id": False})
    items_list = [x for x in find_items]
    random.shuffle(items_list)
    return items_list
