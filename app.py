from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():  # Naming convention can be changed
    return render_template('index.html')


@app.route('/login')
def login_page():  # Naming convention can be changed
    return render_template('login.html')


@app.route('/register')
def register_page():  # Naming convention can be changed
    return render_template('register.html')