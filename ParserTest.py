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

a=requests.get('https://steamcommunity.com/app/218620/discussions/').text
print(a)
"""soup = BeautifulSoup(a, "html.parser")
info = soup.find_all('div',class_='forum_topic  unread')
print(a)
""""""
req = urllib.request.Request('https://steamcommunity.com/app/218620/discussions/',)
with urllib.request.urlopen(req) as response:
    the_page = response.read()
print(the_page)
"""
bot.infinity_polling()