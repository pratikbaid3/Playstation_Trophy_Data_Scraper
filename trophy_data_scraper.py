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
    (game_name TEXT,trophy_name TEXT,trophy_description TEXT)""")

def adding_data_to_db(gName,tName,description,entry):
    try:
        c.execute("""INSERT INTO trophies (game_name,trophy_name,trophy_description) VALUES ("{}","{}","{}");""".format(gName,tName,description))
        print('Success at' +str(i))
    except:
        print('Error at' +str(i))

for i in range(4544,noOfGames):
    my_url='https://www.playstationtrophies.org'+gameData[i][1]
    req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
    uClient = urlopen(req)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    allLinksTrophyName=page_soup.find_all('td',{"class":"ac2"})
    allLinksTrophyDescription=page_soup.find_all('td',{"class":"ac3"})

    description=[]

    for k in range(0,len(allLinksTrophyDescription)):
        description.append(allLinksTrophyDescription[k].text)
    
    noOfTrophies=len(allLinksTrophyName)

    k=0
    for j in range(0,noOfTrophies):
        adding_data_to_db(gameData[i][0],allLinksTrophyName[j].a.b.text,description[k],i)
        k=k+2
    conn.commit()
conn.close()
