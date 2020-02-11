from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import sqlite3

#https://www.playstationtrophies.org/guides/ps4/38/trophy

trophyDataLink=[]
gameName=[]

conn=sqlite3.connect('trophiesDataLink.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS trophy_data_link
    (game_name TEXT PRIMARY KEY,data_link TEXT UNIQUE,image_link TEXT UNIQUE)""")

def adding_data_to_db(name,link,img):
    c.execute("""INSERT INTO trophy_data_link (game_name,data_link,image_link) VALUES ("{}","{}","{}");""".format(name,link,img))
    #"""INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)

for j in range(1,99):
    my_url='https://www.playstationtrophies.org/games/ps4/'+str(j)+'/'
    req = Request(my_url, headers={'User-Agent': 'Chrome/5.0'})
    uClient = urlopen(req)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    allLinks=page_soup.find_all('a',{"class":"linkT"})
    allImgLink=page_soup.find_all('img',{"width":"80"})
    i=0
    k=0
    count=len(allLinks)
    while(i<count):

        name=allLinks[i].strong.contents[0]
        gameName.append(name)

        link=allLinks[i]['href']
        trophyDataLink.append(link)

        img=allImgLink[k]["src"]
        k=k+1

        adding_data_to_db(name,link,img)
        i=i+2
    
conn.commit()
conn.close()

