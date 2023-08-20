import telebot
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
import json

bot = telebot.TeleBot(os.getenv("token"))
#работает, надо перенести на основной проект
@bot.message_handler(commands=['start','back'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('СЫС', callback_data='qs_csc')
    item2 = types.InlineKeyboardButton('SHOSH', callback_data='qs_shosh')
    markup.add(item1,item2)
    bot.send_message(message.chat.id,"What do i do lord?",reply_markup=markup)
@bot.callback_query_handler(func=lambda callback: True)
def csc_or_shosh(callback):
    if callback.data == "qs_csc":
        bot.send_message(callback.message.chat.id, "csc")
    elif callback.data == "qs_shosh":
        bot.send_message(callback.message.chat.id, "shosh")
bot.infinity_polling()



"""
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton('СЫС', callback_data='qs_csc'))
markup.add(types.InlineKeyboardButton('SHOSH', callback_data='qs_shosh'))
bot.send_message(message.chat.id,"What do i do lord?",reply_markup=markup)
"""