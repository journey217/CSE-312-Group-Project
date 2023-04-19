# Hashing Algorithms
from database import *
import bcrypt
from hashlib import sha256
from base64 import b64encode
from enum import Enum


db = Database()


# Class holding different password Errors
class PasswordError(Enum):
    pass


# This function will check the database upon login to ensure that the entered email is linked to an account.
def verifyEmail(email):
    if db.find_user_by_email(email):
        return True
    return False


def verifyPassword(email, password):
    user = db.find_user_by_email(email)
    hashed_password = user['hashed_password']
    return check_password(hashed_password, password)


def check_password(stored_hash, pass_attempt):
    return bcrypt.checkpw(long_password_hash(pass_attempt), stored_hash)


def verifyLogin(email, password):
    if not verifyEmail(email):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Email Verification")
        return False
    if not verifyPassword(email, password):
        # Return an error message indicating that the entered email is incorrect/not registered
        print("Failed Password Verification")
        return False
    return True


def setBrowserCookie(email):
    authToken = (bcrypt.gensalt()).decode()
    encToken = sha256(authToken.encode()).hexdigest()
    db.users_collection.update_one({"email": email}, {"$set": {"token": encToken}})
    return authToken


def generate_hashed_pass(user_password):
    success, reason = password_requirements_check(user_password)
    if not success:
        return reason
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(long_password_hash(user_password), salt)
    return hashed_pass


def long_password_hash(password):
    return b64encode(sha256(password.encode()).digest())


# In a future revision, function should return error messages in some way. That's why its written badly
def password_requirements_check(password):
    # At least 8 characters
    if len(password) < 8:
        return False, "Needs to be at least 8 characters"
    # At least 1 Uppercase and 1 Lower and 1 Digit
    if password.islower() or password.isupper() :
        return False, "Needs at least 1 Uppercase, 1 Lowercase"
    # Special Character Test
    if not any([x.isdigit() for x in password]):
        return False, "Needs at least 1 Number"
    if password.isalnum():
        return False, "Needs at least 1 special character"
    # At least 4 Unique Characters "aabbccdd" would work "aabbccaa" would not
    # Error Message can be too simple of a password
    unique_characters = set()
    for i in range(len(password)):
        unique_characters.add(password[i])
    if len(unique_characters) < 5:
        return False, "Too Simple"
    return True, None
