from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import sqlite3

baseUrl='https://www.playstationtrophies.org/'

#Getting the game name and url from the db
conn=sqlite3.connect('PS4_Game_Database.db')
c=conn.cursor()
c.execute("SELECT * FROM PS4_Games")
gameData=c.fetchall()

game_name=[]
game_guide_url=[]

#Trophy Name
#Trophy Image
#Trophy Type
#Trophy Description
#Trophy Guide

for i in gameData:
    game_name.append(i[0])
    game_guide_url.append(i[2])

try:
    my_url='https://www.playstationtrophies.org/game/kill-all-zombies-na/guide/'
    req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
    uClient = urlopen(req)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    trophy_list=page_soup.find_all('li',{'class':'achilist__item'})
    print(len(trophy_list))
except Exception as e:
    print(e)