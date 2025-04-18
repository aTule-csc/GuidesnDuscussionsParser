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

games_dic={"list1" : 1172470,
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
games_id_name ={
    1172470 :"Apex Legends",
    870780 : "Control Ultimate Edition",
    381210 : "Dead by Daylight",
    548430 : "Deep Rock Galactic",
    217980 : "Dishonored RHCP (СНГ)",
    782330 : "Dishonored 2",
    403640 : "DOOM Eternal", 
    239140 :"Dying Light",
    534380 : "Dying Light 2",
    70 : "Half Life",
    220 : "Half Life 2",
    232090 : "Killing Floor 2",
    17410 : "Mirror's Edge",
    1233570 : "Mirror's Edge™ Catalyst",
    218620 : "Payday 2",
    1272080 :"Payday 3",
    620 : "Portal 2",
    105600 : "Terraria",
    440 : "Team Fortress 2 (2007)",
    1237970 : "Titanfall 2 (2016)",
    230410 : "Warframe",
    730 : "Counter-Strike 2",
    570 : "Dota 2" 
}
words_dic ={"word1":0,
            "word2":1,
            "word3":2,
            "word4":3,
            "word5":4,
            "word6":5}

@bot.message_handler(commands=['start','back'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Начать")
    markup.add(item1)
    bot.send_message(message.chat.id,"Нажмите кнопку внизу экрана для начала работы",reply_markup=markup)
@bot.message_handler(content_types='text')
def main(message):
    if message.text=="Начать" or message.text=="В начало":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("Парсить обсуждения")
        item2=types.KeyboardButton("Парсить руководства")
        item3=types.KeyboardButton("Изменить список игр")
        item4=types.KeyboardButton("Список ключевых слов")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        User_id = message.from_user.id
        Defs.entry_id_set(User_id)
        bot.send_message(message.chat.id,"Что хотите делать?",reply_markup=markup) 
    disc_parse(message)
    guides_parse(message)
    game_list_change(message)
    word_change(message)
    
def disc_parse(message):
    if message.text=="Парсить обсуждения":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Первая страница обсуждений")
        item2=types.KeyboardButton("Обсуждения с фильтром")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно парсить обсуждения?",reply_markup=markup)
    disc_parser_wof(message)
    disc_parser_wtof(message)

def guides_parse(message):
    if message.text=="Парсить руководства":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Первая страница руководств")
        item2=types.KeyboardButton("Руководства с фильтром")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно парсить руководства?",reply_markup=markup)
    guides_parser_wof(message)
    guides_parser_wtof(message)

def game_list_change(message):
    if message.text=="Изменить список игр":
        markup=types.ReplyKeyboardMarkup()
        item1=types.KeyboardButton("Добавить свою игру")
        item2=types.KeyboardButton("Выбрать игру из списка")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно изменить список?",reply_markup=markup)
    set_game_id(message)
    game_list(message)

def word_change(message):
    if message.text=="Список ключевых слов":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("Изменить список")
        item2=types.KeyboardButton("Выбрать слово из списка")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,"Как именно изменить список?",reply_markup=markup)
    word_list_change(message)
    word_pick(message)

def disc_parser_wof(message):
    if message.text=="Первая страница обсуждений":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("В начало")
        markup.add(item1)
        bot.send_message(message.from_user.id,Defs.disc_page_turner(message,1),reply_markup=markup)

def disc_parser_wtof(message):
    if message.text=="Обсуждения с фильтром":
        word = Defs.get_key_word(message)
        game_id = int(Defs.get_game_id(message))
        remove = telebot.types.ReplyKeyboardRemove()
        msg=bot.send_message(message.chat.id, f'Ваше ключевое слово : {word}, Выбранная игра (её id) : {games_id_name.get(game_id,game_id)}. Введите номер кол-ва страниц которое желаете отсортировать по данному ключевому слову?',reply_markup=remove)
        bot.register_next_step_handler(msg,disc_parser_wtof_results)

def disc_parser_wtof_results(message):
    number = message.text
    word = Defs.get_key_word(message)
    try:
        number=int(number)
    except (ValueError,TypeError):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1 = types.KeyboardButton("Обсуждения с фильтром")
        item2 = types.KeyboardButton("В начало")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.from_user.id,f"Никаких {number}, вводи нормальные числа",reply_markup=markup)

    else:
        limit = len(Defs.disc_page_turner_sort(message,number,word))
        if limit <= 4096:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            item1 = types.KeyboardButton("Обсуждения с фильтром")
            item2 = types.KeyboardButton("В начало")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.from_user.id,Defs.disc_page_turner_sort(message,number,word),reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            item1 = types.KeyboardButton("Обсуждения с фильтром")
            item2=types.KeyboardButton("Выбрать слово из списка")
            item3 = types.KeyboardButton("В начало")
            markup.add(item1,item2)
            markup.add(item3)
            bot.send_message(message.from_user.id,f"Длина вашего результата поиска составила {limit} символа(ов) из 4096 допустимых Телеграммом, уменьшите круг поиска или смените ключевое слово",reply_markup=markup)


def guides_parser_wof(message):
    if message.text=="Первая страница руководств":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("В начало")
        markup.add(item1)
        bot.send_message(message.from_user.id,Defs.guides_page_turner(message,1),reply_markup=markup)

def guides_parser_wtof(message):
    if message.text=="Руководства с фильтром":
        word = Defs.get_key_word(message)
        game_id = int(Defs.get_game_id(message))
        remove = telebot.types.ReplyKeyboardRemove()
        msg=bot.send_message(message.chat.id, f'Ваше ключевое слово : {word}, Выбранная игра (её id) : {games_id_name.get(game_id,game_id)}. Введите номер кол-ва страниц которое желаете отсортировать по данному ключевому слову?',reply_markup=remove)
        bot.register_next_step_handler(msg,guides_parser_wtof_results)

def guides_parser_wtof_results(message):
    number=message.text
    word = Defs.get_key_word(message)
    try:
        number=int(number)
    except (ValueError,TypeError):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1 = types.KeyboardButton("Руководства с фильтром")
        item2 = types.KeyboardButton("В начало")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.from_user.id,f"Никаких {number}, вводи нормальные числа",reply_markup=markup)
    else:
        limit = len(Defs.guides_page_turner_sort(message,number,word))
        if limit <= 4096:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            item1 = types.KeyboardButton("Руководства с фильтром")
            item2=types.KeyboardButton("В начало")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.from_user.id,Defs.guides_page_turner_sort(message,number,word),reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            item1 = types.KeyboardButton("Руководства с фильтром")
            item2=types.KeyboardButton("Выбрать слово из списка")
            item3 = types.KeyboardButton("В начало")
            markup.add(item1,item2)
            markup.add(item3)
            bot.send_message(message.from_user.id,f"Длина вашего результата поиска составила {limit} символа(ов) из 4096 допустимых Телеграммом, уменьшите круг поиска или смените ключевое слово",reply_markup=markup)

def set_game_id(message):
    if message.text=="Добавить свою игру":
        bot.send_message(message.from_user.id,"Введи Steam ID" )
        bot.register_next_step_handler(message,game_add)

def game_add(message):
    game_id = Defs.check_game_id(message.text)
    if game_id == -1:
        bot.send_message(message.from_user.id, "Нет такого Steam ID, замена не произведена")
    else:
        con = sqlite3.connect("users_games.db")
        cursor = con.cursor()
        cursor.execute(f"UPDATE Users SET user_game = {game_id} WHERE user_id = {message.from_user.id}")
        con.commit()
        cursor.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("В начало")
        markup.add(item1)
        bot.send_message(message.from_user.id, f"Замена произведена, новая игра {games_id_name.get(game_id,game_id)}",reply_markup=markup)

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
def callback_data_handler(callback):
    if callback.data in games_dic.keys():
        game_id = games_dic[callback.data]
        con = sqlite3.connect("users_games.db")
        cursor = con.cursor()
        cursor.execute(f"UPDATE Users SET user_game = {game_id} WHERE user_id = {callback.message.chat.id}")
        con.commit()
        cursor.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1 = types.KeyboardButton("В начало")
        markup.add(item1)
        bot.send_message(callback.message.chat.id, f"Замена произведена, новая игра {games_id_name.get(game_id,game_id)}",reply_markup=markup)

    if callback.data in words_dic.keys():
        word_id = words_dic[callback.data]
        word_tuple = Defs.get_key_words(callback.message)
        word_list =list(word_tuple)
        if len(word_list) > word_id:
            con = sqlite3.connect("users_games.db")
            cursor = con.cursor()
            insert_values =(f"{word_list[word_id]}",callback.message.chat.id)
            cursor.execute(f"UPDATE Users SET user_key_word = ? WHERE user_id = ?" ,insert_values)
            con.commit()
            cursor.close()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            item1 = types.KeyboardButton("В начало")
            markup.add(item1)
            bot.send_message(callback.message.chat.id, f"Замена произведена, новое ключевое слово {word_list[word_id]}",reply_markup=markup)


def word_list_change(message):
    if message.text=="Изменить список":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        item1=types.KeyboardButton("Добавить слово")
        item2=types.KeyboardButton("Изменить слово")
        item3=types.KeyboardButton("Удалить слово")
        item4 = types.KeyboardButton("В начало")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id,"Как именно изменить список?",reply_markup=markup)
    word_add_replace_remove(message)

def word_add_replace_remove(message):
    words_list = Defs.get_key_words(message)
    if message.text == "Добавить слово":
        bot.send_message(message.chat.id,"Введите слово которое хотите добавить, учтите что слово должно состоять только из строчных букв")
        bot.register_next_step_handler(message,word_list_add)
    if message.text == "Изменить слово":
        bot.send_message(message.chat.id,f"Введите слово которое хотите изменить, список ваших слов :{words_list}")
        bot.register_next_step_handler(message,word_list_replace_setup)
    if message.text == "Удалить слово":
        bot.send_message(message.chat.id,f"Введите слово которое хотите удалить, список ваших слов :{words_list}")
        bot.register_next_step_handler(message,word_list_remove)

def word_list_add(message):
    word = message.text
    word = word.lower()
    words_list = Defs.get_key_words(message)
    if len(words_list) > 5:
        bot.send_message(message.chat.id,"Лимит слов превышен, добавление невозможно")
    if word in words_list:
        bot.send_message(message.chat.id,"Данное слово существует в вашем списке, добавление отменено")
    else:
        insert_values = (message.chat.id, word)
        con = sqlite3.connect("Key_Words.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Key_Words (user_id, key_word) VALUES (?, ?)",insert_values)
        con.commit()
        cursor.close()
        con.close()
        bot.send_message(message.chat.id,f"Добавление произведено, новое слово в списке {word}")

def word_list_replace_setup(message):
    word_to_change = message.text
    bot.send_message(message.from_user.id,"Введите слово на которое хотите изменить" )
    bot.register_next_step_handler(message,word_list_replace,word_to_change)

def word_list_replace(message,word_to_change):
    word = message.text
    print(word,word_to_change,message.chat.id)
    words_list = Defs.get_key_words(message)
    if word_to_change in words_list:
        con = sqlite3.connect("Key_Words.db")
        cursor = con.cursor()
        insert_values = (f"{word}",f"{word_to_change}",message.chat.id)
        cursor.execute(f"UPDATE Key_Words SET key_word = ? WHERE key_word = ? AND user_id = ?",insert_values)
        con.commit()
        cursor.close()
        con.close()
        bot.send_message(message.chat.id,"Замена произведено")
    else:
        bot.send_message(message.chat.id,"Данное слово не существует в вашем списке, замена отменена")

def word_list_remove(message):
    word = str(message.text)
    words_list = Defs.get_key_words(message)
    if word in words_list:
        con = sqlite3.connect("Key_Words.db")
        cursor = con.cursor()
        insert_values = (f"{word}",message.chat.id)
        cursor.execute(f"DELETE FROM Key_Words WHERE key_word = ? and user_id = ? ", insert_values)
        con.commit()
        cursor.close()
        con.close()
        bot.send_message(message.chat.id,"Удаление произведено")
    else:
        bot.send_message(message.chat.id,"Данное слово не существует в вашем списке, удаление отменено")


def word_pick(message):
        if message.text=="Выбрать слово из списка":
            word_tuple = Defs.get_key_words(message)
            word_list =list(word_tuple)
            print(word_list)
            while len(word_list) < 6:
                word_list.append('"пусто"')
            markup = types.InlineKeyboardMarkup()
            item1=types.InlineKeyboardButton(f"{word_list[0]}",callback_data='word1')
            item2=types.InlineKeyboardButton(f"{word_list[1]}",callback_data='word2')
            item3=types.InlineKeyboardButton(f"{word_list[2]}",callback_data='word3')
            item4=types.InlineKeyboardButton(f"{word_list[3]}",callback_data='word4')
            item5=types.InlineKeyboardButton(f"{word_list[4]}",callback_data='word5')
            item6=types.InlineKeyboardButton(f"{word_list[5]}",callback_data='word6')
            row1 = [item1,item2]
            row2 = [item3,item4]
            row3 = [item5,item6]
            rows = [row1,row2,row3]
            markup = telebot.types.InlineKeyboardMarkup(rows)
            bot.send_message(message.chat.id,'Нажмите на кнопку чтобы выбрать слово из списка. Начатие на "пусто" ни к чему не приведёт',reply_markup=markup)

    # word_id = words_dic[callback.data]
    # if callback.data in words_dic.keys:
    #     word_id = words_dic[callback.data]
    #     words_list = Defs.get_key_words(callback.message)
    #     bot.send_message(callback.message.chat.id, f"id={word_id}")
    #     con = sqlite3.connect("Key_Words.db")#нужно доделать
    #     cursor = con.cursor()
bot.infinity_polling()


