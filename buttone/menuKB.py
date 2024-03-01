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
top = f.get("top")
skirt = f.get("skirt")
throusres = f.get("throusres")
menedger = f.get("menedger")
perereg = f.get("perereg")

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=str(top))],
        [types.KeyboardButton(text=str(skirt))],
        [types.KeyboardButton(text=str(throusres))],
        [types.KeyboardButton(text=str(menedger))],
        [types.KeyboardButton(text=str(perereg))]

    ],
    resize_keyboard=True
)
