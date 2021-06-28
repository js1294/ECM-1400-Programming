"""This module is a program used to test controlled_assessment"""
import sys
try:
    from controlled_assessment_main import weather_api as w
except ImportError:
    print("ImportError: unable to get weather_api.")
    sys.exit()

try:
    from controlled_assessment_main import covid_api as c
except ImportError:
    print("ImportError: unable to get covid_api.")
    sys.exit()

try:
    from controlled_assessment_main import news_api as n
except ImportError:
    print("ImportError: unable to get news_api.")
    sys.exit()

try:
    from controlled_assessment_main import controlled_assessment3 as ca3
except ImportError:
    print("ImportError: unable to get controlled_assessment3.")
    sys.exit()


def weather_test(test_int: int, test_float: float, test_str: str):
    """These are tests for the weather api."""
    test_list = [test_str, test_float, test_int]
    tests = [test_int, test_float, test_str, test_list]
    for test in tests:
        assert w.metres_per_second_to_knots(test)
        assert w.pressure_to_words(test)
        assert w.kilometre_to_mile(test)
        assert w.kelvin_to_celsius(test)
        assert w.kelvin_to_fahrenheit(test)
        assert w.temperature_units(test, test)
        assert w.metres_per_second_to_knots(test)
        assert w.beaufort_scale(test)
    assert w.get_config()
    assert w.temperature_units(test_int, "Fahrenheit")
    assert w.update_weather()
    assert w.get_weather()


def covid_test(test_int: int, test_float: float, test_str: str):
    """These are tests for the covid api."""
    test_list = [test_str, test_float, test_int]
    tests = [test_int, test_float, test_str, test_list]
    for test in tests:
        assert c.average(test, test)
    assert c.average(test_list, "newCasesByPublishDate")
    assert c.average([], "newCasesByPublishDate")
    assert c.update_covid()
    assert c.get_covid()


def news_test(test_int: int, test_float: float, test_str: str):
    """These are tests for the news api."""
    test_list = [test_str, test_float, test_int]
    tests = [test_int, test_float, test_str, test_list]
    for test in tests:
        assert n.word_checker(test, test)
        assert n.black_listed(test, test)
    assert n.black_listed([], test_str)
    assert n.update_news()
    assert n.get_news()


def controlled_assessment_test(test_int: int, test_float: float, test_str: str):
    """These are test for the controlled assessment."""
    test_list = [test_str, test_float, test_int]
    tests = [test_int, test_float, test_str, test_list]
    for test in tests:
        assert ca3.date_time_to_seconds(test)
        assert ca3.bool_to_on_off(test)
        assert ca3.add_notification(test, test)
        assert ca3.cancel_alarm(test)
        assert ca3.cancel_notification(test)
    assert ca3.display_alarm()


try:
    weather_test(102, 23.4, "wow")
except AssertionError:
    print("Weather: Assertion Error")

try:
    covid_test(132, 26.4, "wow")
except AssertionError:
    print("Covid: Assertion Error")

try:
    news_test(132, 26.4, "wow")
except AssertionError:
    print("News: Assertion Error")
