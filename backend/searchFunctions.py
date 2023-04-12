from backend.app import auctions_collection, users_collection
import re


def all_item_search():
    find_items = auctions_collection.find({}, projection={"_id": False})
    items_list = [x for x in find_items]
    return items_list


def item_find(query):
    search_list = []
    items_list = all_item_search()
    for item in items_list:
        # The 're' library is used to find if a string contains a given substring while ignoring case
        if re.search(query, item.get("name"), re.IGNORECASE):
            search_list.append(item)
    return search_list


def user_find(query):
    searchList = []
    findUser = users_collection.find({}, projection={"_id": False})
    userList = [x for x in findUser]
    for item in userList:
        if re.search(query, item.get("username"), re.IGNORECASE):
            searchList.append(item)
    return searchList
