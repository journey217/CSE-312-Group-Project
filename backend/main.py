from flask import Flask, render_template
from Database import Database, DBType, UserVal, AuctionVal
from password import check_login, generate_hashed_pass
import app

if __name__ == '__main__':
    db = Database()
    app.app.run(debug=True)