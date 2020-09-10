from tile_game_client import TileGameClient
import time

ID_TOKEN = "YourIDTokenHere"

client = TileGameClient(ID_TOKEN)


#Makes an attempt to join the game every 5 seconds
while not client.join() is True:
    time.sleep(5)


#Ask the server every 3 seconds for a question. If the game hasn't started, then client.ask() will return None
while client.ask() is None:
    time.sleep(3)

first_question = client.ask()


#write any other code you want to use here
