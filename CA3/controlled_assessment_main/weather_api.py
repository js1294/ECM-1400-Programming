"""This is the weather api.
It will take data from open weather maps and return it to the weather.txt file.
This can be configured using the config.json."""
import json
import logging
import sys
from datetime import datetime
import requests


def get_config():
    """This will get the config.json file."""
    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        file.close()
    except FileNotFoundError:
        logging.fatal(
            "FileNotFoundError: config.json file not found"
            ". Check the config.json file is in the main folder.")
        sys.exit()
    except json.decoder.JSONDecodeError:
        logging.fatal(
            "JSONDecodeError: the config file has been"
            " formatted incorrectly and should be re-downloaded.", )
        sys.exit()
    return config


def millibars_to_standard_atmospheres(millibars: int) -> float:
    """This will convert millibars or hpa to standardized atmospheres."""
    try:
        standard_atmospheres = millibars / 1013
        return round(standard_atmospheres, 2)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def pressure_to_words(millibars: int) -> str:
    """This will convert millibars to an easy to understand word like high pressure."""
    try:
        if millibars <= 1000:
            pressure_word = "low"
        elif millibars >= 1026:
            pressure_word = "high"
        else:
            pressure_word = "neutral"
        return pressure_word
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def kilometre_to_mile(kilometre: float) -> float:
    """This will convert kilometres to miles."""
    try:
        mile = kilometre / 1.609
        return round(mile, 2)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def kelvin_to_celsius(kelvin: float) -> float:
    """This will convert kelvin into celsius."""
    try:
        celsius = kelvin - 273.15
        return round(celsius, 2)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """This will convert kelvin into fahrenheit."""
    try:
        fahrenheit = (kelvin_to_celsius(kelvin) * 9 / 5) + 32
        return round(fahrenheit, 2)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def temperature_units(temperature: float, units: dict) -> str:
    """This will handle what units is being used and what to convert them to."""
    try:
        if units.get("temperature").title() == "Celsius":
            temperature = str(kelvin_to_celsius(temperature)) + " degrees celsius."
        elif units.get("temperature").title() == "Fahrenheit":
            temperature = str(kelvin_to_fahrenheit(temperature)) + " degrees fahrenheit."
        elif units.get("temperature").title() == "Kelvin":
            temperature = str(temperature) + " kelvin."
        return temperature
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()
    except AttributeError:
        logging.fatal("AttributeError: object has not attribute 'get'.")
        sys.exit()


def metres_per_second_to_knots(metres_per_second: float) -> float:
    """This will convert metres per second in knots, useful for wind speed."""
    try:
        knots = metres_per_second * 1.944
        return round(knots, 2)
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def beaufort_scale(metres_per_second: float) -> str:
    """This will convert a wind speed in metres per
     second into a description based off the beaufort scale."""
    try:
        if 0 <= metres_per_second < 0.5:
            scale = "calm."
        elif 0.5 <= metres_per_second < 1.5:
            scale = "light air."
        elif 1.5 <= metres_per_second < 3.3:
            scale = "light breeze."
        elif 3.3 <= metres_per_second < 5.5:
            scale = "gentle breeze."
        elif 5.5 <= metres_per_second < 7.9:
            scale = "moderate breeze."
        elif 7.9 <= metres_per_second < 10.7:
            scale = "fresh breeze."
        elif 10.7 <= metres_per_second < 13.8:
            scale = "strong breeze."
        elif 13.8 <= metres_per_second < 17.1:
            scale = "moderate gale. Warning strong winds."
        elif 17.1 <= metres_per_second < 20.7:
            scale = "gale. Warning strong winds."
        elif metres_per_second >= 20.7:
            scale = "strong gale. Warning strong winds."
        else:
            logging.error("Invalid value for beaufort scale.")
            scale = "error"
        return scale
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def compass_directions(direction: int):
    """This is used to convert a direction in degrees to a compass direction."""
    if (315 < direction <= 360) or (0 <= direction < 45):
        direction_word = "north"
    elif 45 <= direction < 135:
        direction_word = "east"
    elif 135 <= direction < 225:
        direction_word = "south"
    elif 225 <= direction < 315:
        direction_word = "west"
    else:
        logging.error("Invalid direction for compass direction.")
        direction_word = "error"
    return direction_word


def get_temperature(weather_options: dict, main: dict, units: dict) -> str:
    """This will get temperature based information
     from the dictionaries and return them to weather."""
    weather = ""
    temperature = str(weather_options.get("temperature"))
    if temperature.title() == "True":
        temperature = main.get("temp")
        temperature = temperature_units(temperature, units)
        weather += "\nThe temperature is: " + temperature
    elif temperature.title() != "False":
        logging.warning("Invalid value for temperature in"
                        " options of config.json. Should only be True or False.")

    feel = str(weather_options.get("feel"))
    if feel.title() == "True":
        feel = main.get("feels_like")
        feel = temperature_units(feel, units)
        weather += "\nThe real feel temperature is: " + feel
    elif feel.title() != "False":
        logging.warning("Invalid value for real feel"
                        " temperature in options of config.json."
                        " Should only be True or False.")

    maximum = str(weather_options.get("max"))
    if maximum.title() == "True":
        max_temperature = main.get("temp_max")
        max_temperature = temperature_units(max_temperature, units)
        weather += "\nThe max temperature today is: " + max_temperature
    elif maximum.title() != "False":
        logging.warning("Invalid value for max temperature in options of config.json."
                        " Should only be True or False.")

    minimum = weather_options.get("min")
    if minimum.title() == "True":
        min_temperature = main.get("temp_min")
        min_temperature = temperature_units(min_temperature, units)
        weather += "\nThe min temperature today is: " + min_temperature
    elif minimum.title() != "False":
        logging.warning("Invalid value for min temperature in options"
                        " of config.json. Should only be True or False.")
    return weather


def get_wind(weather_options: dict, weather_json: dict, units: dict) -> str:
    """This will get wind based information
     from the dictionaries and return them to weather."""
    weather = ""
    wind = str(weather_options.get("wind"))
    if wind.title() == "True":
        wind = weather_json.get("wind")
        wind_speed = wind.get("speed")
        wind_beaufort = beaufort_scale(wind_speed)
        wind_direction = compass_directions(wind.get("deg"))
        if units.get("wind").title() == "Metre Per Second":
            wind_speed = str(wind_speed) + " metres per second."
        elif units.get("wind").title() == "Knot":
            wind_speed = str(metres_per_second_to_knots(wind_speed)) + " knots."
        else:
            wind_speed = str(wind_speed) + " metres per second."
            logging.error("Invalid unit for wind speed."
                          " Metres per second being used as default.")
        weather += "\nThe wind speed is: " + wind_speed
        weather += "\nThe wind conditions are " + wind_beaufort
        weather += "\nThe wind direction is " + wind_direction
    elif wind.title() != "False":
        logging.warning("Invalid value for wind in options of config.json."
                        " Should only be True or False.")
    return weather


def get_visibility(weather_options: dict, weather_json: dict, units: dict) -> str:
    """This will get visibility based information
     from the dictionaries and return them to weather."""
    weather = ""
    visibility = weather_options.get("visibility")
    if visibility.title() == "True":
        visibility = weather_json.get("visibility")
        visibility_unit = str(units.get("distance"))
        if visibility_unit.title() == "Kilometre":
            visibility = str(visibility) + " kilometres."
        elif visibility_unit.title() == "Miles":
            visibility = str(kilometre_to_mile(visibility)) + " miles."
        else:
            visibility = str(visibility) + " kilometres."
            logging.error("Invalid unit for distance. Kilometres being used as default.")
        weather += "\nThe visibility is: " + visibility
    elif visibility.title() != "False":
        logging.warning("Invalid value for visibility in options of config.json."
                        " Should only be True or False.")
    return weather


def get_pressure(weather_options: dict, main: dict, units: dict) -> str:
    """This will get pressure based information
     from the dictionaries and return them to weather."""
    weather = ""
    pressure = weather_options.get("pressure")
    if pressure.title() == "True":
        pressure = main.get("pressure")
        pressure_words = pressure_to_words(pressure)
        pressure_unit = str(units.get("pressure"))
        if pressure_unit.title() == "Standard Atmosphere":
            pressure = str(millibars_to_standard_atmospheres(pressure)) + " standard atmospheres."
        elif pressure_unit.title() == "Millibar":
            pressure = str(pressure) + " millibars."
        else:
            pressure = str(pressure) + " millibars."
            logging.error("Invalid unit for pressure. Millibar being used as default.")
        weather += "\nThe pressure is: " + pressure
        weather += "\nThe pressure conditions are " + pressure_words + "."
    elif pressure.title() != "False":
        logging.warning("Invalid value for pressure in options of config.json."
                        " Should only be True or False.")
    return weather


def get_sunset_sunrise(weather_options: dict, weather_json: dict) -> str:
    """This will get the sunrise and sunset times
     from the dictionaries and return them to weather."""
    weather = ""
    sunrise_sunset = str(weather_options.get("sunrise_sunset"))
    if sunrise_sunset.title() == "True":
        system = weather_json["sys"]
        sunrise = system.get("sunrise")
        sunrise = str(datetime.fromtimestamp(sunrise))
        sunrise = sunrise.split(" ")
        sunset = system.get("sunset")
        sunset = str(datetime.fromtimestamp(sunset))
        sunset = sunset.split(" ")
        weather += "\nSunrise is at: " + sunrise[1] + "."
        weather += "\nSunset is at: " + sunset[1] + "."
    elif sunrise_sunset.title() != "False":
        logging.warning("Invalid value for sunrise and sunset in options of config.json."
                        " Should only be True or False.")
    return weather


def get_humidity(weather_options: dict, main: dict) -> str:
    """This will get humidity percentage
     from the dictionaries and return them to weather."""
    weather = ""
    humidity = str(weather_options.get("humidity"))
    if humidity.title() == "True":
        humidity = main.get("humidity")
        weather += "\nThe humidity is: " + str(humidity) + "%."
    elif humidity.title() != "False":
        logging.warning("Invalid value for humidity in options of config.json."
                        " Should only be True or False.")
    return weather


def get_description(weather_options: dict, weather_json: dict) -> str:
    """This will get the description of the weather
     from the dictionaries and return them to weather."""
    weather = ""
    description = weather_options.get("description")
    if description.title() == "True":
        description = weather_json["weather"]
        description = description[0].get("main")
        weather += "\nThe weather condition are currently " + description + "."
    elif description.title() != "False":
        logging.warning("Invalid value for description in options of config.json."
                        " Should only be True or False.")
    return weather


def get_coordinates(weather_options: dict, weather_json: dict) -> str:
    """This will get the coordinates of the weather station
     from the dictionaries and return them to weather."""
    weather = ""
    coordinates = str(weather_options.get("coordinates"))
    if coordinates.title() == "True":
        coordinates = weather_json["coord"]
        weather += " at the coordinates - longitude: " + str(coordinates.get("lon")) + \
                   " latitude: " + str(coordinates.get("lat")) + "."
    elif coordinates.title() != "False":
        logging.warning("Invalid value for coordinates in"
                        " options of config.json. Should only be True or False.")
    return weather


def update_weather():
    """This will update the weather.txt file with the
     most recent weather in the location specified in the config file.
    The details displayed can be changed in the config file and
     so can the units used."""

    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    config_file = get_config()  # gets the config file used to store api keys, options, etc

    api_key = str(config_file["API-keys"].get("weather"))
    # api-key, a personal api-key will be required to be put into config.json
    if api_key == "":
        logging.fatal("Missing Api-key for the weather."
                      " Please put your personal api key in the config.json file.")
        sys.exit()
    city = str(config_file["Location"].get("city"))
    weather_options = config_file["Weather"]  # options about what to display from the api
    units = config_file["Units"]  # the different units for things like distance and wind speed

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    try:
        data = requests.get(complete_url)
    except requests.exceptions.MissingSchema:
        logging.fatal("MissingSchema: invalid URL.")
        sys.exit()
    try:
        weather_json = data.json()
        main = weather_json["main"]
    except AttributeError:
        logging.fatal("AttributeError: the object has no json attribute.")
        sys.exit()
    except KeyError:
        logging.fatal("KeyError: unable to create a json file.")
        sys.exit()

    weather = "In " + city + "," + get_coordinates(weather_options, weather_json) \
              + get_temperature(weather_options, main, units) \
              + get_description(weather_options, weather_json) \
              + get_wind(weather_options, weather_json, units) \
              + get_visibility(weather_options, weather_json, units) \
              + get_pressure(weather_options, main, units) \
              + get_humidity(weather_options, main) \
              + get_sunset_sunrise(weather_options, weather_json)

    weather_file = open("weather.txt", "w")
    weather_file.write(weather)  # writes the weather-api data to the file covid.txt
    weather_file.close()


def get_weather() -> str:
    """This will return a string containing everything in the weather.txt file."""
    logging.basicConfig(filename="log.txt", format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        weather_file = open("weather.txt", "r")
    except FileNotFoundError:
        logging.fatal(
            "FileNotFoundError: weather.txt file not found."
            " Check if the weather.txt file is in the main folder.")
        sys.exit()
    weather = ""
    for line in weather_file:
        weather += line
    return weather
