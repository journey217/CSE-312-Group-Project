# Hashing Algorithms
from database import *
import bcrypt
from hashlib import sha256
from base64 import b64encode
from secrets import randbits

db = Database()


# This function will check the database upon login to ensure that the entered email is linked to an account.
def check_email_exists(email):
    if db.find_user_by_email(email):
        return True
    return False


def check_username_exists(username):
    if db.find_user_by_username(username):
        return True
    return False


def check_password(stored_hash, pass_attempt):
    return bcrypt.checkpw(long_password_hash(pass_attempt), stored_hash)


def verify_password(email, password):
    user = db.find_user_by_email(email)
    hashed_password = user['hashed_password']
    return check_password(hashed_password, password)


def verify_login(email, password):
    if not check_email_exists(email):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Email Verification")
        return False
    if not verify_password(email, password):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Password Verification")
        return False
    return True


def set_browser_cookie(email):
    authToken = str(randbits(80))
    encToken = generated_token_hash(authToken)
    db.users_collection.update_one({"email": email}, {"$set": {"token": encToken}})
    return authToken


def generated_token_hash(token):
    return sha256(token.encode()).hexdigest()


def generate_hashed_pass(user_password):
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(long_password_hash(user_password), salt)
    return hashed_pass


def long_password_hash(password):
    return b64encode(sha256(password.encode()).digest())


# In a future revision, function should return error messages in some way. That's why its written badly
def strong_password_check(password):
    errors = []
    if len(password) < 8:
        errors.append("Needs to be at least 8 characters")
    if password.lower() == password:
        errors.append("Needs an Uppercase letter")
    if password.upper() == password:
        errors.append("Needs a Lowercase letter")
    if not any([x.isdigit() for x in password]):
        errors.append("Needs at least 1 Number")
    if password.isalnum():
        errors.append("Needs at least 1 special character")
    return errors
