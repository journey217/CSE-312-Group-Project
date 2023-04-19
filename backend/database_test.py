from login import check_password, generate_hashed_pass, PasswordError


def test_password():
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("goodPa$$word2023"*20)
    p3 = generate_hashed_pass("ABcd1234$s")
    assert check_password(p1, "ABcd1234$s")
    assert not check_password(p1, "ABcd1234$s2")
    assert check_password(p2, "goodPa$$word2023"*20)
    assert not check_password(p2, "goodPa$$word2023"*20 + "$")
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
    test_password()
    print('done')
