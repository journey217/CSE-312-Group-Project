import time
from flask import Flask, jsonify, request, make_response, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import Database, DBType
from login import verify_login, set_browser_cookie, generate_hashed_pass, check_email_exists, check_username_exists, strong_password_check
import os
import re
from datetime import datetime, timezone
from uuid import uuid4, UUID
import html

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = Database()
origins = "*"

# initialize your socket instance
socketio = SocketIO(app, namespace="item", cors_allowed_origins=origins)


@app.route("/myUsername")
def username():
    cookieToken = request.cookies.get('authenticationToken')
    user = db.find_user_by_token(cookieToken)
    if user:
        return {'status': 1, 'username': user.get('username')}
    else:
        return {'status': 0}


@app.route("/landing_page_items")
def landing_page_items():
    db.end_auctions()
    return jsonify(db.landing_page_items())


@app.route('/sign-out')
def sign_out():
    response = make_response('Response')
    response.set_cookie('authenticationToken', '', max_age=0,
                        httponly=True, samesite='Strict')
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
    print("\nPrint user: ")
    print(user)
    if user:
        output['username'] = user['username']
        output['email'] = user['email']
        output['profile_pic'] = user['profile_pic']
        # Auction
        output['auctionHistory'] = db.profile_page_auctions(user['ID'])
        # Bid history
        output['bidHistory'] = db.profile_page_bids(user['ID'])
        print("\nPrint output: ")
        print(output)
        return jsonify({'status': 1, 'user': output})
    else:
        return jsonify({'status': 0})


@app.route("/item/<auction_id>")
def route_item(auction_id):
    if not valid_uuid(auction_id):
        return jsonify({'error': 1})
    auction_id = UUID(auction_id)
    item = db.find_by_ID(auction_id, DBType.Auction)
    if not item:
        return jsonify({'error': 1})
    bid_history = [db.find_by_ID(x, DBType.Bid) for x in item['bid_history']]
    item['bid_history'] = bid_history
    auth_token = request.cookies.get('authenticationToken')
    user = db.find_user_by_token(auth_token)
    if user:
        xsrf_token_find = user.get('xsrf', '')
    else:
        xsrf_token_find = ''
    vendor = db.find_by_ID(item['creatorID'], DBType.User).get(
        'username', 'Error: Vendor not Found')
    return jsonify({'error': 0, 'item': item, 'user': auth_token, 'xsrf_token': xsrf_token_find, 'username': vendor})


@socketio.on('connect', namespace="/item")
def handle_connect():
    print('Client connected')


@socketio.on('disconnect', namespace="/item")
def handle_disconnect():
    print('Client disconnected')


@socketio.on('message', namespace="/item")
def handle_message(msg):
    if msg['type'] == 'bid':
        token = msg['token']
        if not token:
            emit("error", "You must be logged in to place bids.")
            return False
        token = UUID(token)
        user = db.find_user_by_token(msg['user'])
        if not user:
            emit("error", "You must be logged in to place bids.")
            return False
        authenticate = db.users_collection.find_one(
            {'username': user['username'], 'xsrf': token})
        if not authenticate:
            emit("error", "Invalid XSRF token. Please sign-out and sign back in.")
            return False
        auction_ID = msg['auctionID']
        price = msg['price']
        price = html.escape(price)
        room = msg['room']
        if user:
            new_bid = db.add_bid_to_db(user['ID'], UUID(auction_ID), price)
            if not new_bid:
                emit(
                    'error', "Submitted bid is not larger than highest bid! Or Auction Expired")
            else:
                emit('message', {
                     "username": user['username'], "bid_price": msg['price'], "auction_id": auction_ID}, room=room)
        else:
            emit("error", "You must be logged in to place bids.")


@socketio.on('join', namespace='/item')
def enter_room(msg):
    room = msg['room']
    join_room(room)
    emit(f'Connected to room: {room}', room=room)


@socketio.on('leave', namespace='/item')
def exit_room(msg):
    room = msg['room']
    leave_room(room)
    emit(f'Left room: {room}', broadcast=True)


@socketio.on('end_auction', namespace='/item')
def end_auction(msg):
    auction_id = msg['auction_id']
    db.end_auctions()
    time.sleep(1)
    item_winner = dict(db.auctions_collection.find_one(
        {"ID": UUID(auction_id)}))['winner']
    winner = db.find_user_by_ID(item_winner).get('username')
    emit(
        f"Auction: {auction_id} has ended. {winner} is the winner!", broadcast=True)
    emit("winner", {"winner": winner}, room=auction_id)


@app.route("/image/<filename>")
def image(filename):
    if db.image_exists(filename):
        return send_from_directory('images', filename)
    return send_from_directory('images', 'NoImage.jpg')


@app.post("/login-user")
def login_user():
    email = request.form['email']
    email = html.escape(email)
    password = request.form['password']
    if verify_login(email, password):
        authToken = set_browser_cookie(email)
        response_data = {'status': '1', 'authenticationToken': authToken}
        response = jsonify(response_data)
        response.set_cookie('authenticationToken', authToken,
                            max_age=3600, httponly=True, samesite='Strict')
        return response
    else:
        response_data = {'status': '0',
                         'error': 'Incorrect Username or Password'}
        response = jsonify(response_data)
        return response


@app.post("/register-user")
def register():
    # Get form data
    username = request.form['username']
    username = html.escape(username)
    email = request.form['email']
    email = html.escape(email)
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

    image = request.files['image']
    hash_ = generate_hashed_pass(password1)
    if not image:
        # set image to default image if no image was submitted
        db.add_user_to_db(username, email, hash_)

    else:
        filename = f'image{str(uuid4())}.jpg'
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Submit data to database
        db.add_image(filename)
        db.add_user_to_db(username, email, hash_, profile_pic=filename)

    authToken = set_browser_cookie(email)

    # print(authToken)
    response_data = {'status': '1', 'authenticationToken': authToken}
    response = jsonify(response_data)
    response.set_cookie('authenticationToken', authToken,
                        max_age=3600, httponly=True, samesite='Strict')
    return response


@app.post("/add-item")
def add_item():
    cookieToken = request.cookies.get('authenticationToken')
    if not cookieToken:
        return jsonify({'status': 0, 'field': 'Please log in before posting an item!'})

    user = db.find_user_by_token(cookieToken)
    if user is None:
        return jsonify({'status': 0, 'field': 'Invalid session token. Please sign out and sign back in!'})

    item_name = request.form.get('Item_Name')
    item_name = html.escape(item_name)
    starting_price = request.form.get('Item_Price')
    starting_price = html.escape(starting_price)
    item_desc = request.form.get('Item_Desc')
    item_desc = html.escape(item_desc)
    condition = request.form.get('condition')
    condition = html.escape(condition)
    end_date = request.form.get('date')
    end_date = html.escape(end_date)
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


def valid_uuid(uuid_string):
    pattern = re.compile(
        r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$")
    return pattern.match(uuid_string)
