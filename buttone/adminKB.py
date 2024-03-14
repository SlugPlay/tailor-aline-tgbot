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
top = f.get("top")
skirt = f.get("skirt")
throusres = f.get("throusres")
menedger = f.get("menedger")
perereg = f.get("perereg")
admin = f.get("admin")
clothes = f.get("clothes")
lists = f.get("lists")
menu = f.get("menu")


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=str(lists))]

    ],
    resize_keyboard=True
)
