import telebot
import re
import requests
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
import json
import sqlite3
import Defs
#bot = telebot.TeleBot(os.getenv("token"))
game_id = 218620
page = 1
n=3
def disc_parser(game_id,page):
    html = requests.get(f"https://steamcommunity.com/app/{game_id}/discussions/?fp={page}").text
    soup = BeautifulSoup(html, 'html.parser') 
    divs = soup.find_all("div", class_ = 'forum_topic')

    posts = []
    for post in divs:
        url = post.find("a", class_ = "forum_topic_overlay").get("href")
        forum_topic_name = post.find("div", class_ = "forum_topic_name")
        span_text=forum_topic_name.find('span')
        if span_text:
            name="ЗАКРЕПЛЕНО "+span_text.next_sibling.strip()
        else:
            name=forum_topic_name.text.strip()
        if post.find("div", class_ = "forum_topic_op") is None:
            author='-'
        else:
            author = post.find("div", class_ = "forum_topic_op").text.strip()
        if post.find("div", class_ = "forum_topic_reply_count") is None:
            reply_count = '-'
        else:
            reply_count = post.find("div", class_ = "forum_topic_reply_count").text.strip()
        if post.find("div", class_ = "forum_topic_reply_count") is None:
            lastpost="-"
        else:
            lastpost = post.find("div", class_ = "forum_topic_lastpost").get("title")
        posts.append((name, url,author,reply_count,lastpost))
    return posts

def diss_sort_test():
    a = 'payday'
    b = guides_parser(game_id,page)
    #def sort(a,b):
    results = []
    for i in b:
        line = i[0]
        # print(type(line))
        pattern = re.compile(a)
        c=bool(pattern.search(line.lower()))
        if c == True:
            results.append(i)
    print(results)

def guides_parser(game_id,page):
    html=requests.get(f"https://steamcommunity.com/app/{game_id}/guides/?searchText=&browsefilter=trend&browsesort=creationorder&requiredtags%5B0%5D=-1&p={page}").text
    soup = BeautifulSoup(html, 'html.parser')
    find= soup.find_all("a", class_ = "workshopItemCollection ugc_show_warning_image ugc")
    
    guides = []
    for guide in find:
        url=guide.get("href")
        title=guide.find("div", class_ ="workshopItemTitle").text.strip()
        author = guide.find("div", class_ = "workshopItemAuthorLine")
        author = author.find('span').text.strip()
        # desc = guide.find("div",class_ = "workshopItemShortDesc").text.strip()
        guides.append((title, author, url ))#desc
    
    return guides

def disc_page_former(n):
    #одна страница = 15 обсуждений
    results=''
    lst=[]
    for i in range (1,n+1):
        results +=f"""
Страница {i}
        
        """
        lst=disc_parser(game_id,i)
        results+=disc_info_former(lst)
    return results

def guides_page_former(n):
    #одна страница = 30 гайдов
    #выдаёт ошибку из-за слишком длиного сообщения
    lst=[]
    results=""
    for i in range (1,n+1):
        results+=f"""
Страница {i}

"""
        lst=guides_parser(game_id,i)
        results+=guides_info_former(lst)
    return results

def disc_info_former(lst):
    str=''
    for j in lst:
            str+=f"""
Topic: {j[0]}
URL: {j[1]}
Автор: {j[2]}
Кол-во записей: {j[3]}
Последнее сообщение: {j[4]}

"""
    return str
    
def guides_info_former(lst):
    str=''
    for j in lst:
            str+=f'''
Name: {j[0]}
Автор: {j[1]}
Описание: {j[3]}
Ссылка: {j[2]} 
            '''
    return str

def check_game_id(game):
    html = requests.get(f"https://steamcommunity.com/app/{game}/discussions/?fp={page}").text
    soup = BeautifulSoup(html, 'html.parser')
    divs = bool(soup.find("div", class_ = 'forum_topic'))
    if divs is True:
        return game
    else:
        return -1

def game_changer():
    return 0

id = 6029053748

con = sqlite3.connect("users_games.db")
test = con.cursor()
test.execute(f"SELECT * FROM Users_games WHERE user_id=1")
testvalue = test.fetchall()
if len(testvalue) == 0:
    print("denied")
        

def get_game_id(id):
    con = sqlite3.connect("users_games.db")
    test = con.cursor()
    test.execute(f"SELECT user_id,user_game FROM Users_games WHERE user_id={id}")
    e,testvalue = test.fetchone()
    return testvalue

def get_key_word(id):
    con = sqlite3.connect("users_games.db")
    cur = con.cursor()
    cur.execute(f"SELECT user_id,user_key_word FROM Users_games WHERE user_id={id}")
    e,word = cur.fetchone()
    return word
print(get_key_word(id))

#check_game_id(1)
# def get_game_name_steamdb():
#     game_id = 730
#     html = requests.get(f"https://steamdb.info/app/{game_id}/").text
#     soup = BeautifulSoup(html, 'html.parser') 
#     hs = soup.find_all()
#     return hs

# print(get_game_name_steamdb())


"""
a=requests.get('https://steamcommunity.com/app/218620/discussions/').text
print(a)
soup = BeautifulSoup(a, "html.parser")
info = soup.find_all('div',class_='forum_topic  unread')
print(a)
req = urllib.request.Request('https://steamcommunity.com/app/218620/discussions/',)
with urllib.request.urlopen(req) as response:
    the_page = response.read()
print(the_page)
"""
#bot.infinity_polling()