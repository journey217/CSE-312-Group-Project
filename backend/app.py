from flask import Flask, jsonify, request, make_response, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import Database, DBType
from login import verify_login, set_browser_cookie, generate_hashed_pass, check_email_exists, check_username_exists, strong_password_check
import os
import re
from datetime import datetime, timezone, date
from uuid import uuid4, UUID
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = Database()
origins = "*"

# initialize your socket instance
socketio = SocketIO(app, namespace="item", cors_allowed_origins=origins)

active_rooms = []


@app.route("/landing_page_items")
def landing_page_items():
    return jsonify(db.landing_page_items())


@app.route('/sign-out')
def sign_out():
    response = make_response('Response')
    response.set_cookie('authenticationToken', '', max_age=0, httponly=True)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.status_code = 200
    response.mimetype = 'text/html; charset=utf-8'
    response.content_length = '0'
    return response


@app.route('/profile')
def profile():
    output = {}
    cookieToken = request.cookies.get('authenticationToken', '')
    user = db.find_user_by_token(cookieToken)
    print(output)
    if user:
        output['username'] = user['username']
        output['email'] = user['email']
        output['profile_pic'] = user['profile_pic']
        # Auction
        output['auctionHistory'] = db.profile_page_auctions(user['ID'])
        # Bid history
        output['bidHistory'] = db.profile_page_bids(user['ID'])
        return jsonify({'status': 1, 'user': output})
    else:
        return jsonify({'status': 0})


@app.route("/item/<auction_id>")
def route_item(auction_id):
    auction_id = UUID(auction_id)
    item = db.find_by_ID(auction_id, DBType.Auction)
    user = request.cookies.get('authenticationToken')
    if item:
        return jsonify({'item': item, 'username': user})
    else:
        return "not found"


@socketio.on('connect', namespace="/item")
def handle_connect():
    print('Client connected')


@socketio.on('disconnect', namespace="/item")
def handle_disconnect():
    print('Client disconnected')


@socketio.on('message', namespace="/item")
def handle_message(msg):
    if msg['type'] == 'bid':
        user = db.find_user_by_token(msg['user'])
        auction_ID = msg['auctionID']
        price = msg['price']
        room = msg['room']
        if user:
            new_bid = db.add_bid_to_db(user['ID'], UUID(auction_ID), price)
            if not new_bid:
                emit("Submitted bid is not larger than highest bid! Or Auction Expired")
            else:
                # print("Added bid to DB")
                emit('message', {"username": user['username'], "bid_price": msg['price'], "auction_id": auction_ID}, room=room)
        else:
            emit("User is not logged in!")


@socketio.on('join', namespace='/item')
def enter_room(msg):
    room = msg['room']
    join_room(room)
    if room not in active_rooms:
        active_rooms.append(room)
    emit(f'Connected to room: {room}', room=room)
    # print("Entered room:", room)


@socketio.on('leave', namespace='/item')
def exit_room(msg):
    room = msg['room']
    print("leaving room:", room)
    leave_room(room)
    emit(f'Left room: {room}', broadcast=True)


@app.route("/users/<user_id>", methods=['GET'])
def get_user_by_id(user_id):
    user_id = UUID(user_id)
    user = db.find_user_by_ID(user_id)
    keys_to_remove = ['hashed_password', 'auctions_made', 'bid_history']
    for key in keys_to_remove:
        user.pop(key, None)
    # print(user)
    if user:
        return jsonify({'user': user})
    else:
        return "not found"


@app.route("/image/<filename>")
def image(filename):
    if db.image_exists(filename):
        return send_from_directory('images', filename)
    return send_from_directory('images', 'NoImage.jpg')


@app.post("/login-user")
def login_user():
    email = request.form['email']
    password = request.form['password']
    # print(email, password)
    if verify_login(email, password):
        authToken = set_browser_cookie(email)
        response_data = {'status': '1', 'authenticationToken': authToken}
        response = jsonify(response_data)
        response.set_cookie('authenticationToken', authToken,
                            max_age=3600, httponly=True)
        return response
    else:
        response_data = {'status': '0',
                         'error': 'Incorrect Username or Password'}
        response = jsonify(response_data)
        return response


@app.route("/myUsername")
def username():
    cookieToken = request.cookies.get('authenticationToken')
    user = db.find_user_by_token(cookieToken)
    if user:
        return {'status': 1, 'username': user.get('username')}
    else:
        return {'status': 0}


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
        errors.append({'password2': 'Passwords do not match'})

    # Check if username already exists
    if check_username_exists(username):
        errors.append({'username': 'Username already exists'})

    # Check if email already exists
    if check_email_exists(email):
        errors.append({'email': 'Email already exists'})

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append({'email': 'Invalid email address'})

    # Validate password
    password_errors = strong_password_check(password1)
    if len(password_errors) != 0:
        errors.append({'password1': '<br>'.join(password_errors)})

    # If there are errors, return them as a JSON response
    if errors:
        return jsonify({'status': '0', 'errors': errors})

    # Submit data to database
    hash_ = generate_hashed_pass(password1)
    db.add_user_to_db(username, email, hash_)
    authToken = set_browser_cookie(email)
    # print(authToken)
    response_data = {'status': '1', 'authenticationToken': authToken}
    response = jsonify(response_data)
    response.set_cookie('authenticationToken', authToken,
                        max_age=3600, httponly=True)
    return response


@app.post("/add-item")
def add_item():
    cookieToken = request.cookies.get('authenticationToken')
    if not cookieToken:
        return jsonify({'status': 0, 'field': 'Please log in before posting an item!'})

    user = db.find_user_by_token(cookieToken)
    if user is None:
        print("User token is invalid!")
        return jsonify({'status': 0, 'field': 'Invalid session token. Please sign out and sign back in!'})

    item_name = request.form.get('Item_Name')
    starting_price = request.form.get('Item_Price')
    item_desc = request.form.get('Item_Desc')
    condition = request.form.get('condition')
    end_date = request.form.get('date')
    try:
        formatted_date = datetime.fromisoformat(end_date)
    except ValueError as x:
        formatted_date = datetime.fromisoformat('2023-06-01T00:05:23+04:00')
    if not (item_name and starting_price and item_desc and condition and end_date):
        return jsonify({'status': 0, 'field': 'Please fill out all fields before submitting!'})

    if formatted_date < datetime.now(timezone.utc):
        return jsonify({'status': 0, 'field': 'Please enter a valid end date!'})

    filename = f'image{str(uuid4())}.jpg'
    image = request.files['image']
    if not image:
        return jsonify({'status': 0, 'field': 'Please add an Image!'})

    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.add_image(filename)
    db.add_auction_to_db(creatorID=user.get('ID'), name=item_name, desc=item_desc, image_name=filename,
                         end_time=formatted_date, price=starting_price, condition=condition)
    return jsonify({'status': 1})
