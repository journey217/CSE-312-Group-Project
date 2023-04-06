# Hashing Algorithms
import bcrypt
from hashlib import sha256
from base64 import b64encode
from enum import Enum


class PasswordError(Enum):
    pass


def check_login(stored_pass, pass_attempt):
    return bcrypt.checkpw(long_password_hash(pass_attempt), stored_pass)


def generate_hashed_pass(user_password):
    cond, reason = valid_password(user_password)
    if not cond:
        return reason
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(long_password_hash(user_password), salt)
    return hashed_pass


def long_password_hash(password):
    return b64encode(sha256(password.encode()).digest())


# In a future revision, function should return error messages in some way. That's why its written badly
def valid_password(password):
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

    # Should make unit tests
    # hashed_pass = password.generate_hashed_pass("@pasSword1"*1000)
    # print(password.check_login(hashed_pass, "@pasSword1"*1000))             #  -> Should be True
    # print(password.check_login(hashed_pass, "@pasSword1" * 1000 + '$'))     #  -> Should be False