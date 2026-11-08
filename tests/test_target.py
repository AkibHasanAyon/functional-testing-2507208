"""Comprehensive functional test suite for all 16 functions in target.py.

Tests cover: valid inputs, boundary values, invalid values, wrong types,
result type checks, and precise assertions to catch hidden faulty versions.
"""

# --- INTENTIONAL FAILING TEST FOR RED CI RUN ---
def test_intentional_fail():
    """This test is intentionally wrong to demonstrate a red CI run."""
    from target import is_adult
    assert is_adult(18) is False  # Wrong! 18 is adult → should be True
# --- END INTENTIONAL FAIL ---

import pytest
import math
from target import (
    is_adult,
    celsius_to_fahrenheit,
    count_vowels,
    invert,
    greet,
    find_max,
    get_price,
    swap,
    common_items,
    is_leap_year,
    to_int,
    divide,
    power,
    square_root,
    factorial,
    average,
)


# ---------------------------------------------------------------------------
# 1. is_adult(age) — True if age >= 18, negative raises ValueError
# ---------------------------------------------------------------------------
class TestIsAdult:
    @pytest.mark.parametrize("age, expected", [
        (18, True),       # boundary: exactly 18
        (19, True),       # just above boundary
        (100, True),      # large age
        (17, False),      # just below boundary
        (0, False),       # zero
        (1, False),       # small positive
    ])
    def test_valid_inputs(self, age, expected):
        assert is_adult(age) is expected

    @pytest.mark.parametrize("age", [-1, -100])
    def test_negative_age_raises(self, age):
        with pytest.raises(ValueError, match="age cannot be negative"):
            is_adult(age)


# ---------------------------------------------------------------------------
# 2. celsius_to_fahrenheit(celsius) — rounded to 2 decimals
# ---------------------------------------------------------------------------
class TestCelsiusToFahrenheit:
    @pytest.mark.parametrize("celsius, expected", [
        (0, 32.0),          # freezing point
        (100, 212.0),       # boiling point
        (-40, -40.0),       # same in both scales
        (37, 98.6),         # body temperature
        (-273.15, -459.67), # absolute zero
        (0.5, 32.9),        # fractional input
    ])
    def test_valid_conversions(self, celsius, expected):
        result = celsius_to_fahrenheit(celsius)
        assert result == pytest.approx(expected, abs=0.01)

    def test_return_type_is_float_or_int(self):
        result = celsius_to_fahrenheit(0)
        assert isinstance(result, (int, float))

    def test_rounding_to_two_decimals(self):
        # 1/3 celsius should produce a value rounded to 2 decimals
        result = celsius_to_fahrenheit(1 / 3)
        # 1/3 * 9/5 + 32 = 32.6
        assert result == round(1 / 3 * 9 / 5 + 32, 2)


# ---------------------------------------------------------------------------
# 3. count_vowels(text) — count a,e,i,o,u case-insensitive, non-str → TypeError
# ---------------------------------------------------------------------------
class TestCountVowels:
    @pytest.mark.parametrize("text, expected", [
        ("hello", 2),         # e, o
        ("HELLO", 2),         # case insensitive
        ("aeiou", 5),         # all vowels lower
        ("AEIOU", 5),         # all vowels upper
        ("xyz", 0),           # no vowels
        ("", 0),              # empty string
        ("a", 1),             # single vowel
        ("b", 0),             # single consonant
        ("AeIoU", 5),         # mixed case vowels
        ("rhythm", 0),        # word with no vowels
        ("Beautiful", 5),     # b-e-a-u-t-i-f-u-l → e,a,u,i,u = 5
    ])
    def test_valid_inputs(self, text, expected):
        assert count_vowels(text) == expected

    @pytest.mark.parametrize("invalid_input", [123, None, 45.6, [], True])
    def test_non_string_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError, match="text must be a string"):
            count_vowels(invalid_input)


# ---------------------------------------------------------------------------
# 4. invert(flag) — return not flag, non-bool → TypeError
# ---------------------------------------------------------------------------
class TestInvert:
    def test_invert_true(self):
        assert invert(True) is False

    def test_invert_false(self):
        assert invert(False) is True

    @pytest.mark.parametrize("invalid_input", [0, 1, "true", "false", None, [], 0.0])
    def test_non_bool_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError, match="flag must be True or False"):
            invert(invalid_input)

    def test_return_type_is_bool(self):
        assert isinstance(invert(True), bool)
        assert isinstance(invert(False), bool)


# ---------------------------------------------------------------------------
# 5. greet(name) — "Hello, <name>!" or "Hello, Guest!" for None/empty/spaces
# ---------------------------------------------------------------------------
class TestGreet:
    @pytest.mark.parametrize("name, expected", [
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        (" Bob ", "Hello, Bob!"),          # strips whitespace
        ("  Alice  ", "Hello, Alice!"),     # strips whitespace
    ])
    def test_valid_names(self, name, expected):
        assert greet(name) == expected

    @pytest.mark.parametrize("name", [None, "", "   ", "  "])
    def test_guest_fallback(self, name):
        assert greet(name) == "Hello, Guest!"

    def test_no_argument_defaults_to_guest(self):
        assert greet() == "Hello, Guest!"


# ---------------------------------------------------------------------------
# 6. find_max(numbers) — largest number, empty → ValueError
# ---------------------------------------------------------------------------
class TestFindMax:
    @pytest.mark.parametrize("numbers, expected", [
        ([1, 2, 3], 3),
        ([3, 2, 1], 3),
        ([-1, -2, -3], -1),          # all negative
        ([5], 5),                     # single element
        ([0, 0, 0], 0),              # all same
        ([1, 1, 2, 2], 2),           # duplicates
        ([-10, 0, 10], 10),          # mixed signs
        ([1.5, 2.5, 0.5], 2.5),     # floats
    ])
    def test_valid_inputs(self, numbers, expected):
        assert find_max(numbers) == expected

    def test_empty_list_raises_value_error(self):
        with pytest.raises(ValueError, match="list is empty"):
            find_max([])


# ---------------------------------------------------------------------------
# 7. get_price(prices, item) — return price, missing → KeyError
# ---------------------------------------------------------------------------
class TestGetPrice:
    def test_existing_item(self):
        prices = {"apple": 1.50, "banana": 0.75}
        assert get_price(prices, "apple") == 1.50

    def test_zero_price(self):
        assert get_price({"free": 0}, "free") == 0

    def test_missing_item_raises_key_error(self):
        prices = {"apple": 1.50}
        with pytest.raises(KeyError, match="banana not found"):
            get_price(prices, "banana")

    def test_empty_dict_raises_key_error(self):
        with pytest.raises(KeyError, match="anything not found"):
            get_price({}, "anything")


# ---------------------------------------------------------------------------
# 8. swap(pair) — swap two values, not exactly 2 → ValueError
# ---------------------------------------------------------------------------
class TestSwap:
    @pytest.mark.parametrize("pair, expected", [
        ((1, 2), (2, 1)),
        (("a", "b"), ("b", "a")),
        ((True, False), (False, True)),
        ((1, 1), (1, 1)),               # same values
        ((0, None), (None, 0)),          # mixed types
        ([10, 20], (20, 10)),            # list input (has len, is indexable)
    ])
    def test_valid_swaps(self, pair, expected):
        result = swap(pair)
        assert result == expected
        assert isinstance(result, tuple)

    @pytest.mark.parametrize("invalid_pair", [
        (1,),       # too few
        (),         # empty
        (1, 2, 3),  # too many
        [1],        # list with 1
        [1, 2, 3],  # list with 3
    ])
    def test_invalid_length_raises_value_error(self, invalid_pair):
        with pytest.raises(ValueError, match="pair must have exactly 2 values"):
            swap(invalid_pair)


# ---------------------------------------------------------------------------
# 9. common_items(set_a, set_b) — intersection of two sets
# ---------------------------------------------------------------------------
class TestCommonItems:
    @pytest.mark.parametrize("set_a, set_b, expected", [
        ({1, 2, 3}, {2, 3, 4}, {2, 3}),       # partial overlap
        ({1, 2}, {3, 4}, set()),                # no overlap
        (set(), set(), set()),                   # both empty
        ({1, 2, 3}, set(), set()),               # one empty
        ({1, 2, 3}, {1, 2, 3}, {1, 2, 3}),     # identical
        ({"a", "b"}, {"b", "c"}, {"b"}),        # strings
    ])
    def test_common_items(self, set_a, set_b, expected):
        result = common_items(set_a, set_b)
        assert result == expected
        assert isinstance(result, set)


# ---------------------------------------------------------------------------
# 10. is_leap_year(year) — leap year logic, year < 1 → ValueError
# ---------------------------------------------------------------------------
class TestIsLeapYear:
    @pytest.mark.parametrize("year, expected", [
        (2024, True),       # divisible by 4, not by 100
        (2000, True),       # divisible by 400
        (1900, False),      # divisible by 100, not by 400
        (2023, False),      # not divisible by 4
        (4, True),          # small leap year
        (1, False),         # boundary: smallest valid year
        (100, False),       # century non-leap
        (400, True),        # century leap
        (800, True),        # another century leap
        (1600, True),       # divisible by 400
        (1700, False),      # divisible by 100, not 400
        (1800, False),      # divisible by 100, not 400
        (2100, False),      # future century non-leap
    ])
    def test_leap_year_logic(self, year, expected):
        assert is_leap_year(year) is expected

    @pytest.mark.parametrize("year", [0, -1, -100])
    def test_year_below_one_raises(self, year):
        with pytest.raises(ValueError, match="year must be 1 or more"):
            is_leap_year(year)


# ---------------------------------------------------------------------------
# 11. to_int(value) — convert to int, bool → TypeError
# ---------------------------------------------------------------------------
class TestToInt:
    @pytest.mark.parametrize("value, expected", [
        ("42", 42),
        ("0", 0),
        ("-5", -5),
        (3.9, 3),        # truncates float
        (0.0, 0),
        (-2.7, -2),      # truncates toward zero
        (10, 10),         # int stays int
        (0, 0),
    ])
    def test_valid_conversions(self, value, expected):
        result = to_int(value)
        assert result == expected
        assert isinstance(result, int)

    @pytest.mark.parametrize("bool_val", [True, False])
    def test_bool_raises_type_error(self, bool_val):
        with pytest.raises(TypeError, match="bool is not allowed"):
            to_int(bool_val)

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            to_int("abc")


# ---------------------------------------------------------------------------
# 12. divide(a, b) — a / b, b=0 → ZeroDivisionError
# ---------------------------------------------------------------------------
class TestDivide:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (-6, 3, -2.0),
        (0, 5, 0.0),
        (1, 3, 1 / 3),          # repeating decimal
        (-10, -2, 5.0),         # both negative
        (100, 10, 10.0),
    ])
    def test_valid_divisions(self, a, b, expected):
        assert divide(a, b) == pytest.approx(expected)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
            divide(10, 0)

    def test_zero_divided_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
            divide(0, 0)


# ---------------------------------------------------------------------------
# 13. power(base, exponent) — base ** exponent
# ---------------------------------------------------------------------------
class TestPower:
    @pytest.mark.parametrize("base, exponent, expected", [
        (2, 3, 8),
        (2, 0, 1),           # anything^0 = 1
        (0, 0, 1),           # 0^0 = 1 in Python
        (0, 5, 0),           # 0^positive = 0
        (2, -1, 0.5),        # negative exponent
        (5, 1, 5),           # anything^1 = itself
        (-2, 3, -8),         # negative base, odd exponent
        (-2, 2, 4),          # negative base, even exponent
        (10, 3, 1000),
        (1, 100, 1),         # 1^anything = 1
    ])
    def test_valid_powers(self, base, exponent, expected):
        assert power(base, exponent) == pytest.approx(expected)


# ---------------------------------------------------------------------------
# 14. square_root(x) — math.sqrt(x), x < 0 → ValueError
# ---------------------------------------------------------------------------
class TestSquareRoot:
    @pytest.mark.parametrize("x, expected", [
        (4, 2.0),
        (0, 0.0),
        (1, 1.0),
        (9, 3.0),
        (2, math.sqrt(2)),      # irrational — use approx
        (0.25, 0.5),
        (100, 10.0),
        (10000, 100.0),
    ])
    def test_valid_inputs(self, x, expected):
        assert square_root(x) == pytest.approx(expected)

    @pytest.mark.parametrize("x", [-1, -100, -0.001])
    def test_negative_raises_value_error(self, x):
        with pytest.raises(
            ValueError,
            match="cannot take the square root of a negative number"
        ):
            square_root(x)


# ---------------------------------------------------------------------------
# 15. factorial(n) — n!, negative → ValueError
# ---------------------------------------------------------------------------
class TestFactorial:
    @pytest.mark.parametrize("n, expected", [
        (0, 1),       # 0! = 1 (critical edge case)
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
    ])
    def test_valid_factorials(self, n, expected):
        assert factorial(n) == expected

    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_negative_raises_value_error(self, n):
        with pytest.raises(
            ValueError,
            match="factorial is not defined for negative numbers"
        ):
            factorial(n)

    def test_return_type_is_int(self):
        assert isinstance(factorial(5), int)


# ---------------------------------------------------------------------------
# 16. average(numbers) — mean of list, empty → ValueError
# ---------------------------------------------------------------------------
class TestAverage:
    @pytest.mark.parametrize("numbers, expected", [
        ([1, 2, 3], 2.0),
        ([10], 10.0),               # single element
        ([0, 0, 0], 0.0),           # all zeros
        ([-1, 1], 0.0),             # cancel out
        ([1, 2, 3, 4, 5], 3.0),
        ([1.5, 2.5], 2.0),          # floats
        ([-10, -20, -30], -20.0),   # all negative
    ])
    def test_valid_averages(self, numbers, expected):
        assert average(numbers) == pytest.approx(expected)

    def test_empty_list_raises_value_error(self):
        with pytest.raises(ValueError, match="list is empty"):
            average([])
