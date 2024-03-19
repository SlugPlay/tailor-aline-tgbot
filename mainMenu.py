from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from adminUser import admin_users
from stateMachine import *
from menuStart import number_request
import db
from buttone.menuKB import menu_kb
from buttone.clothes import clothes_kb
from buttone.order_new import order_new
from buttone.order_old import order_old
from buttone.adminKB import admin_kb
import json
router = Router()


global_phone_number = number_request()
file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)


@router.message(StateFilter(UserState.ageUser))
async def menu2(message: types.Message, state: FSMContext):
    await message.answer(str(f.get('order')), reply_markup=menu_kb)
    await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.menu))
async def menedq(message: types.Message, state: FSMContext):
    global global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    have_user_merki = 'no'
    if str(message.text) == f.get('menedger'):
        kb = [
            [types.KeyboardButton(text="Назад")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f.get('problem'), reply_markup=keyboard)
        await state.set_state(UserReg.problem)
    elif str(message.text) == f.get('clothes'):
        await message.answer(str(f.get('order')), reply_markup=clothes_kb)
        await state.set_state(UserSize.step31)
    elif str(message.text) == f.get('perereg'):
        kb = [
            [types.KeyboardButton(text="Да")],
            [types.KeyboardButton(text="Нет")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(f.get("perereg"), reply_markup=keyboard)
        await state.set_state(UserMenu.registration_again)
    # elif str(message.text).lower() == 'вернуться в панель админа' and global_phone_number in admin_users:
    #     await message.answer("Открываю панель управления...\nбип-буп-бип", reply_markup=admin_kb)
    #     await state.set_state(UserState.admin)


@router.message(StateFilter(UserMenu.registration_again))
async def perereg(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'да':
        db.delete_user(global_phone_number)
        kb = [
            [types.KeyboardButton(text=f.get("number"), request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        nomer = await message.answer(f.get("getNumber"), reply_markup=keyboard)
        await state.set_state(UserState.centr)
    else:
        await message.answer(f.get("repeatMenu"))

        await message.answer(f.get("order"), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
