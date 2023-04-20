from flask import Flask, jsonify, request, make_response, send_from_directory, redirect
from database import Database, AuctionVal, UserVal, DBType
from flask_sock import Sock
from login import verify_login, set_browser_cookie, generate_hashed_pass, verify_email, verify_username, username_exists, email_exists
import os
import re

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
def register():
    # Get form data
    username = request.form['username']
    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']

    # Initialize list to hold error messages
    errors = []

    # Check if passwords match
    if password1 != password2:
        errors.append({'password2':'Passwords do not match'})

    # Check if username already exists
    if username_exists(username):
        errors.append({'username':'Username already exists'})

    # Check if email already exists
    if email_exists(email):
        errors.append({'email':'Email already exists'})

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append({'email':'Invalid email address'})

    # Validate password
    if not re.match(r"^.{8,}$", password1):
        errors.append({'password1':'Password must be at least 8 characters long'})

    # If there are errors, return them as a JSON response
    if errors:
        return jsonify({'errors': errors})
    
    # Submit data to database
    hash = generate_hashed_pass(password1)
    db.add_user_to_db(username, email, hash)
    authToken = set_browser_cookie(email)

    response = make_response(redirect('/'))
    response.set_cookie('authenticationToken', authToken)
    return redirect_response('/', [['authenticationToken', authToken]])


@app.post("/add-item")
def add_item():
    errors = []
    try:
        item_name = request.form['Item_Name']
        starting_price = request.form['Item_Price']
        item_desc = request.form['Item_Desc']
        condition = request.form['condition']
        end_date = request.form['date']
    except KeyError as x:
        errors.append({'field': 'Please fill out all fields before submitting!'})
        return jsonify({'errors': errors})
    try:
        cookieToken = request.cookies.get('authenticationToken')
    except KeyError as x:
        print("User is not logged in!")
        errors.append({'field': 'Please log in before posting an item!'})
        return jsonify({'errors': errors})
    user = db.find_user_by_token(cookieToken)
    if user is None:
        print("User token is invalid!")
        errors.append({'field': 'Invalid log in token. Please sign out and sign back in!'})
        return jsonify({'errors': errors})
    if db.auctions_collection.count_documents({}) == 0:
        x = 1
    else:
        x = int(db.auctions_collection.count_documents({})) + 1
    filename = f'image{x}.jpg'
    image = request.files['image']
    if image:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if user is not None:
        db.add_auction_to_db(creatorID=user.get('ID'), name=item_name, desc=item_desc, image_name=filename, end_time=end_date, price=starting_price, condition=condition)
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
