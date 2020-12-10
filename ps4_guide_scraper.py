from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import sqlite3

try:
    baseUrl='https://www.playstationtrophies.org'

    #Getting the game name and url from the db
    conn=sqlite3.connect('PS4_Game_Database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM PS4_Games")
    gameData=c.fetchall()

    game_name=[]
    game_guide_url=[]

    for i in gameData:
        game_name.append(i[0])
        game_guide_url.append(baseUrl+i[2])

    conn=sqlite3.connect('PS4_Game_Database.db')
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS PS4_Games_Guide
        (game_name TEXT,trophy_name TEXT,trophy_image TEXT,trophy_type TEXT,trophy_description TEXT,trophy_guide TEXT)""")

    def adding_data_to_db(game_name,trophy_name,trophy_image,trophy_type,trophy_description,trophy_guide):
        try:
            c.execute("""INSERT INTO PS4_Games_Guide (game_name,trophy_name,trophy_image,trophy_type,trophy_description,trophy_guide) VALUES ("{}","{}","{}","{}","{}","{}");""".format(str(game_name),str(trophy_name),str(trophy_image),str(trophy_type),str(trophy_description),trophy_guide))
            print('SUCCESS:'+game_name)
        except Exception as e:
            print(e)
            print("ERROR: "+game_name)

    for i in range(1979,2181):
        my_url=game_guide_url[i]
        name=game_name[i]

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
        # my_url='https://www.playstationtrophies.org/game/kill-all-zombies-na/guide/'
        req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
        uClient = urlopen(req)
        page_html=uClient.read()
        uClient.close()
        page_soup=soup(page_html,"html.parser")
        #Trophy Image
        trophy_img_list=page_soup.find_all('div',{'class':'list__pic'})
        trophy_img_list=[img.find('img')['data-src'] for img in trophy_img_list]
        trophy_img_list=[str(trophy).replace('"',"'") for trophy in trophy_img_list]
        #Trophy Name
        trophy_name_list=page_soup.find_all('div',{'class':'achilist__header'})
        trophy_name_list=[name.find('a').find('h4').text for name in trophy_name_list]
        trophy_name_list=[str(trophy).replace('"',"'") for trophy in trophy_name_list]
        #Trophy Description
        trophy_description_list=page_soup.find_all('div',{'class':'achilist__data'})
        trophy_description_list=[description.find('p',recursive=False).text for description in trophy_description_list]
        trophy_description_list=[str(trophy).replace('"',"'") for trophy in trophy_description_list]
        #Trophy Type
        trophy_type_list=page_soup.find_all('span',{'class':'achilist__value-numb'})
        trophy_type_list=[trophy.find('img')['src'] for trophy in trophy_type_list]
        trophy=[]
        for k in trophy_type_list:
            if(k=='/images/icons/trophy_gold.png'):
                trophy.append('GOLD')
            elif(k=='/images/icons/trophy_silver.png'):
                trophy.append('SILVER')
            elif(k=='/images/icons/trophy_bronze.png'):
                trophy.append('BRONZE')
            elif(k=='/images/icons/trophy_platinum.png'):
                trophy.append('PLATINUM')
        trophy_type_list=trophy
        #Trophy Guide
        trophy_guide_list=page_soup.find_all('div',{'class':'mt-1 pl-1'})
        trophy_guide_list=[trophy.find('div',recursive=False) for trophy in trophy_guide_list]
        trophy_guide_list=[str(trophy).replace('src="//','src="https://') for trophy in trophy_guide_list]
        trophy_guide_list=[str(trophy).replace('"',"'") for trophy in trophy_guide_list]

        for j in range(0,len(trophy_name_list)):
            adding_data_to_db(name,trophy_name_list[j],trophy_img_list[j],trophy_type_list[j],trophy_description_list[j],trophy_guide_list[j])
        conn.commit()
        print("******")
        print(i)
        print('******')

    conn.commit()
    conn.close()
except Exception as e:
    print(e)