from flask import Flask, jsonify, request, make_response
from database import *
from flask_sock import Sock
from login import *
from json import loads as json_loads

app = Flask(__name__)
db = Database()
sock = Sock(app)


@app.route("/landing_page_items")
def landing_page_items():
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


@app.post("/login-user")
def loginUser():
    email = request.form['email']
    password = request.form['password']
    print(email, password)
    if not verifyLogin(email, password):
        print('false')
        # return False
    authToken = setBrowserCookie(email)
    myResponse = make_response('Response')
    myResponse.headers['Set-Cookie'] = f'authenticationToken={authToken}; HttpOnly'
    myResponse.headers['Location'] = '/'
    myResponse.headers['X-Content-Type-Options'] = 'nosniff'
    myResponse.status_code = 301
    myResponse.mimetype = 'text/html; charset=utf-8'
    myResponse.content_length = '0'
    return myResponse
