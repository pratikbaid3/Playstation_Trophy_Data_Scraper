from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import sqlite3

#https://www.playstationtrophies.org/guides/ps4/

game_name=[]
game_image_link=[]
game_guide_url=[]

conn=sqlite3.connect('PS4_Game_Database.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS PS4_Games
    (game_name TEXT,game_image_link TEXT,game_guide_url TEXT)""")

def adding_data_to_db(game_name,game_image_link,game_guide_url):
    try:
        c.execute("""INSERT INTO PS4_Games (game_name,game_image_link,game_guide_url) VALUES ("{}","{}","{}");""".format(game_name,game_image_link,game_guide_url))
        print('SUCCESS:'+game_name)
    except Exception as e:
        print(e)
        print("ERROR: "+game_name)

try:
    for i in range(1,45):
        game_name=[]
        game_image_link=[]
        game_guide_url=[]
        my_url='https://www.playstationtrophies.org/guides/ps4/'+str(i)
        req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
        uClient = urlopen(req)
        page_html=uClient.read()
        uClient.close()
        page_soup=soup(page_html,"html.parser")

        #Extracting the game names
        game_name_h4=page_soup.find_all('div',{"class":"col-md-8"})
        game_name_h4=game_name_h4[0].find_all('h4',{"class":"h-5"})
        for i in game_name_h4:
            game_name.append(i.text)

        #Extract the game image
        game_name_h4=page_soup.find_all('div',{"class":"col-md-8"})
        game_image_div=game_name_h4[0].find_all('div',{'class':"list__pic"})
        for i in game_image_div:
            game_img_a=i.find_all('a')
            game_image_link.append(game_img_a[0].img['src'])

        
        #Extract the game guide link
        game_name_h4=page_soup.find_all('div',{"class":"col-md-8"})
        for i in page_soup.find_all('a', {"class":"list__item-link"}):
            game_guide_url.append(i['href'])
        
        for i in range(0,len(game_name)):
            adding_data_to_db(game_name[i],game_image_link[i],game_guide_url[i])
    conn.commit()
    conn.close()

except Exception as e:
	print("ERROR : "+str(e))