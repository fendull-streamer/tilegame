import asyncio
import json
import random
import string
from questions import QuestionGenerator, QuestionSolver
import time

def generate_access_token():
    return ''.join([random.choice(string.ascii_letters) for i in range(10)])

class TileGame:
    def __init__(self, grid_size):
        self.key_to_player = {}
        self.player_data = {}
        self.player_locks = {}
        self.grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        self.grid_lock = asyncio.Lock()
        self.grid_size = grid_size
        self.state = "waiting"
    
    def set_state(self, val):
        self.state = val

    def get_player(self, key):
        try: 
            return self.key_to_player[key]
        except:
            return None

    async def register(self, player):
        
        
        access_token = generate_access_token()
        self.key_to_player[access_token] = player
        
        self.player_locks[player] = asyncio.Lock()
        
        if player in self.player_data:
            return access_token

        self.player_data[player] = {
            'points': 0,
            'position': [random.randrange(self.grid_size), random.randrange(self.grid_size)],
            'questions_for_move': 0,
            'questions_until_move':0,
            'current_question': QuestionGenerator.move(5)
        }

        await self.set_tile(player, self.player_data[player]['position'][0], self.player_data[player]['position'][1])
        return access_token

    async def handle_response(self, player, response):
        await self.player_locks[player].acquire()
        

        try:
            if self.player_data[player]['current_question']['type'] == 'move':
                
                r = self.player_data[player]['position'][0]
                c = self.player_data[player]['position'][1]
                
                if response['value'] in ['down', 'up', 'left', 'right']:
                    if response['value'] == 'down':
                        r = (r + 1) % self.grid_size
                    elif response['value'] == 'up':
                        r = (r - 1) % self.grid_size

                    elif response['value'] == 'right':
                        c = (c + 1) % self.grid_size

                    else:
                        c = (c - 1) % self.grid_size
                    
                    await self.set_tile(player, r, c)
                    self.player_data[player]['position'] = [r, c]
                    scores = json.loads(self.get_scores())
                    scores.sort(key=lambda x: -x[1])
                    qs = len(scores)
                    i = 0
                    while scores[i][0] != player:
                        i += 1
                    
                    self.player_data[player]['questions_for_move'] = qs - i
                    self.player_data[player]['questions_until_move'] = qs - i
                    self.player_data[player]['current_question'] = QuestionGenerator.generate_question(30)

            else:
                answer = QuestionSolver.solve(self.player_data[player]['current_question'])
                if response['value'] == answer or time.time() > self.player_data[player]['current_question']['expires']:
                    self.player_data[player]['questions_until_move'] -= 1
                    if self.player_data[player]['questions_until_move'] == 0:
                        self.player_data[player]['current_question'] = QuestionGenerator.move(30)
                    else:
                        self.player_data[player]['current_question'] = QuestionGenerator.generate_question(30)
        except Exception as e:
            print(e)        
                
        finally:
            self.player_locks[player].release()
            return json.dumps(self.player_data[player])
            



    def get_grid(self):
        return json.dumps(self.grid)
    
    def get_player_data(self):
        return json.dumps(self.player_data)
    
    def get_scores(self):
        return json.dumps([[key, self.player_data[key]['points']] for key in self.player_data])

    async def set_tile(self, player, r, c):
        await self.grid_lock.acquire()

        try:
            prev = self.grid[r][c]
            self.grid[r][c] = player
            
        finally:
            self.grid_lock.release()

        self.increment_points(player, 1)
        if not prev is None:
            self.increment_points(prev, -1)
    
    def increment_points(self, player, points):

        

        
        self.player_data[player]['points'] += points
        