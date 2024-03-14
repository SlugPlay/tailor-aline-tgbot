from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import db
from stateMachine import *
from adminUser import acsess_files, admin_users
from func import check
from buttone.adminKB import admin_kb
router = Router()
global_phone_number = ''


def number_request():
    global global_phone_number
    return global_phone_number


@router.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await db.create_db()
    kb = [
        [types.KeyboardButton(text="Предоставить номер телефона", request_contact=True)],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    nomer = await message.answer('Просим предоставить номер телефона', reply_markup=keyboard)
    await state.set_state(UserState.centr)


@router.message(StateFilter(UserState.centr))
async def user_start1(message: types.Message, state: FSMContext):
    global user_info, all_user_data, global_phone_number

    if message.text:
        kb = [
            [types.KeyboardButton(text="Предоставить номер телефона", request_contact=True)],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        nomer = await message.answer('Просим предоставить номер телефона.\nНажмите на кнопку ниже', reply_markup=keyboard)
        await state.set_state(UserState.centr)
    else:
        user_info = []
        global_phone_number = str(message.contact.phone_number)
        if global_phone_number[0] != '+':
            global_phone_number = '+' + global_phone_number
        if global_phone_number in admin_users:
            status_user = db.check_admin(global_phone_number)
            try:
                if status_user[0] == 'ageUser':
                    vr_all_user_data = db.get_user(global_phone_number)
                    await db.edit_profile(user_id=vr_all_user_data[0], phone=global_phone_number, status='admin',
                                        first_name=vr_all_user_data[2], last_name=vr_all_user_data[3],
                                        age=vr_all_user_data[4], region=vr_all_user_data[5], size=vr_all_user_data[6],
                                        photo_front=vr_all_user_data[7], photo_back=vr_all_user_data[8],
                                        photo_profile=vr_all_user_data[9])
            except:
                pass
        data_users = await db.get_phone_status()
        flag1 = 'newUser'
        for i in range(len(data_users)):
            if global_phone_number == str(data_users[i][0]):
                flag1 = str(data_users[i][1])
        if flag1 == 'newUser':
            user_info.append(int(message.chat.id))
            user_info.append(global_phone_number)
            await message.answer(str(user_info[0]))
            await message.answer(str(user_info[1]))
            await db.create_profile(user_info[0], user_info[1], 'newUser')
            user_info.append('ageUser')
            await message.answer('Напишите ваше имя')
            await state.set_state(UserState.newUser)
        elif flag1 == 'ageUser':
            await state.set_state(UserState.ageUser)
            kb = [
                [types.KeyboardButton(text="В меню")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            all_user_data = db.get_user(global_phone_number)
            await message.answer('Добрый день, {first_name}'.format(first_name=all_user_data[2]), reply_markup=keyboard)
        elif flag1 == 'admin':
            all_user_data = db.get_user(global_phone_number)

            await message.answer("Открываю панель управления...\nбип-буп-бип", reply_markup=admin_kb)
            await state.set_state(UserState.admin)
        elif flag1 == 'black':
            await message.answer('Вас внесли в чёрный список за нарушение пункта ???')
            await state.set_state(UserState.ban_safe)


@router.message(StateFilter(UserState.ban_safe))
async def ban_safe(message: types.Message, state: FSMContext):
    await message.answer('Вас внесли в чёрный список за нарушение пункта ???')
    await state.set_state(UserState.ban_safe)


@router.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    if check(str(message.text), 'lang'):
        user_info.append(str(message.text))
        await message.answer('Напишите вашу фамилию')
        await state.set_state(UserReg.lastName)
    else:
        await message.answer('🥺Не похоже на имя. Попробуйте еще раз')
        await state.set_state(UserState.newUser)


@router.message(StateFilter(UserReg.lastName))
async def reg1(message: types.Message, state: FSMContext):
    if check(str(message.text), 'lang'):
        user_info.append(str(message.text))
        await message.answer('Напишите свой возраст')
        await state.set_state(UserReg.age)
    else:
        await message.answer('🥺Не похоже на фамилию. Попробуйте еще раз')
        await state.set_state(UserReg.lastName)


@router.message(StateFilter(UserReg.age))
async def regRegio(message: types.Message, state: FSMContext):
    if check(str(message.text), 'num'):
        user_info.append(str(message.text))
        kb = [
            [types.KeyboardButton(text="Санкт-Петербург"), types.KeyboardButton(text="Москва")],
            [types.KeyboardButton(text="Другой")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите свой регион", reply_markup=keyboard)
        await state.set_state(UserReg.regionAnother)
    else:
        await message.answer('🥺Не похоже на возраст. Попробуйте еще раз')
        await state.set_state(UserReg.age)


@router.message(StateFilter(UserReg.regionAnother))
async def reg2(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'другой':
        await message.answer('Выберите свой регион', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserReg.regionAnother)
    else:
        user_info.append(str(message.text))
        kb = [
            [types.KeyboardButton(text="40"), types.KeyboardButton(text="42"),
             types.KeyboardButton(text="44"), types.KeyboardButton(text="46")],
            [types.KeyboardButton(text="48"), types.KeyboardButton(text="50"),
             types.KeyboardButton(text="52"), types.KeyboardButton(text="54")]



        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Какой размер одежды вы носите?", reply_markup=keyboard)
        await state.set_state(UserReg.clothingSize)


@router.message(StateFilter(UserReg.clothingSize))
async def reg3(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    kb = [
        [types.KeyboardButton(text="Пропустить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Загрузите фото в полный рост спереди', reply_markup=keyboard)
    await state.set_state(UserReg.photoFront)


@router.message(StateFilter(UserReg.photoFront))
async def reg4(message: types.Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        user_info.append(str(file_id) + '/pic')
        await message.answer('Загрузите фото в полный рост сзади')
        await state.set_state(UserReg.photoBack)
    elif message.document:
        if str(message.document.mime_type) in acsess_files:
            file_id = message.document.file_id
            user_info.append(str(file_id) + '/doc')
            await message.answer('Загрузите фото в полный рост сзади')
            await state.set_state(UserReg.photoBack)
        else:
            await message.answer(
                '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
            await state.set_state(UserReg.photoFront)
    elif str(message.text).lower() == 'пропустить':
        user_info.append('')
        kb = [
            [types.KeyboardButton(text="Пропустить")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Загрузите фото в полный рост сзади', reply_markup=keyboard)
        await state.set_state(UserReg.photoBack)
    else:
        await message.answer(
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoFront)


@router.message(StateFilter(UserReg.photoBack))
async def reg5(message: types.Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        user_info.append(str(file_id) + '/pic')
        await message.answer('Загрузите фото в полный рост в профиль')
        await state.set_state(UserReg.photoProfile)
    elif message.document:
        if str(message.document.mime_type) in acsess_files:
            file_id = message.document.file_id
            user_info.append(str(file_id) + '/doc')
            await message.answer('Загрузите фото в полный рост в профиль')
            await state.set_state(UserReg.photoProfile)
        else:
            await message.answer(
                '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
            await state.set_state(UserReg.photoBack)
    elif str(message.text).lower() == 'пропустить':
        user_info.append('')
        kb = [
            [types.KeyboardButton(text="Пропустить")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Загрузите фото в полный рост в профиль', reply_markup=keyboard)
        await state.set_state(UserReg.photoProfile)
    else:
        await message.answer(
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoBack)


@router.message(StateFilter(UserReg.photoProfile))
async def reg6(message: types.Message, state: FSMContext):
    global all_user_data

    if message.photo:
        file_id = message.photo[-1].file_id
        user_info.append(str(file_id) + '/pic')
        user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile = user_info
        await db.edit_profile(user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back,
                              photo_profile)
        kb = [
            [types.KeyboardButton(text="В меню")],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        all_user_data = db.get_user(phone)
        await message.answer('Регистрация завершена')
        await message.answer('Добрый день, {first_name1}'.format(first_name1=all_user_data[2]), reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    elif message.document:
        if str(message.document.mime_type) in acsess_files:
            file_id = message.document.file_id
            user_info.append(str(file_id) + '/doc')
            user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile = user_info
            await db.edit_profile(user_id, phone, status, first_name, last_name, age, region, size, photo_front,
                                  photo_back,
                                  photo_profile)
            kb = [
                [types.KeyboardButton(text="В меню")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            all_user_data = db.get_user(phone)
            await message.answer('Регистрация завершена')
            await message.answer('Добрый день, {first_name1}'.format(first_name1=all_user_data[2]),
                                 reply_markup=keyboard)
            await state.set_state(UserState.ageUser)
        else:
            await message.answer(
                '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
            await state.set_state(UserReg.photoProfile)
    elif str(message.text).lower() == 'пропустить':
        user_info.append('')
        user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile = user_info
        await db.edit_profile(user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back,
                              photo_profile)
        kb = [
            [types.KeyboardButton(text="В меню")],

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        all_user_data = db.get_user(phone)
        await message.answer('Регистрация завершена')
        await message.answer('Добрый день, {first_name1}'.format(first_name1=all_user_data[2]), reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer(
            '🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoProfile)
