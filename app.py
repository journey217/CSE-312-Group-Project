from flask import Flask, render_template
from pymongo import MongoClient
import json

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

@app.post('/login')


@app.route('/register')
def register_page():  # Naming convention can be changed
    return render_template('register.html')