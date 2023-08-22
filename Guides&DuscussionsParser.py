import telebot
from telebot import types
import sqlite3
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
        User_id = message.from_user.id
        Defs.entry_id_set(User_id)
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
        markup=types.ReplyKeyboardMarkup()
        item1=types.KeyboardButton("Добавить свою игру")
        item2=types.KeyboardButton("Выбрать игру из списка")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно изменить список?",reply_markup=markup)
    set_game_id(message)
    game_list(message)


def disc_parser_wof(message):
    if message.text=="Первая страница обсуждений":
        bot.send_message(message.from_user.id,Defs.disc_page_turner(1))

def guides_parser_wof(message):
    if message.text=="Без фильтров":
        bot.send_message(message.from_user.id,Defs.guides_page_turner(1))

def set_game_id(message):
    if message.text=="Добавить свою игру":
        bot.send_message(message.from_user.id,"Введи Steam ID" )
        bot.register_next_step_handler(message,game_add)


def game_add(message):
    game_id = Defs.check_game_id(message.text)

    if game_id == -1:
        bot.send_message(message.message.from_user.id, "Нет такого Steam ID, замена не произведена")
    else:
        con = sqlite3.connect("users_games.db")
        cursor = con.cursor()
        cursor.execute(f"UPDATE Users_games SET user_game = {game_id} WHERE user_id = {message.from_user.id}")
        con.commit()
        cursor.close()
        bot.send_message(message.from_user.id, "Замена произведена")

def game_list(message):
    if message.text=="Выбрать игру из списка":
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton('1.Apex Legends', callback_data='list1')
        item2 = types.InlineKeyboardButton('2.Control Ultimate Edition', callback_data='list2')
        item3 = types.InlineKeyboardButton('3.Dead by Daylight', callback_data='list3')
        item4 = types.InlineKeyboardButton('4.Deep Rock Galactic', callback_data='list4')
        item5 = types.InlineKeyboardButton('5.Dishonored RHCP', callback_data='list5')
        item6 = types.InlineKeyboardButton('6.Dishonored 2', callback_data='list6')
        item7 = types.InlineKeyboardButton('7.DOOM Eternal', callback_data='list7')
        item8 = types.InlineKeyboardButton('8.Dying Light', callback_data='list8')
        item9 = types.InlineKeyboardButton('9.Dying Light 2', callback_data='list9')
        item10 = types.InlineKeyboardButton('10.Half Life', callback_data='list10')
        item11 = types.InlineKeyboardButton('11.Half Life 2', callback_data='list11')
        item12 = types.InlineKeyboardButton('12.Killing Floor 2', callback_data='list12')
        item13 = types.InlineKeyboardButton("13.Mirror's Edge", callback_data='list13')
        item14 = types.InlineKeyboardButton("14.Mirror's Edge™ Catalyst", callback_data='list14')
        item15 = types.InlineKeyboardButton('15.Payday 2', callback_data='list15')
        item16 = types.InlineKeyboardButton('16.Portal 2', callback_data='list16')
        item17 = types.InlineKeyboardButton('17.Terraria', callback_data='list17')
        item18 = types.InlineKeyboardButton('18.Team Fortress 2', callback_data='list18')
        item19 = types.InlineKeyboardButton('19.Titanfall 2', callback_data='list19')
        item20 = types.InlineKeyboardButton('20.Warframe', callback_data='list20')
        row1 = [item1,item2]
        row2 =[item3,item4]
        row3 =[item5,item6]
        row4=[item7,item8]
        row5=[item9,item10]
        row6=[item11,item12]
        row7=[item13,item14]
        row8=[item15,item16]
        row9=[item17,item18]
        row10=[item19,item20]
        rows = [row1,row2,row3,row4,row5,row6,row7,row8,row9,row10]
        markup = telebot.types.InlineKeyboardMarkup(rows)
        bot.send_message(message.chat.id,"Test",reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def games_from_list(callback):
    dic={"list1" : 1172470,
        "list2" : 870780,
        "list3" : 381210,
        "list4" : 548430,
        "list5" : 217980,
        "list6" : 782330,
        "list7" : 403640,
        "list8" : 239140,
        "list9" : 534380,
        'list10' : 70,
        'list11' : 220,
        'list12' : 232090,
        'list13' : 17410,
        'list14' : 1233570,
        'list15' : 218620,
        'list16' : 620,
        'list17' : 105600,
        'list18' : 440,
        'list19' : 1237970,
        'list20' : 230410}
    game_id = dic[callback.data]
    con = sqlite3.connect("users_games.db")
    cursor = con.cursor()
    cursor.execute(f"UPDATE Users_games SET user_game = {game_id} WHERE user_id = {callback.message.chat.id}")
    con.commit()
    cursor.close()
    bot.send_message(callback.message.chat.id, "Замена произведена")

bot.infinity_polling()


