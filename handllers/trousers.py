from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from stateMachine import *
from adminUser import acsess_files
from func import check, request_buy
from handllers.menuStart import number_request
import db
from photos import photo_1, photo_4, photo_6, photo_9, photo_16
from buttone.menuKB import menu_kb
import json
router = Router()

file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)

@router.message(StateFilter(UserMenu.underTrousers))
async def under8(message: types.Message, state: FSMContext):
    global global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    if str(message.text) == f.get('oldSize'):
        global merki_pants
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text) == f.get('standartSize'):
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text) == f.get('makeSize'):
        merki_pants = ''
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderUnderTrousers)
    elif str(message.text).lower() == 'назад':
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.orderUnderTrousers))
async def under9(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
    else:
        print('work')
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step23)


@router.message(StateFilter(UserSize.step23))
async def under10(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants = 'Обхват талии: ' + str(message.text) + '\n'

        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step24)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step23)


@router.message(StateFilter(UserSize.step24))
async def under11(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants = 'Обхват бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step25)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step24)


@router.message(StateFilter(UserSize.step25))
async def under12(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants = 'Высота бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_4, 'Высота сиденья')
        await state.set_state(UserSize.step26)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step25)


@router.message(StateFilter(UserSize.step26))
async def under13(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants = 'Высота сиденья: ' + str(message.text) + '\n'
        await message.answer_photo(photo_6, 'Длина брюк по боку')
        await state.set_state(UserSize.step27)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step26)


@router.message(StateFilter(UserSize.step27))
async def under14(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants = 'Длина брюк по боку: ' + str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step28)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step27)


@router.message(StateFilter(UserSize.step28),
                F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under15(message: types.Message, state: FSMContext, album: list[Message]):
    global merki_pants, all_user_data

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
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step28)
    else:
        await message.answer('Фото получены')
        db.input_merki(merki_pants, 'pants', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
        await request_buy('Низ - Брюки', all_user_data, db.get_admin_data(), merki_pants, 'individual', media_group)
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@router.message(StateFilter(UserMenu.orderTrousers),
                F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under16(message: types.Message, state: FSMContext, album: list[Message]):
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
            f.get('fileCheck')
        )
        media_group = []
        await state.set_state(UserMenu.orderTrousers)
    else:
        await message.answer('Фото получены')
        await request_buy('Низ - Брюки', all_user_data, db.get_admin_data(), all_user_data[6], 'standart', media_group)
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.',
                             reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
