from aiogram import Bot
import json
file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))

def flag_request():
    file1 = open('bot_token.json', 'r')
    flag = str(json.load(file1).get('flag_midleware'))
    file1.close()
    if flag == 'False':
        return False
    elif flag == 'True':
        return True


def rewrite_flag(state):
    file2 = open('bot_token.json', 'r')
    data = json.load(file2)
    file2.close()
    data['flag_midleware'] = state
    file3 = open('bot_token.json', 'w')
    json.dump(data, file3, indent=4)
    file3.close()