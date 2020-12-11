from flask import Flask,request
from flask_restful import Resource, Api
import ps4_games

app=Flask(__name__)
api=Api(app)

class PS4Games(Resource):
    def get(self):
        page=request.args.get('page', 1)
        count=request.args.get('count', 50)
        try:
            game_list=ps4_games.get_games(page,count)
            if(game_list=='Error'):
                raise
            return {'result':{'games':game_list,'page':page,'count':count}}
        except Exception as e:
            print('ERROR')
            return {'result':'Server Error'}

class PS4Game(Resource):
    def get(self,name):
        try:
            game_list=ps4_games.get_game(name)
            if(game_list=='Error'):
                raise
            return {'result':{'games':game_list}}
        except Exception as e:
            print('ERROR',e)
            return {'result':'Server Error'}

class PS4GameGuide(Resource):
    def get(self,name):
        try:
            game_list=ps4_games.get_game_guide(name)
            if(game_list=='Error'):
                raise
            return {'result':{'games':game_list}}
        except Exception as e:
            print('ERROR',e)
            return {'result':'Server Error'}

api.add_resource(PS4Games,'/ps4/games/')
api.add_resource(PS4Game,'/ps4/game/<string:name>')
api.add_resource(PS4GameGuide,'/ps4/game/guide/<string:name>')

if __name__ == "__main__":
    app.run(port=5000, debug=True)