from flask import Flask, render_template
from pymongo import MongoClient
import json
import Database

app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client["CSE312-Group-Project-Test"]
auctions_collection = db["Auctions"]
users_collection = db["Users"]
bids_collection = db["Bids"]

@app.route('/')
def home_page():  # Naming convention can be changed
    itemsList = []
    findItems = auctions_collection.find()
    for doc in findItems:
        itemsList.append(
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
    return json.dumps(itemsList)


@app.route('/login')
def login_page():  # Naming convention can be changed
    return render_template('login.html')


# There should be data sent to /login with a form submission. This data is then matched to a record in the users
# database before then caching that account to the browser and logging them in.
@app.post('/login')
def cacheAccount():
    return True


# Requires info from a form submission about what is being changed. Then will go into database and change
# that data.
@app.route('/change-?')
def change():
    return True


@app.route("/profile")
def profile_page():
    # Check who the user is from caches
    username = "Passed username from cache/browser"
    user = {}
    findUser = users_collection.find_one({"username": username})
    user["ID"] = findUser.get("ID")
    user["username"] = findUser.get("username")
    user["email"] = findUser.get("email")
    user["profile_pic"] = findUser.get("profile_pic")
    user["bio"] = findUser.get("bio")
    user["name"] = findUser.get("name")
    user["auctions_made"] = findUser.get("auctions_made")
    user["bid_history"] = findUser.get("bid_history")
    return json.dumps(user)


@app.route("/create-auction")
def createAuctionPage():
    # Return the blank form page for creating an auction item
    return True


@app.route("/change-auction")
def changeAuction():
    # Return the blank form page for changing an auction item
    return True


@app.post("/change-auction")
def changeAuction2():
    # Read from the submitted form and use that data to update an auction item.
    itemID = "Item from form"
    updatedAttribute = "Key they would like to change"
    updatedValue = "Value they want to update it with"
    item = {}
    itemFind = auctions_collection.find_one({"ID": itemID})
    item[updatedAttribute] = updatedValue
    # Then update the database
    return True


@app.route("/post-bid")
def postBid():
    # Reads submitted form for what item the bid is on and then appends that bid to that items bid list
    return True


@app.route("/get-bid")
def getBid():
    # Returns a bid by ID?
    return True


@app.route('/register')
def register_page():  # Naming convention can be changed
    return render_template('register.html')
