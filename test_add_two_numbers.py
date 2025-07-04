from testing.add_two_numbers import add_numbers

def test_add_positive_integers():
    assert add_numbers(2, 3) == 5

def test_add_negative_integers():
    assert add_numbers(-4, -6) == -10

def test_add_positive_and_negative():
    assert add_numbers(7, -2) == 5

def test_add_zeros():
    assert add_numbers(0, 0) == 0

def test_add_floats():
    assert add_numbers(2.5, 3.1) == 5.6

def test_add_int_and_float():
    assert add_numbers(5, 2.5) == 7.5

def test_add_large_numbers():
    assert add_numbers(1_000_000, 2_000_000) == 3_000_000