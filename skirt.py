from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from stateMachine import *
from adminUser import acsess_files
from func import check, request_buy
from photos import *
from menuStart import number_request
import db
from aiogram.types import FSInputFile
from buttone.menuKB import menu_kb
import json

file = open("TXT.json", 'r', encoding='utf-8')
f = json.load(file)

router = Router()


@router.message(StateFilter(UserMenu.underSkirt))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt, global_phone_number, all_user_data

    global_phone_number = number_request()
    all_user_data = db.get_user(global_phone_number)
    if str(message.text) == f.get('oldSIze'):
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text) == f.get('standartSize'):
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text) == f.get('makeSize'):
        merki_skirt = ''
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderUnderSkirt)
    elif str(message.text).lower() == 'назад':
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.orderUnderSkirt))
async def under1(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        await message.answer(f.get('order'), reply_markup=menu_kb)
        await state.set_state(UserMenu.menu)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step1)


@router.message(StateFilter(UserSize.step1))
async def under2(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt = 'Обхват талии: ' + str(message.text) + '\n'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step2)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step1)


@router.message(StateFilter(UserSize.step2))
async def under3(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt = 'Обхват бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step3)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step2)


@router.message(StateFilter(UserSize.step3))
async def under4(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt = 'Высота бедер: ' + str(message.text) + '\n'
        await message.answer_photo(photo_7, 'Длина изделия')
        await state.set_state(UserSize.step3_5)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step3)


@router.message(StateFilter(UserSize.step3_5))
async def under5(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt = 'Длина изделия: ' + str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step4)
    else:
        await message.answer(f.get('parametrCheck'))
        await state.set_state(UserSize.step3_5)




@router.message(StateFilter(UserSize.step4),
                F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under6(message: types.Message, state: FSMContext, album: list[Message]):
    global merki_skirt, all_user_data
    
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
        await state.set_state(UserSize.step4)
    else:
        await message.answer('Фото получены')
        db.input_merki(merki_skirt, 'skirt', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
        await request_buy('Низ - Юбка', all_user_data, db.get_admin_data(), merki_skirt, 'individual', media_group)
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@router.message(StateFilter(UserMenu.orderSkirt),
                F.content_type.in_(
                    [ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT, ContentType.TEXT]))
async def under7(message: types.Message, state: FSMContext, album: list[Message]):
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
        await state.set_state(UserMenu.orderSkirt)
    else:
        await message.answer('Фото получены')
        await request_buy('Низ - Юбка', all_user_data, db.get_admin_data(), all_user_data[6], 'standart', media_group)
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.',
                             reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
