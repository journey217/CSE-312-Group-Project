from flask import Flask, jsonify
from database import *
from flask_sock import Sock

app = Flask(__name__)
db = Database()  # In future everything should be changed to this
sock = Sock(app)


@app.route("/landing_page_items")
def landing_page_items():  # Naming convention can be changed
    print(db.landing_page_items())
    return jsonify(db.landing_page_items())


@app.route("/item/<auction_id>")
def routeItem(auction_id):
    item = db.find_by_ID(auction_id, DBType.Auction)
    if item:
        return dict(item)


@sock.route("/item/<auction_id>")
def makeWebsocketConnection(ws):
    while True:
        data = ws.receive()
        ws.send(data)
