import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sqlite3

# game_id = 218620
page = 1
n=3
def entry_id_set(id):
    con = sqlite3.connect("users_games.db")
    test = con.cursor()
    test.execute(f"SELECT * FROM Users_games WHERE user_id={id}")
    testvalue = test.fetchall()
    test.close()
    if len(testvalue) == 0:
        cursor = con.cursor()
        ug = (id, 218620)
        cursor.execute("INSERT INTO Users_games (user_id, user_game) VALUES (?, ?)",ug)
        con.commit()
        cursor.close()

def get_game_id(message):
    con = sqlite3.connect("users_games.db")
    test = con.cursor()
    test.execute(f"SELECT user_id,user_game FROM Users_games WHERE user_id={message.chat.id}")
    e,testvalue = test.fetchone()
    return testvalue

def get_key_word(message):
    con = sqlite3.connect("users_games.db")
    cur = con.cursor()
    cur.execute(f"SELECT user_id,user_key_word FROM Users_games WHERE user_id={message.chat.id}")
    e,word = cur.fetchone()
    return word

def get_key_words(message):
    con = sqlite3.connect("Key_Words.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT user_id,key_word FROM Key_Words Where user_id = {message.chat.id}")
    e,return_value = cursor.fetchall() #e нужна чтобы обработать полученные данные в желаемом виде
    print(return_value)
    return return_value

def disc_parser(message,page):
    game_id = get_game_id(message)
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

def guides_parser(message,page):
    game_id = get_game_id(message)
    html=requests.get(f"https://steamcommunity.com/app/{game_id}/guides/?searchText=&browsefilter=trend&browsesort=creationorder&requiredtags%5B0%5D=-1&p={page}").text
    soup = BeautifulSoup(html, 'html.parser')
    find= soup.find_all("a", class_ = "workshopItemCollection ugc_show_warning_image ugc")
    
    guides = []
    for guide in find:
        url=guide.get("href")
        title=guide.find("div", class_ ="workshopItemTitle").text.strip()
        author = guide.find("div", class_ = "workshopItemAuthorLine")
        author = author.find('span').text.strip()
        desc = guide.find("div",class_ = "workshopItemShortDesc").text.strip()
        guides.append((title, author, url, desc))
    
    return guides

def disc_page_turner(message,n):
    #одна страница = 15 обсуждений
    results=''
    e=[]
    for i in range (1,n+1):
        results +=f"""
Страница {i}
        
        """
        e=disc_parser(message,page)
        for j in e:
            results+=f"""
Topic : {j[0]}
URL: {j[1]}
Автор: {j[2]}
Кол-во записей: {j[3]}
Последнее сообщение: {j[4]}


"""
    return results

def guides_page_turner(message,n):
    #одна страница = 30 гайдов
    #выдаёт ошибку из-за слишком длиного сообщения
    e=[]
    results=""
    for i in range (1,n+1):
        results+=f"""
Страница {i}"""
        e=guides_parser(message,i)
        for j in e:
            results+=f'''
Name: {j[0]}
Ссылка: {j[2]} 
            '''
    return results

def check_game_id(game):
    html = requests.get(f"https://steamcommunity.com/app/{game}/discussions/?fp={page}").text
    soup = BeautifulSoup(html, 'html.parser')
    divs = bool(soup.find("div", class_ = 'forum_topic'))
    if divs is True:
        return game
    else:
        return -1