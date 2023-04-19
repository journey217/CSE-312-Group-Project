from flask import Flask, jsonify, request, make_response
from database import Database, AuctionVal, UserVal, DBType, Categories
from flask_sock import Sock
from login import verify_login, set_browser_cookie, generate_hashed_pass, verify_email, verify_username
from json import loads as json_loads

app = Flask(__name__)
db = Database()
sock = Sock(app)


@app.route("/landing_page_items")
def landing_page_items():
    return jsonify(db.landing_page_items())


@app.route("/item/<auction_id>")
def route_item(auction_id):
    item = db.find_by_ID(auction_id, DBType.Auction)
    if item:
        return dict(item)


@sock.route("/item/<auction_id>")
def makeWebsocketConnection(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@app.post("/login-user")
def login_user():
    email = request.form['email']
    password = request.form['password']
    print(email, password)
    if not verify_login(email, password):
        print('false')
        # return False

    authToken = set_browser_cookie(email)
    return redirect_response('/', [['authenticationToken', authToken]])


@app.post("/register-user")
def register_user():
    username = request.form['username']
    if verify_username(username):
        # Return message that username is already taken
        return False
    email = request.form['email']
    if verify_email(email):
        # Return message that email is already registered with another account
        return False
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 != password2:
        print('different passwords')

    hash = generate_hashed_pass(password1)
    db.add_user_to_db(username, email, hash)

    authToken = set_browser_cookie(email)
    return redirect_response('/', [['authenticationToken', authToken]])


def redirect_response(path, cookies):
    myResponse = make_response('Response')
    for cookie in cookies:
        myResponse.set_cookie(key=cookie[0], value=cookie[1], max_age=3600, httponly=True)
    myResponse.headers['Location'] = path
    myResponse.headers['X-Content-Type-Options'] = 'nosniff'
    myResponse.status_code = 302
    myResponse.mimetype = 'text/html; charset=utf-8'
    myResponse.content_length = '0'
    return myResponse
