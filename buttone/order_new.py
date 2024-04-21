from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram import types
import json
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)
makeSize = f.get('makeSize')
standartSize = f.get('standartSize')
back = f.get('back')
order_new = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=str(makeSize))],
        [types.KeyboardButton(text=str(standartSize))],
        [types.KeyboardButton(text=str(back))]

    ],
    resize_keyboard=True
)
