import telebot
import sqlite3;
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
import json
import Defs

bot = telebot.TeleBot(os.getenv("token"))

@bot.message_handler(commands=['start','back'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Начать")
    markup.add(item1)
    bot.send_message(message.chat.id,"ae",reply_markup=markup)
@bot.message_handler(content_types='text')
def main(message):
    if message.text=="Начать":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("Парсить обсуждения")
        item2=types.KeyboardButton("Парсить руководства")
        item3=types.KeyboardButton("Изменить список")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        id = message.from_user.id
        ug = (id, 218620)
        con = sqlite3.connect("users_games.db")
        print(ug) #remove after tests
        cursor = con.cursor()
        cursor.execute("INSERT INTO Users_games (user_id, user_game) VALUES (?, ?)",ug)
        con.commit()
        bot.send_message(message.chat.id,"What do i do lord?",reply_markup=markup)
    disc_parse(message)
    guides_parse(message)
    list_change(message)

def disc_parse(message):
    if message.text=="Парсить обсуждения":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Первая страница обсуждений")
        item2=types.KeyboardButton("Обсуждения с фильтром")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно парсить обсуждения?",reply_markup=markup)
    disc_parser_wof(message)

def guides_parse(message):
    if message.text=="Парсить руководства":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Без фильтров")
        item2=types.KeyboardButton("С фильтром")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно парсить руководства?",reply_markup=markup)
    guides_parser_wof(message)

def list_change(message):
    if message.text=="Изменить список":
        markup = types.InlineKeyboardMarkup()
        item1=types.InlineKeyboardButton("Добавить",callback_data="list_add")
        item2=types.InlineKeyboardButton("Удалить",callback_data="list_remove")
        item3=types.InlineKeyboardButton("Редактировать", callback_data="list_replace")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id,"Как именно изменить список?",reply_markup=markup)

def disc_parser_wof(message):
    if message.text=="Первая страница обсуждений":
        bot.send_message(message.from_user.id,Defs.disc_page_turner(1))

def guides_parser_wof(message):
    if message.text=="Без фильтров":
        bot.send_message(message.from_user.id,Defs.guides_page_turner(1))
bot.infinity_polling()