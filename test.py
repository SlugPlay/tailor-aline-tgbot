global merki_skmerki_upirt

merki_up = ''

global merki_up

    merki_up += str(message.text)
    merki_up += '/'

global merki_up, all_user_data

    merki_up += str(message.text)
    db.input_merki(merki_up, 'up', global_phone_number)
    all_user_data = db.get_user(global_phone_number)