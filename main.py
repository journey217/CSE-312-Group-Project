from flask import Flask, render_template
from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["CSE312-Group-Project-Test"]
master = db["Testing"]


app = Flask(__name__)


@app.route('/')
def homepage():  # Naming convention can be changed
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
