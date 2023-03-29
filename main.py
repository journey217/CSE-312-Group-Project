from flask import Flask, render_template
from Database import Database, DBType, UserVal, AuctionVal
from password import check_login, generate_hashed_pass


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


if __name__ == '__main__':
    db = Database()
    app.run(debug=True)

