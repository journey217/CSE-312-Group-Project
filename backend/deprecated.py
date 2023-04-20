

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
