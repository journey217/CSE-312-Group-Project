from flask import Flask
import json
from database import *

app = Flask(__name__)
db = Database()  # In future everything should be changed to this


@app.route("/landing_page_items")
def landing_page_items():  # Naming convention can be changed
    print(db.random_item_order())
    return db.random_item_order()


@app.route("/login")
def login_page():  # Naming convention can be changed
    pass


# There should be data sent to /login with a form submission. This data is then matched to a record in the users
# database before then caching that account to the browser and logging them in.
@app.post("/login")
def cache_account():
    return True


# Requires info from a form submission about what is being changed. Then will go into database and change
# that data.
@app.route("/change-?")
def change():
    return True


@app.route("/profile")
def profile_page():
    # username = "Passed username from cache/browser"
    # user = {}
    # findUser = users_collection.find_one({"username": username})
    # user["ID"] = findUser.get("ID")
    # user["username"] = findUser.get("username")
    # user["email"] = findUser.get("email")
    # user["profile_pic"] = findUser.get("profile_pic")
    # user["bio"] = findUser.get("bio")
    # user["name"] = findUser.get("name")
    # user["auctions_made"] = findUser.get("auctions_made")
    # user["bid_history"] = findUser.get("bid_history")

    # Check the user email from cache
    email = ""
    user = db.find_user_by_email(email)
    return json.dumps(user)


@app.route("/create-auction")
def create_auction_page():
    # Return the blank form page for creating an auction item
    return True


@app.route("/change-auction")
def change_auction():
    # Return the blank form page for changing an auction item
    return True


@app.post("/change-auction")
def change_auction2():
    # Read from the submitted form and use that data to update an auction item.
    # Then update the database
    return True


@app.route("/post-bid")
def post_bid():
    # Reads submitted form for what item the bid is on and then appends that bid to that items bid list
    return True


@app.route("/get-bid")
def get_bid():
    # Returns a bid by ID?
    return True


@app.route("/register")
def register_page():  # Naming convention can be changed
    return
