# Hashing Algorithms
import bcrypt
from hashlib import sha256
from base64 import b64encode


def check_login(stored_pass, pass_attempt):
    return bcrypt.checkpw(long_password_hash(pass_attempt), stored_pass)


def generate_hashed_pass(user_password):
    if not valid_password(user_password):
        return None
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(long_password_hash(user_password), salt)
    return hashed_pass


def long_password_hash(password):
    return b64encode(sha256(password.encode()).digest())


# In a future revision, function should return error messages in some way. That's why its written badly
def valid_password(password):
    if password == "password":
        return False
    # At least 8 characters
    if len(password) < 8:
        return False
    # At least 1 Uppercase and 1 Lower and 1 Digit
    if password.islower() or password.isupper() or password.isalpha():
        return False
    # Special Character Test
    if password.isalnum():
        return False
    # At least 4 Unique Characters "aabbccdd" would work "aabbccaa" would not
    # Error Message can be too simple of a password
    unique_characters = set()
    for i in range(len(password)):
        unique_characters.add(password[i])
    if len(unique_characters) < 4:
        return False
    return True

    # Should make unit tests
    # hashed_pass = password.generate_hashed_pass("@pasSword1"*1000)
    # print(password.check_login(hashed_pass, "@pasSword1"*1000))             #  -> Should be True
    # print(password.check_login(hashed_pass, "@pasSword1" * 1000 + '$'))     #  -> Should be False