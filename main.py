from flask import Flask, render_template
from Database import Database, DBType, UserVal, AuctionVal


app = Flask(__name__)


@app.route('/')
def homepage():  # Naming convention can be changed
    return render_template('index.html')


if __name__ == '__main__':
    db = Database()
    app.run(debug=True)
