import random
import time

class QuestionGenerator:
    @staticmethod
    def move(t):
        return {
            "type": "move",
            "explanation": "Please choose a direction (up, down, left or right) to move within the grid. You will gain a tile if the tile you step on is not already your own",
            "expires": int(time.time()) + t
        }
    
    @staticmethod
    def add(t):
        return {
            "type": "add",
            "explanation": "Return the result of value1 and value2",
            "value1": random.randrange(1000),
            "value2": random.randrange(1000),
            "expires": int(time.time()) + t
        }
    
    @staticmethod
    def generate_question(t):
        return QuestionGenerator.add(t)

class QuestionSolver:

    @staticmethod
    def solve(q):
        if q['type'] == 'add':
            return q['value1'] + q['value2']
