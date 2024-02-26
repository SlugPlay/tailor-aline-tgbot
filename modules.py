@dp.message(StateFilter(UserSize.step4))
async def under(message: types.Message, state: FSMContext):
    global merki_skirt, all_user_data, flag_photos, all_photo_down_skirt

    all_photo_down_skirt = []
    all_photo_down_skirt.append(message.photo[-1].file_id)
    kb = [
        [types.KeyboardButton(text="Продолжить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    for i in range(len(all_photo_down_skirt)):
        if i == (len(all_photo_down_skirt) - 1) and flag_photos:
            flag_photos = False
            await message.answer('Фото получены', reply_markup=keyboard)
    db.input_merki(merki_skirt, 'skirt', global_phone_number)
    all_user_data = db.get_user(global_phone_number)
    await state.set_state(UserSize.step4_5)


@dp.message(StateFilter(UserSize.step4_5))
async def under2(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="В меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Благодарим Вас! С вами свяжется наш менеджер в течении 1 часа.', reply_markup=keyboard)
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    #Переадресация админу !!!!!!!!!!!!!
    await state.set_state(UserState.ageUser)



@dp.message(F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def handle_albums(message: Message, album: list[Message]):
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(file_id)
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(file_id)


@dp.message(StateFilter(UserSize.step28), F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]))
async def under(message: types.Message, state: FSMContext, album: list[Message]):
    global merki_pants, all_user_data

    flag_unknown_media = False
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append([file_id, 'pic'])
        elif str(msg.document.mime_type) in acsess_files:
            file_id = msg.document.file_id
            media_group.append([file_id, 'doc'])
        else:
            flag_unknown_media = True
    if flag_unknown_media:
        await message.answer('🥺Не похоже на нужный формат. Загрузи фотографию в обычном формате теллеграмма или в виде файла с расширением jpg/jpeg/png')
        media_group = []
        await state.set_state(UserSize.step4)
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