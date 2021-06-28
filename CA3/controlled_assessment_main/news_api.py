"""This is the news api. It will take the top headlines from the website and return it to news.txt.
This can be configured with config.json."""
import sys
import logging
import requests

try:
    from weather_api import get_config
except ImportError:
    logging.fatal("ImportError: unable to get weather_api.")


def black_listed(black_list: list, article_source: str) -> bool:
    """This will check if an article's source is on the black list or not."""
    try:
        article_source = str.lower(article_source)
        for source in black_list:
            source = str.lower(source)
            if source == article_source:
                return True
        return False
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def word_checker(article_title: str, keyword: str) -> bool:
    """This will check if the keyword is in the article"""
    try:
        keyword = str.lower(keyword)
        for word in article_title.split(" "):
            word = str.lower(word)
            if word == keyword:
                return True
        return False
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def update_news():
    """This will update the news.txt file with the most
     recent news depending on the options in the config file."""
    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p')
    config_file = get_config()  # gets the config file used to store api keys, options, etc

    api_key = config_file["API-keys"].get("news")
    # api-key, a personal api-key will be required to be put into config.json
    if api_key == "":
        logging.fatal("Missing Api-key for the news."
                      " Please put your personal api key in the config.json file.")
        sys.exit()
    country = config_file["Location"].get("countries")
    news = config_file["News"]

    keyword = news.get("keyword")  # a keyword that if found will make that article show up
    black_list = news.get("blacklist")  # black list what sources should never show up
    white_list = news.get("whitelist")
    # white list what sources should always show up regardless of the keyword

    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    try:
        news_dict = requests.get(complete_url)
    except requests.exceptions.MissingSchema:
        logging.fatal("MissingSchema: invalid URL.")
        sys.exit()
    try:
        news_dict = news_dict.json()
        articles = news_dict["articles"]
    except AttributeError:
        logging.fatal("AttributeError: the object has no json attribute.")
        sys.exit()
    except KeyError:
        logging.fatal("KeyError: unable to create a json file.")
        sys.exit()

    news = "The top headlines today are:\n"

    for article in articles:
        article_name = str(article["source"].get("name"))
        if black_listed(black_list, article_name) is False:
            article_title = article["title"]
            if black_listed(white_list, article_name) is True:
                news += "\n" + article_title
            elif (word_checker(article_title, keyword) is True) and (keyword != ""):
                news += "\n" + article_title

    news_file = open("news.txt", "w")
    news_file.write(news)  # writes the weather-api data to the file covid.txt
    news_file.close()


def get_news() -> str:
    """This will return a string containing everything in the news.txt file."""
    try:
        news_file = open("weather.txt", "r")
    except FileNotFoundError:
        logging.fatal("FileNotFoundError: news.txt file not found."
                      " Check if the news.txt file is in the main folder.")
        sys.exit()
    news = ""
    for line in news_file:
        news += line
    return news
