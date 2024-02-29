from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from tailor_aline_tgbot.stateMachine import *
from tailor_aline_tgbot.adminUser import acsess_files
from tailor_aline_tgbot.func import check
from tailor_aline_tgbot.globall import *
from tailor_aline_tgbot import db
from tailor_aline_tgbot.photos import photo_1, photo_7, photo_9, photo_16

router = Router()


@router.message(StateFilter(UserMenu.underSkirt))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt
    if str(message.text).lower() == 'использовать старые мерки':
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text).lower() == 'сделаем мерки':
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
        kb = [
            [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
            [types.KeyboardButton(text="Хочу заказать низ Юбка")],
            [types.KeyboardButton(text="Хочу заказать низ Брюки")],
            [types.KeyboardButton(text="Связаться с менеджером")],
            [types.KeyboardButton(text="Зарегистрироваться заново")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Что вы хотите заказать?", reply_markup=keyboard)
        await state.set_state(UserMenu.menu)


@router.message(StateFilter(UserMenu.orderUnderSkirt))
async def under1(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
            [types.KeyboardButton(text="Хочу заказать низ Юбка")],
            [types.KeyboardButton(text="Хочу заказать низ Брюки")],
            [types.KeyboardButton(text="Связаться с менеджером")],
            [types.KeyboardButton(text="Зарегистрироваться заново")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Что вы хотите заказать?", reply_markup=keyboard)
        await state.set_state(UserMenu.menu)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step1)


@router.message(StateFilter(UserSize.step1))
async def under2(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step2)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step1)


@router.message(StateFilter(UserSize.step2))
async def under3(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step3)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step2)


@router.message(StateFilter(UserSize.step3))
async def under4(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_7, 'Длина изделия')
        await state.set_state(UserSize.step3_5)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step3)


@router.message(StateFilter(UserSize.step3_5))
async def under5(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step4)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
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
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step4)
    else:
        await message.answer('Фото получены')
        db.input_merki(merki_skirt, 'skirt', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
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
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserMenu.orderSkirt)
    else:
        await message.answer('Фото получены')
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        # Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.',
                             reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
