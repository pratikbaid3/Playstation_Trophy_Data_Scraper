from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import sqlite3


conn=sqlite3.connect('trophiesDataLink.db')
c=conn.cursor()
c.execute("SELECT * FROM trophy_data_link")

gameData=c.fetchall()
noOfGames=len(gameData)

c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS trophies
    (game_name TEXT,trophy_name TEXT,trophy_description TEXT,trophy_type TEXT,trophy_icon)""")

def adding_data_to_db(gName,tName,description,trophyType,trophyIcon,entry):
    try:
        c.execute("""INSERT INTO trophies (game_name,trophy_name,trophy_description,trophy_type,trophy_icon) VALUES ("{}","{}","{}","{}","{}");""".format(gName,tName,description,trophyType,trophyIcon))
        print('Success at' +str(i))
    except:
        print('Error at ' +str(i) +' '+gName)

for i in range(4545,noOfGames):
    my_url='https://www.playstationtrophies.org'+gameData[i][1]
    req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
    uClient = urlopen(req)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    allLinksTrophyName=page_soup.find_all('td',{"class":"ac2"})
    allLinksTrophyDescription=page_soup.find_all('td',{"class":"ac3"})
    allTrophyType=page_soup.find_all('td',{'class':'ac4'})
    allTrophyIcon=page_soup.find_all('td',{'class':'ac1'})

    description=[]
    trophyType=[]

    for k in range(0,len(allLinksTrophyDescription)):
        description.append(allLinksTrophyDescription[k].text)

    for k in range(0,len(allTrophyType)):
        if(allTrophyType[k].img['src']=='/images/site/icons/trophy_gold.png'):
            trophyType.append(2)
        elif(allTrophyType[k].img['src']=='/images/site/icons/trophy_silver.png'):
            trophyType.append(3)
        elif(allTrophyType[k].img['src']=='/images/site/icons/trophy_bronze.png'):
            trophyType.append(4)
        elif(allTrophyType[k].img['src']=='/images/site/icons/trophy_platinum.png'):
            trophyType.append(1)
    
    noOfTrophies=len(allLinksTrophyName)

    k=0
    for j in range(0,noOfTrophies):
        adding_data_to_db(gameData[i][0],allLinksTrophyName[j].a.b.text,description[k],trophyType[j],allTrophyIcon[j].img['src'],i)
        k=k+2
    conn.commit()
conn.close()
