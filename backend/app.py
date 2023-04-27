from flask import Flask, jsonify, request, make_response, send_from_directory, redirect
from flask_socketio import SocketIO, emit
from database import Database, DBType
from login import verify_login, set_browser_cookie, generate_hashed_pass, check_email_exists, check_username_exists, strong_password_check
import os
import re
from datetime import datetime
from uuid import uuid4, UUID

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = Database()
socketio = SocketIO(app, namespace="/item")

if os.environ.get('FLASK_ENV') == 'production':
    origins = [
        'http://actual-app-url.herokuapp.com',
        'https://actual-app-url.herokuapp.com'
    ]
else:
    origins = "*"

# initialize your socket instance
socketio = SocketIO(cors_allowed_origins=origins)



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
    cookieToken = request.cookies.get('authenticationToken', '')
    user = db.find_user_by_token(cookieToken)
    if user:
        return jsonify({'status': 1, 'user': user})
    else:
        return jsonify({'status': 0})


@app.route("/item/<auction_id>")
def route_item(auction_id):
    auction_id = UUID(auction_id)
    item = db.find_by_ID(auction_id, DBType.Auction)
    if item:
        return jsonify({'item': item})
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
    print(msg)
    emit('received')



@app.route("/users/<user_id>", methods=['GET'])
def get_user_by_id(user_id):
    user_id = UUID(user_id)
    user = db.find_user_by_ID(user_id)
    keys_to_remove = ['hashed_password', 'auctions_made', 'bid_history']
    for key in keys_to_remove:
        user.pop(key, None)
    print(user)
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
    print(email, password)
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
    print(authToken)
    response_data = {'status': '1', 'authenticationToken': authToken}
    response = jsonify(response_data)
    response.set_cookie('authenticationToken', authToken, max_age=3600, httponly=True)
    return response


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
        errors.append(
            {'field': 'Please fill out all fields before submitting!'})
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
        errors.append(
            {'field': 'Invalid log in token. Please sign out and sign back in!'})
        return jsonify({'errors': errors})
    filename = f'image{str(uuid4())}.jpg'
    image = request.files['image']
    if image:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.add_image(filename)
        db.add_auction_to_db(creatorID=user.get('ID'), name=item_name, desc=item_desc, image_name=filename,
                             end_time=datetime.strptime(end_date, '%Y-%m-%dT%H:%M'), price=starting_price, condition=condition)
        return redirect('/')
    else:
        errors.append(
            {'field': 'Please fill out all fields before submitting!'})
        return jsonify({'errors': errors})


def redirect_response(path, cookies):
    myResponse = make_response('Response')
    for cookie in cookies:
        myResponse.set_cookie(
            key=cookie[0], value=cookie[1], max_age=3600, httponly=True)
    myResponse.headers['Location'] = path
    myResponse.headers['X-Content-Type-Options'] = 'nosniff'
    myResponse.status_code = 302
    myResponse.mimetype = 'text/html; charset=utf-8'
    myResponse.content_length = '0'
    return myResponse
