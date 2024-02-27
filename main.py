import asyncio
import logging
import json
import db
import re

from typing import Callable, Any, Awaitable, Union
from aiogram import Bot, Dispatcher, types, fsm, filters, F, BaseMiddleware
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, InputMediaPhoto, InputMedia, ContentType


file = open('bot_token.json', 'r')
data = json.load(file).get('token')
bot = Bot(token=str(data))
acsess_files = ['image/jpg', 'image/jpeg', 'image/png']
admin_users = ['+79140043418']

def check(text, type):
    if type == 'lang':
        regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
        pattern = re.compile(regex)
        return pattern.search(text) is not None
    if type == 'num':
        return text.isdigit()

# --------------------------------------------- photo-------------------------------------------
photo_1 = FSInputFile("photo_bot/Высота бедер.jpg")
photo_2 = FSInputFile("photo_bot/Высота груди.jpg")
photo_3 = FSInputFile("photo_bot/Высота переда до талии.jpg")
photo_4 = FSInputFile("photo_bot/Высота сиденья.jpg")
photo_5 = FSInputFile("photo_bot/Длина изделия (низ)(1).jpg")
photo_6 = FSInputFile("photo_bot/Длина изделия (низ).jpg")
photo_7 = FSInputFile("photo_bot/Длина изделия_.jpg")
photo_8 = FSInputFile("photo_bot/Длина спины до талии.jpg")
photo_9 = FSInputFile("photo_bot/Обхват бедер.jpg")
photo_10 = FSInputFile("photo_bot/Обхват груди 1.jpg")
photo_11 = FSInputFile("photo_bot/Ширина спины.jpg")
photo_12 = FSInputFile("photo_bot/Обхват груди 2.jpg")
photo_13 = FSInputFile("photo_bot/Обхват груди 3.jpg")
photo_14 = FSInputFile("photo_bot/Обхват запястья.jpg")
photo_15 = FSInputFile("photo_bot/Обхват плеча.jpg")
photo_16 = FSInputFile("photo_bot/Обхват талии.jpg")
photo_17 = FSInputFile("photo_bot/Обхват шеи.jpg")
photo_18 = FSInputFile("photo_bot/Центр груди.jpg")
photo_19 = FSInputFile("photo_bot/Ширина плеча_.jpg")
photo_20 = FSInputFile("photo_bot/Длина рукава.jpg")
# --------------------------------------------- photo-------------------------------------------
flag1 = ''

# Диспетчер
dp = Dispatcher()
recInformation = ''


class UserState(StatesGroup):
    centr = State()
    newUser = State()
    ageUser = State()
    admin = State()


mes = [0]


class UserSize(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step3_5 = State()
    step4 = State()
    step5 = State()
    step6 = State()
    step7 = State()
    step8 = State()
    step9 = State()
    step10 = State()
    step11 = State()
    step12 = State()
    step13 = State()
    step14 = State()
    step15 = State()
    step16 = State()
    step17 = State()
    step18 = State()
    step19 = State()
    step20 = State()
    step21 = State()
    step22 = State()
    step23 = State()
    step24 = State()
    step25 = State()
    step26 = State()
    step27 = State()
    step28 = State()
    step29 = State()
    step30 = State()


class UserReg(StatesGroup):
    name = State()
    lastName = State()
    age = State()
    region = State()
    regionAnother = State()
    clothingSize = State()
    photoFront = State()
    photoBack = State()
    photoProfile = State()


class UserAdmin(StatesGroup):
    menu = State()


class UserMenu(StatesGroup):
    menu = State()
    meneg = State()
    registration_again = State()
    underSkirt = State()
    underTrousers = State()
    top = State()
    orderTopVse = State()
    orderSkirt = State()
    orderTrousers = State()
    orderUnderTrousers = State()
    orderUnderSkirt = State()
    orderTop = State()


class SomeMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']


dp.message.middleware(SomeMiddleware())


# --------------------------------------------- тестовая полигон -------------------------------------------------------------------------------------
# -----------------(пускай здесь повисит, чтобы тестить всякие штуки (я уже потеститл, если надо забирай)) -------------------------------------------

class UserTest(StatesGroup):
    test1 = State()
    test2 = State()

@dp.message(Command('test'))
async def user_test(message: types.Message, state: FSMContext):
    await message.answer('Отправь файл')
    await message.answer(str(message.message_id))
    await message.answer('Отправь файл2')
    await message.answer(str(message.message_id))
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(UserTest.test1)


@dp.message(StateFilter(UserTest.test1))
async def reg(message: types.Message, state: FSMContext):
    await message.answer(str(message.message_id))
    await message.answer('подходит')
    await message.answer(str(message.message_id))
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(UserTest.test1)

# --------------------------------------------- тестовая полигон -------------------------------------------------------------------------------------
# -----------------(пускай здесь повисит, чтобы тестить всякие штуки (я уже потеститл, если надо забирай)) -------------------------------------------

# --------------------------------------------- регистрация -------------------------------------------
@dp.message(Command('start'))
async def user_start(message: types.Message, state: FSMContext):
    await db.create_db()
    kb = [
            [types.KeyboardButton(text="Предоставить номер телефона", request_contact=True)],

        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    nomer = await message.answer('Просим предоставить номер телефона', reply_markup=keyboard)
    await state.set_state(UserState.centr)

@dp.message(StateFilter(UserState.centr))
async def user_start(message: types.Message, state: FSMContext):
    global user_info, all_user_data, global_phone_number

    user_info = []
    global_phone_number = str(message.contact.phone_number)
    if global_phone_number in admin_users:
        status_user = db.check_admin(global_phone_number)
        if status_user[0] == 'ageUser':
            vr_all_user_data = db.get_user(global_phone_number)
            await db.edit_profile(user_id=vr_all_user_data[0], phone=global_phone_number, status='admin', first_name=vr_all_user_data[2], last_name=vr_all_user_data[3], age=vr_all_user_data[4], region=vr_all_user_data[5], size=vr_all_user_data[6], photo_front=vr_all_user_data[7], photo_back=vr_all_user_data[8], photo_profile=vr_all_user_data[9])
    data_users = await db.get_phone_status()
    flag1 = 'newUser'
    for i in range(len(data_users)):
        if global_phone_number == str(data_users[i][0]):
            flag1 = str(data_users[i][1])
    if flag1 == 'newUser':
        user_info.append(int(message.chat.id))
        user_info.append(global_phone_number)
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
        kb = [
            [types.KeyboardButton(text="Получить список всех пользователей")],
            [types.KeyboardButton(text="Вывести все заявки")],
            [types.KeyboardButton(text="В меню")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Открываю панель управления...\nбип-буп-бип", reply_markup=keyboard)
        await state.set_state(UserState.admin)


@dp.message(StateFilter(UserState.newUser))
async def reg(message: types.Message, state: FSMContext):
    if check(str(message.text), 'lang'):
        user_info.append(str(message.text))
        await message.answer('Напишите вашу фамилию')
        await state.set_state(UserReg.lastName)
    else:
        await message.answer('🥺Не похоже на имя. Попробуйте еще раз')
        await state.set_state(UserState.newUser)

@dp.message(StateFilter(UserReg.lastName))
async def reg(message: types.Message, state: FSMContext):
    if check(str(message.text), 'lang'):
        user_info.append(str(message.text))
        await message.answer('Напишите свой возраст')
        await state.set_state(UserReg.age)
    else:
        await message.answer('🥺Не похоже на фамилию. Попробуйте еще раз')
        await state.set_state(UserReg.lastName)


@dp.message(StateFilter(UserReg.age))
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


@dp.message(StateFilter(UserReg.regionAnother))
async def reg(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'другой':
        await message.answer('Выберите свой регион', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserReg.regionAnother)
    else:
        user_info.append(str(message.text))
        kb = [
            [types.KeyboardButton(text="40"), types.KeyboardButton(text="41"),
             types.KeyboardButton(text="42"), types.KeyboardButton(text="43")],
            [types.KeyboardButton(text="44"), types.KeyboardButton(text="45"),
             types.KeyboardButton(text="46"), types.KeyboardButton(text="47")],
            [types.KeyboardButton(text="48"), types.KeyboardButton(text="49"),
             types.KeyboardButton(text="50"), types.KeyboardButton(text="51")],
            [types.KeyboardButton(text="52"), types.KeyboardButton(text="53"),
             types.KeyboardButton(text="54"), types.KeyboardButton(text="55"), types.KeyboardButton(text="55")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Какой размер одежды вы носите?", reply_markup=keyboard)
        await state.set_state(UserReg.clothingSize)


@dp.message(StateFilter(UserReg.clothingSize))
async def reg(message: types.Message, state: FSMContext):
    user_info.append(str(message.text))
    kb = [
        [types.KeyboardButton(text="Пропустить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Загрузите фото в полный рост спереди', reply_markup=keyboard)
    await state.set_state(UserReg.photoFront)


@dp.message(StateFilter(UserReg.photoFront))
async def reg(message: types.Message, state: FSMContext):
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
            await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoFront)



@dp.message(StateFilter(UserReg.photoBack))
async def reg(message: types.Message, state: FSMContext):
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
            await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoBack)


@dp.message(StateFilter(UserReg.photoProfile))
async def reg(message: types.Message, state: FSMContext):
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
            await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        await state.set_state(UserReg.photoProfile)


# --------------------------------------------- регистрация ------------------------------------
# --------------------------------------------- админ ------------------------------------
@dp.message(StateFilter(UserState.admin))
async def menu(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'в меню':
        kb = [
            [types.KeyboardButton(text="Хочу заказать верх (Платье, блузка, жакет, рубашка)")],
            [types.KeyboardButton(text="Хочу заказать низ Юбка")],
            [types.KeyboardButton(text="Хочу заказать низ Брюки")],
            [types.KeyboardButton(text="Связаться с менеджером")],
            [types.KeyboardButton(text="Зарегистрироваться заново")],
            [types.KeyboardButton(text="Вернуться в панель админа")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Что вы хотите заказать?", reply_markup=keyboard)
        await state.set_state(UserMenu.menu)


@dp.message(StateFilter(UserAdmin.menu))
async def menu(message: types.Message, state: FSMContext):
    pass
    

# --------------------------------------------- админ ------------------------------------
# --------------------------------------------- меню -------------------------------------------
@dp.message(StateFilter(UserState.ageUser))
async def menu(message: types.Message, state: FSMContext):
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


@dp.message(StateFilter(UserMenu.menu))
async def menedq(message: types.Message, state: FSMContext):
    have_user_merki = 'no'
    if str(message.text).lower() == 'связаться с менеджером':
        await message.answer('Введите текст проблемы, и с вами свяжется менеджер',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserMenu.meneg)
    elif str(message.text).lower() == 'хочу заказать низ юбка':
        if all_user_data[-3]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underSkirt)
    elif str(message.text).lower() == 'хочу заказать низ брюки':
        if all_user_data[-2]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],

            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.underTrousers)
    elif str(message.text).lower() == 'хочу заказать верх (платье, блузка, жакет, рубашка)':
        if all_user_data[-1]:
            have_user_merki = 'yes'
        if have_user_merki == 'no':
            kb = [
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Давайте снимим с вас мерки", reply_markup=keyboard)
        elif have_user_merki == 'yes':
            kb = [
                [types.KeyboardButton(text="Использовать старые мерки")],
                [types.KeyboardButton(text="Сделаем мерки")],
                [types.KeyboardButton(text="Стандартный размер")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer("Выберите действие", reply_markup=keyboard)
        await state.set_state(UserMenu.top)
    elif str(message.text).lower() == 'зарегистрироваться заново':
        kb = [
            [types.KeyboardButton(text="Да")],
            [types.KeyboardButton(text="Нет")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Вы точно хотите пройти процесс регистрации заново?', reply_markup=keyboard)
        await state.set_state(UserMenu.registration_again)
    elif str(message.text).lower() == 'вернуться в панель админа' and global_phone_number in admin_users:
        kb = [
            [types.KeyboardButton(text="Получить список всех пользователей")],
            [types.KeyboardButton(text="Вывести все заявки")],
            [types.KeyboardButton(text="В меню")]

        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Открываю панель управления...\nбип-буп-бип", reply_markup=keyboard)
        await state.set_state(UserState.admin)


@dp.message(StateFilter(UserMenu.registration_again))
async def perereg(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'да':
        db.delete_user(global_phone_number)
        kb = [
            [types.KeyboardButton(text="Предоставить номер телефона", request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        nomer = await message.answer('Здравствуйте, предоставьте свой номер телефона', reply_markup=keyboard)
        await state.set_state(UserState.centr)
    else:
        await message.answer("Возвращаю вас в меню...")
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



# --------------------------------------------- меню -------------------------------------------
# --------------------------------------------- менеджер ---------------------------------------
@dp.message(StateFilter(UserMenu.meneg))
async def problem(message: types.Message, state: FSMContext):
    global all_user_data

    admin_data = db.get_admin_data()
    for i in admin_data:
        await bot.send_message(i, "Новое обращение с вопросом!\nПользователь номер: {}\nНомер телефона: {}\nИмя: {}\nФамилия: {}\nВозраст: {}\nРегион: {}\nРазмер: {}\n".format(all_user_data[0], all_user_data[1], all_user_data[2], all_user_data[3], all_user_data[4], all_user_data[5], all_user_data[6]))
        if all_user_data[7][:-3] == 'pic':
            await bot.send_photo(i, all_user_data[7][:-4], caption='Фото спереди:')
        else:
            await bot.send_document(i, all_user_data[7][:-4], caption='Фото спереди:')
        if all_user_data[8][:-3] == 'pic':
            await bot.send_photo(i, all_user_data[8][:-4], caption='Фото сзади:')
        else:
            await bot.send_document(i, all_user_data[8][:-4], caption='Фото сзади:')
        if all_user_data[9][:-3] == 'pic':
            await bot.send_photo(i, all_user_data[9][:-4], caption='Фото в профиль:')
        else:
            await bot.send_document(i, all_user_data[9][:-4], caption='Фото в профиль:')
        await bot.send_message(i, 'Текст проблемы:')
        await bot.forward_message(i, message.chat.id, message.message_id)
    kb = [
        [types.KeyboardButton(text="В меню")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Менеджер свяжется с вами в течении 1 часа', reply_markup=keyboard)
    await state.set_state(UserState.ageUser)


# --------------------------------------------- менеджер ---------------------------------------
# --------------------------------------------- низ юбка --------------------------------------------
@dp.message(StateFilter(UserMenu.underSkirt))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt

    print(str(message.text))
    if str(message.text).lower() == 'использовать старые мерки':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderSkirt)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
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


@dp.message(StateFilter(UserMenu.orderUnderSkirt))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step1)


@dp.message(StateFilter(UserSize.step1))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step2)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step1)


@dp.message(StateFilter(UserSize.step2))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step3)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step2)


@dp.message(StateFilter(UserSize.step3))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        merki_skirt += '/'
        await message.answer_photo(photo_7, 'Длина изделия')
        await state.set_state(UserSize.step3_5)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step3)

@dp.message(StateFilter(UserSize.step3_5))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt

    if check(str(message.text), 'num'):
        merki_skirt += str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step4)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step3_5)


@dp.message(StateFilter(UserSize.step4), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step4)
    else:
        await message.answer('Фото получены')
        db.input_merki(merki_skirt, 'skirt', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderSkirt), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserMenu.orderSkirt)
    else:
        await message.answer('Фото получены')
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    

# --------------------------------------------- низ юбка --------------------------------------------
# --------------------------------------------- низ брюки --------------------------------------------
@dp.message(StateFilter(UserMenu.underTrousers))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'использовать старые мерки':
        global merki_pants

        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTrousers)
    elif str(message.text).lower() == 'сделаем мерки':
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


@dp.message(StateFilter(UserMenu.orderUnderTrousers))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_16, 'Обхват талии', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step23)


@dp.message(StateFilter(UserSize.step23))
async def under(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants += str(message.text)
        merki_pants += '/'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step24)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step23)


@dp.message(StateFilter(UserSize.step24))
async def under(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants += str(message.text)
        merki_pants += '/'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step25)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step24)


@dp.message(StateFilter(UserSize.step25))
async def under(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants += str(message.text)
        merki_pants += '/'
        await message.answer_photo(photo_4, 'Высота сиденья')
        await state.set_state(UserSize.step26)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step25)


@dp.message(StateFilter(UserSize.step26))
async def under(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants += str(message.text)
        merki_pants += '/'
        await message.answer_photo(photo_6, 'Длина брюк по боку')
        await state.set_state(UserSize.step27)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step26)


@dp.message(StateFilter(UserSize.step27))
async def under(message: types.Message, state: FSMContext):
    global merki_pants

    if check(str(message.text), 'num'):
        merki_pants += str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step28)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step27)


@dp.message(StateFilter(UserSize.step28), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step28)
    else:
        await message.answer('Фото получены')
        db.input_merki(merki_pants, 'pants', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderTrousers), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserMenu.orderTrousers)
    else:
        await message.answer('Фото получены')
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


# --------------------------------------------- низ брюки --------------------------------------------
# --------------------------------------------- верх -------------------------------------------
@dp.message(StateFilter(UserMenu.top))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    print(str(message.text))
    if str(message.text).lower() == 'использовать старые мерки':
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserMenu.orderTop)
    elif str(message.text).lower() == 'стандартный размер':
        await message.answer('Загрузите одно-два фото желаемого изделия')
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


@dp.message(StateFilter(UserMenu.orderTopVse))
async def under(message: types.Message, state: FSMContext):
    if str(message.text).lower() == 'меню':
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Тогда когда нибудь потом', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)
    else:
        await message.answer_photo(photo_17, 'Обхват шеи', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserSize.step5)


@dp.message(StateFilter(UserSize.step5))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_10, 'Обхват груди 1')
        await state.set_state(UserSize.step6)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step5)



@dp.message(StateFilter(UserSize.step6))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_12, 'Обхват груди 2')
        await state.set_state(UserSize.step7)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step6)


@dp.message(StateFilter(UserSize.step7))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_13, 'Обхват груди 3')
        await state.set_state(UserSize.step8)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step7)


@dp.message(StateFilter(UserSize.step8))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_18, 'Центр груди')
        await state.set_state(UserSize.step9)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step8)


@dp.message(StateFilter(UserSize.step9))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_2, 'Высота груди')
        await state.set_state(UserSize.step10)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step9)


@dp.message(StateFilter(UserSize.step10))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_19, 'Ширина плеча')
        await state.set_state(UserSize.step11)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step10)


@dp.message(StateFilter(UserSize.step11))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_15, 'Обхват плеча')
        await state.set_state(UserSize.step12)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step11)


@dp.message(StateFilter(UserSize.step12))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_14, 'Обхват запястья')
        await state.set_state(UserSize.step13)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step12)


@dp.message(StateFilter(UserSize.step13))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_20, 'Длина рукава')
        await state.set_state(UserSize.step14)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step13)


@dp.message(StateFilter(UserSize.step14))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_16, 'Обхват талии')
        await state.set_state(UserSize.step15)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step14)


@dp.message(StateFilter(UserSize.step15))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_9, 'Обхват бедер')
        await state.set_state(UserSize.step16)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step15)


@dp.message(StateFilter(UserSize.step16))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_1, 'Высота бедер')
        await state.set_state(UserSize.step17)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step16)


@dp.message(StateFilter(UserSize.step17))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_11, 'Ширина спины')
        await state.set_state(UserSize.step18)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step17)


@dp.message(StateFilter(UserSize.step18))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина спины до талии')
        await state.set_state(UserSize.step19)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step18)


@dp.message(StateFilter(UserSize.step19))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина переда до талии')
        await state.set_state(UserSize.step20)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step19)


@dp.message(StateFilter(UserSize.step20))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        merki_up += '/'
        await message.answer_photo(photo_8, 'Длина изделия')
        await state.set_state(UserSize.step21)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step20)


@dp.message(StateFilter(UserSize.step21))
async def under(message: types.Message, state: FSMContext):
    global merki_up

    if check(str(message.text), 'num'):
        merki_up += str(message.text)
        await message.answer('Загрузите одно-два фото желаемого изделия')
        await state.set_state(UserSize.step22)
    else:
        await message.answer('🥺Не похоже на ваши параметры. Попробуйте еще раз')
        await state.set_state(UserSize.step21)


@dp.message(StateFilter(UserSize.step22), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step22)
    else:
        await message.answer('Фото получены')
        merki_up += str(message.text)
        db.input_merki(merki_up, 'up', global_phone_number)
        all_user_data = db.get_user(global_phone_number)
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


@dp.message(StateFilter(UserMenu.orderTop), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
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
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserMenu.orderTop)
    else:
        await message.answer('Фото получены')
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        #Переадресация админу !!!!!!!!!!!!!
        kb = [
            [types.KeyboardButton(text="В меню")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
        await state.set_state(UserState.ageUser)


# --------------------------------------------- верх -------------------------------------------


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
