import hashlib

import bcrypt
from pymongo import MongoClient
from database import *

db = Database()


# This function will check the database upon login to ensure that the entered email is linked to an account.
def verifyEmail(email):
    if db.find_user_by_email(email):
        return True
    return False


def comparePasswords(email, password):
    user = dict(db.find_user_by_email(email))
    userSalt = user['salt']
    userPass = user['hashed_password']
    attemptedPass = (bcrypt.hashpw(password.encode(), userSalt.encode())).decode()
    if attemptedPass != userPass:
        # Return an error message indicating that the entered password is incorrect/not registered
        return False
    return True


def verifyLogin(email, password):
    if not verifyEmail(email):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Email Verification")
        return False
    if not comparePasswords(email, password):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Password Verification")
        return False
    return True


def setBrowserCookie(email):
    authToken = (bcrypt.gensalt()).decode()
    encToken = hashlib.sha256(authToken.encode()).hexdigest()
    db.users_collection.update_one({"email": email}, {"$set": {"token": encToken}})
    return authToken

