from password import check_login, generate_hashed_pass, PasswordError
from database import *
from datetime import datetime


def fill_with_data():
    db = Database()
    db.users_collection.delete_many({})
    db.auctions_collection.delete_many({})
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("pA$ssword5")
    p3 = generate_hashed_pass("goodPa$$word2023")
    user_1 = db.add_user_to_db(username="Vandorlot",
                      name="Vlad S",
                      email="ubcodingprojects@gmail.com",
                      hashed_password=p1.decode(),
                      bio="UB2025")
    user_2 = db.add_user_to_db(username="AAron",
                      name="Aaron Rodgers",
                      email="aaron.rodgers@gmail.com",
                      hashed_password=p2.decode(),
                      bio="Jets")
    user_3 = db.add_user_to_db(username="JHurts",
                      name="Jalen Hurts",
                      email="jalen.hurts@gmail.com",
                      hashed_password=p3.decode(),
                      bio="Eagles",
                      profile_pic="blank.jpeg")
    db.add_auction_to_db(creatorID=user_1.get('ID'),
                         name="Jersey",
                         desc="Gameworn Jersey",
                         images="blank.jpeg",
                         category="",
                         end_time=datetime.max)
    db.add_auction_to_db(creatorID=user_2.get('ID'),
                         name="Hat",
                         desc="Old_hat",
                         images="blank.jpeg",
                         category="",
                         end_time=datetime.max)


if __name__ == "__main__":
    fill_with_data()
    print('done')
