from os import environ
from os.path import join, dirname
import math

from dotenv import load_dotenv
import pendulum
import telebot

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = telebot.TeleBot(environ.get('TELEGRAM_TOKEN'))


def get_year_progress(dt):
    year_days = 366 if dt.is_leap_year() else 365
    passed_days = dt.timetuple().tm_yday
    percent = math.floor((passed_days / year_days) * 100)
    return percent


def get_month_progress(dt):
    days_since_start_of_month = dt.day - 1
    percent = math.floor((days_since_start_of_month / dt.days_in_month) * 100)
    return percent


def get_day_progress(dt):
    percent = math.floor((dt.hour / 24) * 100)
    return percent


def make_progress_string(percent):
    blocks = 16
    percent = percent * blocks / 100
    return ''.join(["▓" if i < percent else "░" for i in range(blocks)])


@bot.message_handler(commands=['start'])
def send__greeting(message):
    text = f'Hi, there! It is nice to see you here, {message.from_user.first_name} !'
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['progress'])
def send_progress(message):
    dt = pendulum.now()

    year_percents = get_year_progress(dt)
    year_progress = make_progress_string(year_percents)

    month_percents = get_month_progress(dt)
    month_progress = make_progress_string(month_percents)

    day_percents = get_day_progress(dt)
    day_progress = make_progress_string(day_percents)

    text = f'Year:      {year_progress} {year_percents}%\n'\
           f'Month:  {month_progress} {month_percents}%\n'\
           f'Day:       {day_progress} {day_percents}%\n'

    bot.send_message(message.chat.id, text=text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
