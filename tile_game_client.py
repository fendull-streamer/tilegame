import requests
import json

GAME_URL = "http://localhost:8000/"
ACCESS_TOKEN_FILE = "access_token.txt"

class TileGameClient:

    def __init__(self, id_token):
        self.id_token = id_token
        self.access_code = None

        if not self.get_status() is None:
            try:
                with open(ACCESS_TOKEN_FILE, "r") as f:
                    self.access_code = str(f.read())
                    if len(self.access_code) < 1:
                        self.access_code = None
            except:
                pass
                
    
    def join(self):
        r = requests.get(GAME_URL + "join?id_token={}".format(self.id_token))
        print(r.content)
        if r.status_code == 200:
            print("Joined game successfully")
            self.access_code = json.loads(r.content)['access_token']
            with open(ACCESS_TOKEN_FILE, "w") as f:
                f.write(self.access_code)


    def get_status(self):
        r = requests.get(GAME_URL + "status")
        if r.status_code == 200:
            
            return json.loads(r.content)
        else:
            return None

    def ask(self):
        if self.access_code is None:
            print("Access code required, please join game")
            return
        r = requests.get(GAME_URL + "respond?response={}&access_token={}".format('{}', self.access_code))
        print(r.content)
        return json.loads(r.content)

    def set_state(self, state):
        r = requests.get(GAME_URL + "state?id_token={}&state={}".format(self.id_token, state))
        print(r.content)

    def respond(self, value):
        if self.access_code is None:
            print("Access code required, please use join")
            return
        
        r = requests.get(GAME_URL + "respond?response={}&access_token={}".format(json.dumps({"value": value}), self.access_code))
        return json.loads(r.content)
