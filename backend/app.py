from flask import Flask, jsonify, request, make_response, send_from_directory, redirect
from database import Database, AuctionVal, UserVal, DBType
from flask_sock import Sock
from login import verify_login, set_browser_cookie, generate_hashed_pass, verify_email, verify_username
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = Database()
sock = Sock(app)


@app.route("/landing_page_items")
def landing_page_items():
    return jsonify(db.landing_page_items())


@app.route("/item/<auction_id>")
def route_item(auction_id):
    item = db.find_by_ID(auction_id, DBType.Auction)
    if item:
        return item


@app.route("/image/<filename>")
def image(filename):
    return send_from_directory('images', filename)


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


@app.post("/add-item")
def add_item():
    try:
        item_name = request.form['Item_Name']
        starting_price = request.form['Item_Price']
        item_desc = request.form['Item_Desc']
        condition = request.form['condition']
        end_date = request.form['date']
        image = request.files['file']
    except KeyError as x:
        # Return an error message pop up telling the user that they didn't completely fill out the form
        print("Add Item Key Error!")
        # return False
    try:
        cookieToken = request.cookies.get('authenticationToken')
    except KeyError as x:
        # Return an error message pop up telling the user that they're not signed in
        print("User is not logged in!")
        # return False
    user = db.find_user_by_token(cookieToken)
    if not user:
        # Return an error message pop up telling the user that their auth token is invalid and that they
        # must log out and log back in
        print("User token is invalid!")
        # return False
    if db.auctions_collection.count_documents({}) == 0:
        x = 1
    else:
        x = int(db.auctions_collection.count_documents({})) + 1
    filename = f'image{x}.jpg'
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.add_auction_to_db(user.get('ID'), item_name, item_desc, image.name, end_date, starting_price, condition)
    return redirect('/')


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
