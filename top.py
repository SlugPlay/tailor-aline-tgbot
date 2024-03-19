from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from stateMachine import *
from adminUser import acsess_files
from func import check, request_buy
from menuStart import number_request
import db
from aiogram.types import FSInputFile
from buttone.menuKB import menu_kb
import json
from photos import *

router = Router()

file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)


@router.message(StateFilter(UserMenu.top))
async def under17(message: types.Message, state: FSMContext):
    global merki_up, global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    if str(message.text) == f.get('oldSize'):
        await message.answer(f.get("product"), reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTop)
    elif str(message.text) == f.get('standartSize'):
        await message.answer(f.get("product"), reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTop)
    elif str(message.text) == f.get('makeSize'):
        merki_up = ''
        kb = [
            [types.KeyboardButton(text=f.get("start"))],
            [types.KeyboardButton(text = f.get("menu"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            f.get("menu"),
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderTopVse)
    elif str(message.text) == f.get("back"):
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.orderTopVse))
async def under18(message: types.Message, state: FSMContext):
    if str(message.text) == f.get("menu"):
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
    else:
        await message.answer_photo(photo_17, 'Обхват шеи', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step5)


@router.message(StateFilter(UserSize.step5))
async def under19(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват шеи: ' + str(message.text) + '\n'
        await message.answer_photo(photo_10, 'Обхват груди 1')
        await state.set_state(UserSize.step6)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step5)


@router.message(StateFilter(UserSize.step6))
async def under20(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват груди 1: ' + str(message.text) + '\n'
        await message.answer_photo(photo_12, 'Обхват груди 2')
        await state.set_state(UserSize.step7)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step6)


@router.message(StateFilter(UserSize.step7))
async def under21(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват груди 2: ' + str(message.text) + '\n'
        await message.answer_photo(photo_13, 'Обхват груди 3')
        await state.set_state(UserSize.step8)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step7)


@router.message(StateFilter(UserSize.step8))
async def under22(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват груди 3: ' + str(message.text) + '\n'
        await message.answer_photo(photo_18, 'Центр груди')
        await state.set_state(UserSize.step9)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step8)


@router.message(StateFilter(UserSize.step9))
async def under23(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Центр груди: ' + str(message.text) + '\n'
        await message.answer_photo(photo_2, 'Высота груди')
        await state.set_state(UserSize.step10)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step9)


@router.message(StateFilter(UserSize.step10))
async def under24(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Высота груди: ' + str(message.text) + '\n'
        await message.answer_photo(photo_19, 'Ширина плеча')
        await state.set_state(UserSize.step11)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step10)


@router.message(StateFilter(UserSize.step11))
async def under25(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Ширина плеча: ' + str(message.text) + '\n'
        await message.answer_photo(photo_15, 'Обхват плеча')
        await state.set_state(UserSize.step12)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step11)


@router.message(StateFilter(UserSize.step12))
async def under26(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват плеча: ' + str(message.text) + '\n'
        await message.answer_photo(photo_14, 'Обхват запястья')
        await state.set_state(UserSize.step13)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step12)


@router.message(StateFilter(UserSize.step13))
async def under27(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват запястья: ' + str(message.text) + '\n'
        await message.answer_photo(photo_20, 'Длина рукава')
        await state.set_state(UserSize.step14)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step13)


@router.message(StateFilter(UserSize.step14))
async def under28(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Длина рукава: ' + str(message.text) + '\n'
        await message.answer_photo(photo_16, 'Обхват талии')
        await state.set_state(UserSize.step15)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step14)


@router.message(StateFilter(UserSize.step15))
async def under29(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват талии: ' + str(message.text) + '\n'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step16)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step15)


@router.message(StateFilter(UserSize.step16))
async def under30(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Обхват бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step17)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step16)


@router.message(StateFilter(UserSize.step17))
async def under31(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Высота бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_11, 'Ширина спины')
        await state.set_state(UserSize.step18)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step17)


@router.message(StateFilter(UserSize.step18))
async def under32(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Ширина спины: ' + str(message.text) + '\n'
        await message.answer_photo(photo_8, 'Длина спины до талии')
        await state.set_state(UserSize.step19)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step18)


@router.message(StateFilter(UserSize.step19))
async def under33(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Длина спины до талии: ' + str(message.text) + '\n'
        await message.answer_photo(photo_8, 'Длина переда до талии')
        await state.set_state(UserSize.step20)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step19)


@router.message(StateFilter(UserSize.step20))
async def under34(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Длина переда до талии: ' + str(message.text) + '\n'
        await message.answer_photo(photo_8, 'Длина изделия')
        await state.set_state(UserSize.step21)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step20)


@router.message(StateFilter(UserSize.step21))
async def under35(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up = 'Длина изделия: ' + str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step22)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step21)


@router.message(StateFilter(UserSize.step22),
                F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under36(message: types.Message, state: FSMContext, album: list[Message]):
    global merki_up, all_user_data

    flag_unknown_media = False
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(str(file_id) + '/pic')
        elif str(msg.document.mime_type) in acsess_files:
            file_id = msg.document.file_id
            media_group.append(str(file_id) + '/doc')
        else:
            flag_unknown_media = True
    if flag_unknown_media:
        await message.answer(
            f.get('fileCheck'))
        media_group = []
        await state.set_state(UserSize.step22)
    else:
        await message.answer(f.get("photoComplete"))
        merki_up += str(message.text)
        db.input_merki(merki_up, 'up', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
        await request_buy('Верх', all_user_data, db.get_admin_data(), merki_up, 'individual', media_group)
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f.get("please"), reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@router.message(StateFilter(UserMenu.orderTop),
                F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under37(message: types.Message, state: FSMContext, album: list[Message]):
    flag_unknown_media = False
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(str(file_id) + '/pic')
        elif str(msg.document.mime_type) in acsess_files:
            file_id = msg.document.file_id
            media_group.append(str(file_id) + '/doc')
        else:
            flag_unknown_media = True
    if flag_unknown_media:
        await message.answer(
            f.get('fileCheck'))
        media_group = []
        await state.set_state(UserMenu.orderTop)
    else:
        await message.answer(f.get("photoComplete"))
        await request_buy('Верх', all_user_data, db.get_admin_data(), all_user_data[6], 'standart', media_group)
        kb = [
            [types.KeyboardButton(text=f.get("menu"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f.get("please"),
                             reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
