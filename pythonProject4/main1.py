import csv
import os
import random
import time

import requests
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     "Привет, ты написал мне /start или /help. "
                     "Используй /todos для получения рандомного задания.\n"
                     "Мои задачи: \n"
                     "/my_todos - список моих задач")


@bot.message_handler(commands=['todos'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/todos/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        todos = response.json()
        idx = todos['id']
        title = todos['title']
        userid = todos['userId']

        telegram_user_id = message.from_user.id

        if bool(todos['completed']):
            completed = 'Выполнено'
        else:
            completed = 'Не выполнено'
        bot.send_message(message.chat.id, f"Задача: {todos['title']}\nСтатус: {completed}")
        with open(f'todos_{telegram_user_id}.csv', 'a', newline='',  encoding='utf-8') as file:
            fieldnames = ['id', 'Заголовок', 'Пользователь', 'Статус', 'Время']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()

            named_tuple = time.localtime()
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

            writer.writerow({
                'id': idx,
                'Заголовок': title,
                'Пользователь': userid,
                'Статус': completed,
                'Время': time_string
            })
    else:
        bot.send_message(message.chat.id, "Задача не найдена.")


@bot.message_handler(commands=['my_todos'])
def handler_my_todos(message):
    user_id = message.from_user.id
    try:
        with open(f'todos_{user_id}.csv', newline='',encoding='utf=8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bot.send_message(message.chat.id,
                                 f"ID: {row['id']}\n"
                                 f"Заголовок: {row['Заголовок']}\n"
                                 f"Пользователь: {row['Пользователь']}\n"
                                 f"Статус: {row['Статус']}\n"
                                 f"Время: {row['Время']}"
                                 )
    except FileNotFoundError:
         bot.send_message(message.chat.id, "У вас нет сохраненных задач.")


bot.polling(none_stop=True)