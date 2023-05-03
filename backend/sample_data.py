from login import generate_hashed_pass
from database import *
from datetime import datetime, timedelta, timezone


def fill_with_data():
    db = Database()
    db.users_collection.delete_many({})
    db.auctions_collection.delete_many({})
    db.image_collection.delete_many({})
    db.bids_collection.delete_many({})
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("pA$ssword5")
    p3 = generate_hashed_pass("goodPa$$word2023")
    user_1 = db.add_user_to_db(username="Vandorlot",
                               email="ubcodingprojects@gmail.com",
                               hashed_password=p1)
    user_2 = db.add_user_to_db(username="AAron",
                               email="aaron.rodgers@gmail.com",
                               hashed_password=p2)
    user_3 = db.add_user_to_db(username="JHurts",
                               email="jalen.hurts@gmail.com",
                               hashed_password=p3)
    db.add_auction_to_db(creatorID=user_1.get('ID'),
                         name="Jersey",
                         desc="Gameworn Jersey",
                         image_name="jersey.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(hours=5),
                         price=500,
                         condition="Brand New")
    db.add_auction_to_db(creatorID=user_1.get('ID'),
                         name="Journey's 1 minute Auction",
                         desc="going, going, gone.",
                         image_name="fakeimage.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(seconds=20),
                         price=500,
                         condition="Brand New")
    db.add_auction_to_db(creatorID=user_1.get('ID'),
                         name="Jersey",
                         desc="Gameworn Jersey",
                         image_name="jersey.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(hours=5),
                         price=500,
                         condition="Brand New")
    db.add_auction_to_db(creatorID=user_1.get('ID'),
                         name="Jersey",
                         desc="Gameworn Jersey",
                         image_name="jersey.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(hours=5),
                         price=500,
                         condition="Brand New")
    db.add_auction_to_db(creatorID=user_2.get('ID'),
                         name="Hat",
                         desc="Old_hat",
                         image_name="hat.png",
                         end_time=datetime.now(timezone.utc) + timedelta(hours=1),
                         price=30,
                         condition="Brand New"
                         )
    db.add_auction_to_db(creatorID=user_2.get('ID'),
                         name="Scarf",
                         desc="Old_Scarf",
                         image_name="NoImage.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(days=3),
                         price=20,
                         condition="Brand New"
                         )
    db.add_auction_to_db(creatorID=user_2.get('ID'),
                         name="Neckalce",
                         desc="Neckalce",
                         image_name="fakeimage.jpg",
                         end_time=datetime.now(timezone.utc) + timedelta(minutes=10),
                         price=200,
                         condition="Brand New"
                         )
    db.add_image('jersey.jpg')
    db.add_image('hat.png')


if __name__ == "__main__":
    fill_with_data()
    print('done')
