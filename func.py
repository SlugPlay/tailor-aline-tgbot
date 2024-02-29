import re
from config import bot

def check(text, type):
    if type == 'lang':
        regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
        pattern = re.compile(regex)
        return pattern.search(text) is not None
    if type == 'num':
        return text.isdigit()
    

async def request_buy(name_order, all_user_data, admin_data, merki, type, files):
    for i in admin_data:
        await bot.send_message(i,
                                "Новый заказ!\nПользователь номер: {}\nНомер телефона: {}\nИмя: {}\nФамилия: {}\nВозраст: {}\nРегион: {}\nРазмер: {}\n".format(
                                    all_user_data[0], all_user_data[1], all_user_data[2], all_user_data[3],
                                    all_user_data[4], all_user_data[5], all_user_data[6]))
        try:
            if all_user_data[7][-3:] == 'pic':
                await bot.send_photo(i, all_user_data[7][:-4], caption='Фото спереди:')
            else:
                await bot.send_document(i, all_user_data[7][:-4], caption='Фото спереди:')
        except:
            await bot.send_message(i, 'Отсутствует фото спереди')
        try:
            if all_user_data[8][-3:] == 'pic':
                await bot.send_photo(i, all_user_data[8][:-4], caption='Фото сзади:')
            else:
                await bot.send_document(i, all_user_data[8][:-4], caption='Фото сзади:')
        except:
            await bot.send_message(i, 'Отсутствует фото сзади')
        try:
            if all_user_data[9][-3:] == 'pic':
                await bot.send_photo(i, all_user_data[9][:-4], caption='Фото в профиль:')
            else:
                await bot.send_document(i, all_user_data[9][:-4], caption='Фото в профиль:')
        except:
            await bot.send_message(i, 'Отсутствует фото в профиль')
        if type == 'individual':
            await bot.send_message(i, '{} - заказ с индивидуальными мерками\n{}'.format(name_order, merki))
        elif type == 'standart':
            await bot.send_message(i, '{}\nСтандартный размер: {}'.format(name_order, merki))
        await bot.send_message(i, 'Желаемое изделие:')
        for file in files:
            if file[-3:] == 'pic':
                await bot.send_photo(i, file[:-4])
            else:
                await bot.send_document(i, file[:-4])
