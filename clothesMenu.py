from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from adminUser import admin_users
from stateMachine import *
from menuStart import number_request
import db
from buttone.clothes import clothes_kb
from buttone.order_new import order_new
from buttone.order_old import order_old
from buttone.menuKB import menu_kb
import json

router = Router()

global_phone_number = number_request()
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)


@router.message(StateFilter(UserSize.step31))
async def menu2(message: types.Message, state: FSMContext):
    global global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    have_user_merki = 'no'
    if str(message.text) == f.get('skirt'):
        if all_user_data[-3]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            await message.answer(f.get("size"), reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer(f.get('action'), reply_markup=order_old)
        await state.set_state(UserMenu.underSkirt)
    elif str(message.text) == f.get('throusres'):
        if all_user_data[-2]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':

            await message.answer(f.get("size"), reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer(f.get("action"), reply_markup=order_old)
        await state.set_state(UserMenu.underTrousers)
    elif str(message.text) == f.get('top'):
        if all_user_data[-1]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':

            await message.answer(f.get("size"), reply_markup=order_new)
        elif have_user_merki == 'yes':

            await message.answer(f.get("action"), reply_markup=order_old)
        await state.set_state(UserMenu.top)
    elif str(message.text) == f.get('back'):
        await message.answer(str(f.get('order')), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
