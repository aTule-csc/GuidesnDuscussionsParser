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
#bot = telebot.TeleBot(os.getenv("token"))
def steam_parse():
    html = requests.get("https://steamcommunity.com/app/218620/discussions/?l=russian&p=1").text
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
        author = post.find("div", class_ = "forum_topic_op").text.strip()
        reply_count = post.find("div", class_ = "forum_topic_reply_count").text.strip()
        lastpost = post.find("div", class_ = "forum_topic_lastpost").get("title")
        posts.append((name, url,author,reply_count,lastpost))
    return posts
def diss_sort_test():
    a = 'Jacket'
    b = steam_parse()
    #def sort(a,b):
    results = []
    for i in b:
        pattern =re.compile(a)
        line = i[0]
        c=bool(pattern.search(line))
        if c == True:
            results.append(i)
    print(results)

def guides_parser():
    html=requests.get("https://steamcommunity.com/app/218620/guides/?searchText=&browsefilter=trend&browsesort=creationorder&requiredtags%5B0%5D=-1&p=1").text
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

print(guides_parser())


    
#print(steam_parse())

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