import telebot
import requests
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
import json
bot = telebot.TeleBot(os.getenv("token"))
def steam_parse():
    html = requests.get("https://steamcommunity.com/app/218620/discussions/?l=russian").text
    soup = BeautifulSoup(html, 'html.parser') 
    divs = soup.find_all("div", class_ = 'forum_topic')
    posts = []
    for post in divs:
        url = post.find("a", class_ = "forum_topic_overlay").get("href")
        name = post.find("div", class_ = "forum_topic_name").text.strip() 
        posts.append((name, url))
    return posts


print(steam_parse())

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
bot.infinity_polling()