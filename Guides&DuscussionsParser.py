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




bot.infinity_polling()