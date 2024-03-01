from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import json
from aiogram import types

file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)
oldSIze = f.get('oldSIze')
makeSize = f.get('makeSize')
standartSize = f.get('standartSize')
back = f.get('back')
order_old = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=str(oldSIze))],
        [types.KeyboardButton(text=str(makeSize))],
        [types.KeyboardButton(text=str(standartSize))],
        [types.KeyboardButton(text=str(back))]

    ],
    resize_keyboard=True
)
