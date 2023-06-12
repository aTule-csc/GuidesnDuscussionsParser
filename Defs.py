import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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
        desc = guide.find("div",class_ = "workshopItemShortDesc").text.strip()
        guides.append((title, author, url, desc))
    
    return guides

def disc_page_turner(n):
    #одна страница = 15 обсуждений
    results=''
    e=[]
    for i in range (1,n+1):
        results +=f"""
Страница {i}
        
        """
        e=disc_parser(game_id,i)
        for j in e:
            results+=f"""
Topic : {j[0]}
URL: {j[1]}
Автор: {j[2]}
Кол-во записей: {j[3]}
Последнее сообщение: {j[4]}


"""
    return results

def guides_page_turner(n):
    #одна страница = 30 гайдов
    #выдаёт ошибку из-за слишком длиного сообщения
    e=[]
    results=""
    for i in range (1,n+1):
        results+=f"""
Страница {i}"""
        e=guides_parser(game_id,i)
        for j in e:
            results+=f'''
Name: {j[0]}
Автор: {j[1]}
Описание: {j[3]}
Ссылка: {j[2]} 
            '''
    return results