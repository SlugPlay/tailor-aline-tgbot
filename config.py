from aiogram import Bot
import json
file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))