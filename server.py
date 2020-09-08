from aiohttp import web
import jwt
import requests
import json
import time
from tilegame import TileGame

CLIENT_ID = "9zgymms0nexuuqai86o1gkdz31sgp4"

jwks = json.loads(requests.get("https://id.twitch.tv/oauth2/keys").content)
public_keys = {}
for jwk in jwks['keys']:
    kid = jwk['kid']
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))


game = TileGame(20)


async def join(request):
    if not game.state == "waiting":
        return web.Response(text="The game is not accepting members right now", status=400)

    if not 'id_token' in request.query:
        return web.Response(text="id_token is a required parameter", status=404)
    
    twitch_user_name = get_twitch_user_name(request.query['id_token'])
    if twitch_user_name is None:
        return web.Response(text="The id_token provided is not valid", status=404)
    
    access_token = await game.register(twitch_user_name)

    return web.Response(text=json.dumps({'access_token': access_token}))

async def respond(request):
    if not game.state == 'started':
        return web.Response(text="The game has not started", status=401)
    
    if not 'access_token' in request.query:
        return web.Response(text='The access_token parameter is required for this method', status=404)
    
    player = game.get_player(request.query['access_token'])
    if player is None:
        return web.Response(text='Your access_token is invalid', status=404) 

    resp = await game.handle_response(player, json.loads(request.query['response']))
    return web.Response(text=resp)

async def status(request):
    r = {
        "grid": game.get_grid(),
        "player": game.get_player_data()
    }
    return web.Response(text=json.dumps(r))

async def set_state(request):

    if not 'id_token' in request.query:
        return web.Response(text="id_token is a required parameter", status=404)
    
    twitch_user_name = get_twitch_user_name(request.query['id_token'])
    if twitch_user_name is None:
        return web.Response(text="The id_token provided is not valid", status=404)
    
    if twitch_user_name == "fendull":
        game.state = request.query['state']

    return web.Response(text="State change successful")

def get_twitch_user_name(id_token):
    try:
        kid = jwt.get_unverified_header(id_token)['kid']
        key = public_keys[kid]
        payload = jwt.decode(id_token, key=key, algorithms=['RS256'], audience=CLIENT_ID)
        return payload['preferred_username']
    except Exception as e:
        print(e)
        return None




app = web.Application()
app.router.add_get('/join', join)
app.router.add_get('/respond', respond)
app.router.add_get('/status', status)
app.router.add_get('/state', set_state)
web.run_app(app, host='localhost', port=8000)