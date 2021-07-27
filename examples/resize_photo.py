from instagrapi_bot import InstagrapiBot
from instagrapi import Client

USERNAME = ''
PASSWORD = ''
PHOTO_PATH = ''

client = Client()
client.login(USERNAME, PASSWORD)

bot = InstagrapiBot(client)
bot.resize_and_upload('Example', PHOTO_PATH, '4:5', (0,0,0))
