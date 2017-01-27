from bs4 import BeautifulSoup
import configparser
from pocket import Pocket, PocketException
import random
import requests
import telebot
from thumbot import Thumbot
import unshortenit
import sys

config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/CentralDeTudo/bot.conf')

bot_token = config['BOT']['token']
msg_dest = config['BOT']['dest']
bot_admin = config['BOT']['admin']
line_file = config['LINE']['file']
lastUpdates = config['LINE']['updates']
pocket_consumer_key = config['POCKET']['consumer_key']
pocket_access_token = config['POCKET']['access_token']

bot = telebot.TeleBot(bot_token)

def get_img(url):
    print('img')
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    img = html.find('meta', {'property': 'og:image'})
    if not img:
        img = html.find('meta', {'name': 'og:image'})
    try:
        img = img['content']
        preview = False
        if 'http:' not in img and 'https:' not in img:
            img = 'http:' + img
    except TypeError:
        img = ''
        preview = True
    print(img)
    return preview, img

def line_read():
    with open(line_file, 'r', encoding="utf-8") as file:
        first_line = file.readline()
        lines = file.readlines()
        file.close()
    with open(line_file, 'w', encoding="utf-8") as file:
        for l in lines:
            file.write(l)
        file.close()
    lines = open(line_file).readlines()
    random.shuffle(lines)
    open(line_file, 'w', encoding="utf-8").writelines(lines)
    return first_line.strip()

def send_line(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    try:
        title = html.find('meta', {'property': 'og:title'})
        title = title['content']
    except:
        title = html.title.text.strip()
    print(title)
    domain = url.split('://')[1].split('/')[0].replace('www.','')
    print(domain)
    preview, img = get_img(url)
    send_msg(title,url,domain,img,preview)
    send_pocket(url)

def send_msg(title,url,domain,img,preview):
    message = ('<b>{}</b><a href="{}">.</a>' +
        '\n<a href="{}">{}</a>').format(title,img,url,domain)
    bot.send_message(msg_dest, message, parse_mode='HTML', 
        disable_web_page_preview=preview,
        reply_markup=Thumbot.empty_keyboard())

def send_pocket(url):
    pocket_instance = Pocket(
        consumer_key=pocket_consumer_key,
        access_token=pocket_access_token
    )
    pocket_instance.add(url)

def expand_url(url):
    unshortened_uri,status = unshortenit.unshorten(url)
    return unshortened_uri

def fileUpdates(link):
    with open(lastUpdates, 'r') as file:
        lines = file.readlines()
    if lines.__len__() >= 100:
        lines.pop(0)
    lines.append(''.join(link) + '\n')
    with open(lastUpdates, 'w') as file:
        for l in lines:
            file.write(l)

def checkUpdates(param,new):
    updates = open(lastUpdates,'r')
    for upd in updates:
        if param in upd.split('\n'):
            new = 0
            #print('Repetido')
            return new
    if new == 1:
        fileUpdates(param)
        return new

def read_line():
    url = line_read()
    url = expand_url(url)
    print(url)
    return url

if True:
    url = read_line()
    if checkUpdates(url, 1):
        send_line(url)

#except:
#    pass
