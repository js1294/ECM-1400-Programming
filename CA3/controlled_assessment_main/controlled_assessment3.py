"""This is the controlled_assessment_main main file."""
import sched
import time
import calendar
import logging
import sys
from datetime import datetime
from pyttsx3 import speak
from flask import request, render_template, Flask, redirect
import jinja2

# Done to catch any missing python files
try:
    from covid_api import get_covid, update_covid
except ImportError:
    logging.fatal("ImportError: unable to get covid_api.")
try:
    from weather_api import get_weather, update_weather, get_config
except ImportError:
    logging.fatal("ImportError: unable to get weather_api.")
try:
    from news_api import get_news, update_news
except ImportError:
    logging.fatal("ImportError: unable to get news_api.")

# The two schedules: one for the alarms and another to schedule when to update the api's.
alarm_schedule = sched.scheduler(time.time, time.sleep)
api_schedule = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)


def date_time_to_seconds(date_time: str) -> float:
    """This will take a data and time and convert this into a unix timestamp."""
    try:
        year, month, date_time = date_time.split("-")
        days, date_time = date_time.split("T")
        hour, minutes = date_time.split(":")
        date_time = (int(year), int(month), int(days), int(hour), int(minutes), 0)
        date_time = calendar.timegm(date_time)
        return date_time
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def bool_to_on_off(boolean: bool) -> str:
    """This converts a boolean value into a string, on or off."""
    try:
        if boolean is True:
            result = "on"
        elif boolean is False:
            result = "off"
        else:
            logging.error("ValueError: the variable boolean is not a bool.")
            result = "error"
        return result
    except ValueError:
        logging.fatal("ValueError: invalid input in function.")
        sys.exit()


def display_alarm() -> list:
    """This is will return formatted alarms so they can be displayed."""
    alarm = []
    for event in alarm_schedule.queue:
        alarm_name = event[3][0]
        alarm_date_time = event[3][1]
        alarm_news = event[3][2]
        alarm_weather = event[3][3]

        date, times = alarm_date_time.split("T")
        content = "Date - " + date + ", Time - " + times + ", News - " + bool_to_on_off(
            alarm_news) + ", Weather - " + bool_to_on_off(alarm_weather)
        alarm_name = "Alarm Title - " + alarm_name
        alarm.append({"title": alarm_name, "content": content})
    return alarm


def alarm_announcement(alarm_name: str, alarm_date_time: str, alarm_news: str, alarm_weather: str):
    """This will announce the alarm when it is scheduled to go off."""
    logging.info("Alarm completed: the alarm called %s has been has gone off, it was due for %s.",
                 alarm_name, alarm_date_time)
    speak("Alarm" + alarm_name)
    covid = get_covid()
    speak(covid)
    if alarm_news is True:
        news = get_news()
        speak(news)
    if alarm_weather is True:
        weather = get_weather()
        speak(weather)


def add_notification(notification_name: str, content: str):
    """This will add a new notification."""
    try:
        notification.append({"title": notification_name, "content": content})
    except ValueError:
        logging.error("ValueError: Unable to add notification")


def cancel_notification(notification_name: str):
    """This is used to cancel notifications."""
    try:
        for alert in notification:
            if alert.get("title") == notification_name:
                notification.remove(alert)
                break
        logging.warning("Unable to cancel notification as unable to find notification.")
    except ValueError:
        logging.error("ValueError: Unable to cancel notification.")


def add_alarm(alarm_name: str, alarm_date_time: str, alarm_news: bool, alarm_weather: bool):
    """This will add the new alarm to the schedule queue and to the list of alarms."""
    try:
        new_alarm = {"title": alarm_name, "date_time": alarm_date_time, "alarm_news": alarm_news,
                     "alarm_weather": alarm_weather}
        time_set = date_time_to_seconds(alarm_date_time)
        if time_set <= time.time():
            add_notification("Failed to add alarm: " + alarm_name,
                             "The alarm's date and time has already happened.")
            logging.warning("An alarm failed to be added due to being before the current time.")
        else:
            alarm_schedule.enterabs(time=time_set, priority=1,
                                    action=alarm_announcement,
                                    argument=list(new_alarm.values()))
    except ValueError:
        logging.fatal("ValueError: Unable to add alarm.")
        sys.exit()


def cancel_alarm(cancel: str):
    """This is used to cancel an alarm in the schedule."""
    try:
        for event in alarm_schedule.queue:
            alarm_name = event[3][0]
            if "Alarm Title - " + alarm_name == cancel:
                alarm_schedule.cancel(event)
                break
        logging.warning("Unable to cancel alarm as unable to find alarm.")
    except ValueError:
        logging.error("ValueError: Unable to cancel alarm.")


@app.route("/index")
def alarms_notifications():
    """This handles the alarms and the notifications."""
    alarm_date_time = request.args.get("alarm")
    alarm_name = request.args.get("two")
    alarm_news = request.args.get("news")
    alarm_weather = request.args.get("weather")
    cancel_a = request.args.get("alarm_item")
    cancel_n = request.args.get("notif")

    weather = False
    if alarm_weather:
        weather = True

    news = False
    if alarm_news:
        news = True

    if alarm_date_time and alarm_name:  # Adding an alarm
        add_alarm(alarm_name, alarm_date_time, news, weather)
        logging.info("Created alarm: the alarm called [%s] has been created."
                     " It is due to go off at %s", alarm_name, alarm_date_time)
        return redirect("/")
    if cancel_a:  # cancelling an alarm
        cancel_alarm(cancel_a)
        current_time = str(datetime.fromtimestamp(time.time()))
        add_notification("Cancelled alarm:", "The alarm " + str(cancel_a)
                         + " was cancelled at " + str(current_time))
        logging.info("Cancelled alarm: the alarm called [%s] has been cancelled.", cancel_a)
        return redirect("/")
    if cancel_n:  # cancelling a notification
        cancel_notification(cancel_n)
        logging.info("Cancelled notification: the notification"
                     " called %s has been cancelled.", cancel_n)
        return redirect("/")
    return redirect("/")


@app.route('/')
def main():
    """This is the main method handling scheduling of
     updating the api's and the displaying the html page."""
    if len(api_schedule.queue) == 0:
        # when the api schedule is empty,
        # schedule more updates based off the delay set in the config file.
        api_schedule.enter(float(DELAY), 1, update_news)
        api_schedule.enter(float(DELAY), 1, update_weather)
        api_schedule.enter(float(DELAY), 1, update_covid)
        add_notification("Updated api data:", "The news headlines,"
                                              " weather and covid data has been updated.")
        logging.info("Updated api data: The news headlines, weather"
                     " and covid data has been updated.")
    alarm_schedule.run(blocking=False)
    api_schedule.run(blocking=False)
    # run each schedule, blocking is false to allow the rest of the program to continue to run.
    try:
        return render_template("main.html", alarms=display_alarm(), notifications=notification,
                               title="Coronavirus Smart Alarm Clock")
    except jinja2.exceptions.TemplateNotFound:
        logging.fatal("TemplateNotFound: the html file,"
                      " main.html in /templates, is missing.")
        sys.exit()


if __name__ == '__main__':
    notification = []
    logging.basicConfig(filename="log.txt",
                        format="%(levelname)s:%(asctime)s:%(message)s",
                        level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Start of program-\n")

    config_file = get_config()

    update_news()
    update_weather()
    update_covid()

    try:
        DELAY = int(config_file["Delay"])
    except ValueError:
        DELAY = 3600
        logging.error("ValueError: delay not found or invalid type"
                      " was used in config file, default value used.")
    app.run()
