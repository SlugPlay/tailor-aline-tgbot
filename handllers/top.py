from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from tailor_aline_tgbot.stateMachine import *
from tailor_aline_tgbot.adminUser import acsess_files
from tailor_aline_tgbot.func import check
from tailor_aline_tgbot.globall import *
from tailor_aline_tgbot import db
from tailor_aline_tgbot.photos import photo_1, photo_2, photo_8, photo_9, \
    photo_10, photo_11, \
    photo_12, photo_13, photo_14, photo_15, photo_17, photo_18, photo_19, photo_20, photo_16

router = Router()


@router.message(StateFilter(UserMenu.top))
async def under17(message: types.Message, state: FSMContext):
    global merki_up
    if str(message.text).lower() == 'использовать старые мерки':
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTop)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.orderTop)
    elif str(message.text).lower() == 'сделаем мерки':
        merki_up = ''
        kb = [
            [types.KeyboardButton(text="Начать")],
            [types.KeyboardButton(text="Меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Пожалуйста, измерьте фигуру самостоятельно или при помощи другого человека, следуя инструкции.",
            reply_markup=keyboard)
        await state.set_state(UserMenu.orderTopVse)
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


@router.message(StateFilter(UserMenu.orderTopVse))
async def under18(message: types.Message, state: FSMContext):
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
        await message.answer_photo(photo_17, 'Обхват шеи', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step5)


@router.message(StateFilter(UserSize.step5))
async def under19(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_10, 'Обхват груди 1')
        await state.set_state(UserSize.step6)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step5)


@router.message(StateFilter(UserSize.step6))
async def under20(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_12, 'Обхват груди 2')
        await state.set_state(UserSize.step7)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step6)


@router.message(StateFilter(UserSize.step7))
async def under21(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_13, 'Обхват груди 3')
        await state.set_state(UserSize.step8)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step7)


@router.message(StateFilter(UserSize.step8))
async def under22(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_18, 'Центр груди')
        await state.set_state(UserSize.step9)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step8)


@router.message(StateFilter(UserSize.step9))
async def under23(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_2, 'Высота груди')
        await state.set_state(UserSize.step10)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step9)


@router.message(StateFilter(UserSize.step10))
async def under24(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_19, 'Ширина плеча')
        await state.set_state(UserSize.step11)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step10)


@router.message(StateFilter(UserSize.step11))
async def under25(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_15, 'Обхват плеча')
        await state.set_state(UserSize.step12)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step11)


@router.message(StateFilter(UserSize.step12))
async def under26(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_14, 'Обхват запястья')
        await state.set_state(UserSize.step13)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step12)


@router.message(StateFilter(UserSize.step13))
async def under27(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_20, 'Длина рукава')
        await state.set_state(UserSize.step14)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step13)


@router.message(StateFilter(UserSize.step14))
async def under28(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_16, 'Обхват талии')
        await state.set_state(UserSize.step15)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step14)


@router.message(StateFilter(UserSize.step15))
async def under29(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step16)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step15)


@router.message(StateFilter(UserSize.step16))
async def under30(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step17)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step16)


@router.message(StateFilter(UserSize.step17))
async def under31(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_11, 'Ширина спины')
        await state.set_state(UserSize.step18)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step17)


@router.message(StateFilter(UserSize.step18))
async def under32(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина спины до талии')
        await state.set_state(UserSize.step19)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step18)


@router.message(StateFilter(UserSize.step19))
async def under33(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина переда до талии')
        await state.set_state(UserSize.step20)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step19)


@router.message(StateFilter(UserSize.step20))
async def under34(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина изделия')
        await state.set_state(UserSize.step21)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step20)


@router.message(StateFilter(UserSize.step21))
async def under35(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step22)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
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
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step22)
    else:
        await message.answer('Фото получены')
        merki_up += str(message.text)
        db.input_merki(merki_up, 'up', global_phone_number)
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
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserMenu.orderTop)
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
