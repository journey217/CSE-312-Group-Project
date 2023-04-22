from login import check_password, generate_hashed_pass, strong_password_check


def test_password():
    p1 = generate_hashed_pass("ABcd1234$s")
    p2 = generate_hashed_pass("goodPa$$word2023"*20)
    p3 = generate_hashed_pass("ABcd1234$s")
    assert check_password(p1, "ABcd1234$s")
    assert not check_password(p1, "ABcd1234$s2")
    assert check_password(p2, "goodPa$$word2023"*20)
    assert not check_password(p2, "goodPa$$word2023"*20 + "$")
    assert p1 != p3

    p4 = strong_password_check("!234567A")  # Lower
    p5 = strong_password_check("!234567a")  # Upper
    p6 = strong_password_check("123456aA")  # Special
    p7 = strong_password_check("!2345Aa")  # Count
    p8 = strong_password_check("Ab!defgh")  # digit

    assert p4 == ["Needs a Lowercase letter"]
    assert p5 == ["Needs an Uppercase letter"]
    assert p6 == ["Needs at least 1 special character"]
    assert p7 == ["Needs to be at least 8 characters"]
    assert p8 == ["Needs at least 1 Number"]


if __name__ == "__main__":
    test_password()
    print('done')
