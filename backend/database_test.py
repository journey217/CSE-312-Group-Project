from database import *
from password import check_login, generate_hashed_pass, PasswordError


def fill_with_data():
    db = Database()
    db.users_collection.delete_many({})
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("pA$ssword5")
    p3 = generate_hashed_pass("goodPa$$word2023")
    db.add_user_to_db(username="Vandorlot",
                      name="Volodymyr Semenov",
                      email="ubcodingprojects@gmail.com",
                      hashed_password=p1,
                      bio="UB2025")
    db.add_user_to_db(username="AAron",
                      name="Aaron Rodgers",
                      email="aaron.rodgers@gmail.com",
                      hashed_password=p2,
                      bio="Jets")
    db.add_user_to_db(username="JHurts",
                      name="Jalen Hurts",
                      email="jalen.hurts@gmail.com",
                      hashed_password=p3,
                      bio="Eagles",
                      profile_pic="blank.jpeg")


def test_password():
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("goodPa$$word2023"*20)
    p3 = generate_hashed_pass("ABcd1234$s")
    assert check_login(p1, "ABcd1234$s")
    assert not check_login(p1, "ABcd1234$s2")
    assert check_login(p2, "goodPa$$word2023"*20)
    assert not check_login(p2, "goodPa$$word2023"*20 + "$")
    assert p1 != p3

    p4 = generate_hashed_pass("!234567A")  # Lower
    p5 = generate_hashed_pass("!234567a")  # Upper
    p6 = generate_hashed_pass("123456aA")  # Special
    p7 = generate_hashed_pass("!2345Aa")  # Count
    p8 = generate_hashed_pass("!A1c!A1c")  # Weak
    p9 = generate_hashed_pass("Ab!defgh")  # digit

    assert p4 == "Needs at least 1 Uppercase, 1 Lowercase"
    assert p5 == "Needs at least 1 Uppercase, 1 Lowercase"
    assert p6 == "Needs at least 1 special character"
    assert p7 == "Needs to be at least 8 characters"
    assert p8 == "Too Simple"
    assert p9 == "Needs at least 1 Number"


if __name__ == "__main__":
    fill_with_data()
    test_password()
    print('done')
