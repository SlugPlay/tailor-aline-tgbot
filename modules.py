# Получение фотки для добавления в БД ----------------------------------------------------------------------------------------------------
file_id = message.photo[-1].file_id
user_info.append(file_id)



# Проверка на текст и цифры---------------------------------------------------------------------------------------------------------------
import re

def check(text, type):
    if type == 'lang':
        regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
        pattern = re.compile(regex)
        return pattern.search(text) is not None
    if type == 'num':
        return text.isdigit()


#Проверка на фотку---------------------------------------------------------------------------------------------------------------
if message.photo:
    pass # Ваш код в случае если пользователь отправил фото
elif message.document:
    pass
else:
    await message.answer("Это не фото")
