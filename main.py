import datetime
import logging

import telebot

import config
import first_week
import second_week

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start", "starts"])
def welcomeMessage(message):
    bot.send_message(message.chat.id, text="Вітаю, плебеє " + str(message.from_user.first_name))
    detect_current_lesson(message)


first_week_of_fortnight = {
    "Monday": first_week.monday,
    "Tuesday": first_week.tuesday,
    "Wednesday": first_week.wednesday,
    "Thursday": first_week.thursday,
    "Friday": first_week.friday,
    "Saturday": first_week.saturday,
    "Sunday": first_week.sunday
}

second_week_of_fortnight = {
    "Monday": second_week.monday,
    "Tuesday": second_week.tuesday,
    "Wednesday": second_week.wednesday,
    "Thursday": second_week.thursday,
    "Friday": second_week.friday,
    "Saturday": second_week.saturday,
    "Sunday": second_week.sunday
}


def current_lesson_number():
    # string representation of the current time with : separator
    # for instance 13:24
    time_separator = datetime.datetime.now().strftime("%H" + ":" + "%M")
    # devide data into tho parts: hours and minutes - and conver them to int
    # for instance h = 13 and m = 24
    h, m = map(int, time_separator.split(":"))
    time = datetime.time(h, m)

    # check intervals and return the number of lesson
    if datetime.time(8, 20) < time < datetime.time(10, 5):
        return 1
    if datetime.time(10, 15) < time < datetime.time(12, 0):
        return 2
    if datetime.time(12, 10) < time < datetime.time(13, 55):
        return 3
    if datetime.time(14, 5) < time < datetime.time(15, 50):
        return 4


def set_current_week():
    # datetime.date.isocalendar() is an instance-method returning
    # a tuple containing year, weeknumber and weekday in respective order for the given date instance.
    # we get week number and check current week, deviding by 2
    week_number = datetime.datetime.now().isocalendar()[1]
    # select the current week as the first or second part of fortnight
    current_week = first_week_of_fortnight if (week_number % 2 == 1) else second_week_of_fortnight
    return current_week


def get_today_lessons():
    current_week = set_current_week()
    # string representation of today
    # for instance Monday
    today = datetime.datetime.today().strftime('%A')
    # dict of today's lessons, where key = lesson number
    today_lessons = current_week[today]
    return today_lessons


@bot.message_handler(commands=["les", "td", "all"])
def send_today_lessons(message):
    today_lessons = get_today_lessons()
    sentence = ""
    for k in today_lessons:
        string = str(k) + " : " + str(today_lessons[k])
        index = string.find("h")
        string = string[:index]
        sentence += string + "\n"
    bot.send_message(message.chat.id, text=sentence)


@bot.message_handler(commands=["qq"])
def detect_current_lesson(message):
    today_lessons = get_today_lessons()
    bot.send_message(message.chat.id, text=today_lessons.get(current_lesson_number(), "Наразі пари немає"))


@bot.message_handler(commands=["time"])
def send_time(message):
    text = (
    "8:30 - 10:05\n"
    "10:25 - 12:00\n"
    "12:20 - 13:55\n"
    "14:15 - 15:50"
    )

    bot.send_message(message.chat.id, text=text)


bot.polling(none_stop=True)
