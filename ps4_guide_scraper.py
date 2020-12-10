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
trophy_name_list=[]
#Trophy Image
trophy_img_list=[]
#Trophy Type
trophy_type_list=[]
#Trophy Description
trophy_description_list=[]
#Trophy Guide
trophy_guide_list=[]

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
    #Trophy Image
    trophy_img_list=page_soup.find_all('div',{'class':'list__pic'})
    trophy_img_list=[img.find('img')['data-src'] for img in trophy_img_list]
    #Trophy Name
    trophy_name_list=page_soup.find_all('div',{'class':'achilist__header'})
    trophy_name_list=[name.find('a').find('h4').text for name in trophy_name_list]
    #Trophy Description
    trophy_description_list=page_soup.find_all('div',{'class':'achilist__data'})
    trophy_description_list=[description.find('p',recursive=False).text for description in trophy_description_list]
    #Trophy Type
    trophy_type_list=page_soup.find_all('span',{'class':'achilist__value-numb'})
    trophy_type_list=[trophy.find('img')['src'] for trophy in trophy_type_list]
    trophy=[]
    for i in trophy_type_list:
        if(i=='/images/icons/trophy_gold.png'):
            trophy.append('GOLD')
        elif(i=='/images/icons/trophy_silver.png'):
            trophy.append('SILVER')
        elif(i=='/images/icons/trophy_bronze.png'):
            trophy.append('BRONZE')
        elif(i=='/images/icons/trophy_platinum.png'):
            trophy.append('PLATINUM')
    trophy_type_list=trophy
    #Trophy Guide
    trophy_guide_list=page_soup.find_all('div',{'class':'mt-1 pl-1'})
    trophy_guide_list=[trophy.find('div',recursive=False) for trophy in trophy_guide_list]

    



    print(trophy_guide_list[3])



except Exception as e:
    print(e)