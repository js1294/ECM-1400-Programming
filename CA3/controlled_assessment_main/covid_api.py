"""This is the covid api. It will take the most recent
 covid cases and deaths from the uk government's covid api
  and return it to news.txt. This can be configured with config.json."""
import logging
import json
import sys
import requests

try:
    from weather_api import get_config
except ImportError:
    logging.fatal("ImportError: unable to get weather_api.")


def average(data: list, get: str) -> int:
    """This calculates the mean or average for a list."""
    try:
        total = 0
        for value in data:
            total += value.get(get)
        mean = total / len(data)
        return round(mean)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()
    except AttributeError:
        logging.fatal("AttributeError: object has not attribute 'get'.")
        sys.exit()


def update_covid():
    """This will use the covid19 uk api to return covid data to the covid.txt file."""
    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    config_file = get_config()  # gets the config file used to store api keys, options, etc

    area = config_file["Location"].get("country")
    covid_options = config_file["Covid"]  # options about what to display from the api

    base_url = """https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation;areaName="""
    endpoint = base_url + area + """&structure={"date":"date",\
    "newCasesByPublishDate":"newCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate",\
    "newDeathsByDeathDate":"newDeathsByDeathDate","cumDeathsByDeathDate":"cumDeathsByDeathDate"}"""
    response = requests.get(endpoint, timeout=10)
    # an error has occurred when the status code is greater than 400
    if response.status_code >= 400:
        logging.fatal("RuntimeError: the request failed with the code %s", response.text)
        sys.exit()
    try:
        covid_json = response.json()
        data = covid_json["data"]
    except AttributeError:
        logging.fatal("AttributeError: the object has no json attribute.")
        sys.exit()
    except KeyError:
        logging.fatal("KeyError: unable to create a json file.")
        sys.exit()
    except json.decoder.JSONDecodeError:
        logging.fatal("JSONDecodeError: unable to decode file.")
        sys.exit()
    covid = "In " + area + ""

    if covid_options.get("daily") == "True":  # stores yesterdays cases / deaths
        covid += "\nYesterday, the number of new cases was " \
                 + str(data[0].get("newCasesByPublishDate"))
        if covid_options.get("deaths") == "True":  # stores deaths in general,
            # using the day before yesterday due to them not being available for yesterday
            covid += " and the number of new deaths was " \
                     + str(data[1].get("newDeathsByDeathDate"))
            if covid_options.get("cumulative") == "True":
                covid += "\nThe number of cumulative deaths are " \
                         + str(data[1].get("cumDeathsByDeathDate"))
        if covid_options.get("cumulative") == "True":  # store cumulative deaths / cases
            covid += "\nThe number of cumulative cases are " \
                     + str(data[0].get("cumCasesByPublishDate"))
    if covid_options.get("weekly") == "True":  # stores a weekly average of cases / deaths
        weekly_cases = str(average(data[0:6], "newCasesByPublishDate"))
        covid += "\nThe weekly average number of new cases was " + weekly_cases
        if covid_options.get("deaths") == "True":
            weekly_deaths = str(average(data[1:7], "newDeathsByDeathDate"))
            covid += "\nThe weekly average number of new deaths was " + weekly_deaths
    if covid_options.get("monthly") == "True":  # stores a monthly average of cases / deaths
        monthly_cases = str(average(data[0:29], "newCasesByPublishDate"))
        covid += "\nThe monthly average number of new cases was " + monthly_cases
        if covid_options.get("deaths") == "True":
            monthly_deaths = str(average(data[1:30], "newDeathsByDeathDate"))
            covid += "\nThe monthly average number of new deaths was " + monthly_deaths

    covid_file = open("covid.txt", "w")
    covid_file.write(covid)  # writes the covid-api data to the file covid.txt
    covid_file.close()


def get_covid() -> str:
    """This will return a string containing everything in the covid.txt file."""
    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        covid_file = open("covid.txt", "r")
    except FileNotFoundError:
        logging.fatal(
            "FileNotFoundError: weather.txt file not found."
            " Check if the weather.txt file is in the main folder.")
        sys.exit()
    covid = ""
    for line in covid_file:
        covid += line
    return covid
