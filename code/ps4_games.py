
import sqlite3

#Get all the games
def get_games(page,count):
    try:
        page=int(page)
        count=int(count)
        lower_limit=(page-1)*10

        conn=sqlite3.connect('PS4_Game_Database.db')
        c=conn.cursor()
        c.execute(f'SELECT * FROM PS4_Games ORDER BY game_name LIMIT {lower_limit},{count}')
        games=c.fetchall()
        game_list=[]
        for data in games:
            game={
                'game_name':data[0],
                'game_image_url':data[1],
            }
            game_list.append(game)
        conn.commit()
        conn.close()
        return (game_list)
    except Exception as e:
        print(e)
        return 'Error'

#Get general details of a game
def get_game(name):
    try:
        print(name)
        conn=sqlite3.connect('PS4_Game_Database.db')
        c=conn.cursor()
        c.execute(f'SELECT * FROM PS4_Games WHERE game_name = \"{name}\"')
        games=c.fetchall()
        game_list=[]
        for data in games:
            game={
                'game_name':data[0],
                'game_image_url':data[1],
            }
            game_list.append(game)
        conn.commit()
        conn.close()
        if(len(game_list)>0):
            return (game_list[0])
        else:
            return('Error')
    except Exception as e:
        print(e)
        return 'Error'

#Get guide and detailed info about a game
def get_game_guide(name):
    try:
        conn=sqlite3.connect('PS4_Game_Database.db')
        c=conn.cursor()
        c.execute(f'SELECT * FROM PS4_Games WHERE game_name = \"{name}\"')
        games=c.fetchall()
        game_guide_list=[]
        game_image_url=''
        for data in games:
            game_image_url=data[1]
        c.execute(f'SELECT * FROM PS4_Games_Guide WHERE game_name = \"{name}\"')
        guides=c.fetchall()
        for data in guides:
            guide={
                'trophy_name':data[1],
                'trophy_image':data[2],
                'trophy_type':data[3],
                'trophy_description':data[4],
                'trophy_guide':data[5],
            }
            game_guide_list.append(guide)

        game={
            'game_name':name,
            'game_image_url':game_image_url,
            'guide':game_guide_list
        }
        conn.commit()
        conn.close()
        return (game)
    except Exception as e:
        print(e)
        return 'Error'

