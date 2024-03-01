import sqlite3


async def create_db():
    global conn, cur

    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, phone_number TEXT, status TEXT, first_name TEXT, last_name TEXT, age TEXT, region TEXT, size TEXT, photo_front TEXT, photo_back TEXT, photo_profile TEXT, merki_down_skirt TEXT, merki_down_pants TEXT, merki_up TEXT)")
    conn.commit()


async def get_phone_status():
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT phone_number, status FROM users").fetchall()
    conn.commit()
    return result


async def create_profile(user_id, phone_number, status):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    user = cur.execute("SELECT 1 FROM users WHERE phone_number == '{key}'".format(key=phone_number)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, phone_number, status, '', '', '', '', '', '', '', '', '', '', ''))
        conn.commit()


async def edit_profile(user_id, phone, status, first_name, last_name, age, region, size, photo_front, photo_back,
                       photo_profile):
    cur.execute(
        "UPDATE users SET status = '{}', first_name = '{}', last_name = '{}', age = '{}', region = '{}', size = '{}', photo_front = '{}', photo_back = '{}', photo_profile = '{}' WHERE user_id == '{}'".format(
            status, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile, user_id))
    conn.commit()


def get_user(phone_number):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute(
        "SELECT user_id, phone_number, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile, merki_down_skirt, merki_down_pants, merki_up FROM users WHERE phone_number == '{key}'".format(
            key=phone_number)).fetchone()
    return result


def input_merki(merki, type, phone):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    if type == 'skirt':
        cur.execute("UPDATE users SET merki_down_skirt = '{value}' WHERE phone_number == '{key}'".format(value=merki,
                                                                                                         key=phone))
    elif type == 'pants':
        cur.execute("UPDATE users SET merki_down_pants = '{value}' WHERE phone_number == '{key}'".format(value=merki,
                                                                                                         key=phone))
    elif type == 'up':
        cur.execute(
            "UPDATE users SET merki_up = '{value}' WHERE phone_number == '{key}'".format(value=merki, key=phone))
    conn.commit()


def delete_user(phone_number):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE phone_number == '{key}'".format(key=phone_number))
    conn.commit()


def check_admin(phone_number):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT status FROM users WHERE phone_number == '{key}'".format(key=phone_number)).fetchone()
    return result


def get_admin_data():
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT user_id FROM users WHERE status == 'admin'").fetchone()
    return result
