import sqlite3


async def create_db():
    global conn, cur

    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, phone_number TEXT, first_name TEXT, last_name TEXT, age TEXT, region TEXT, size TEXT, photo_front TEXT, photo_back TEXT, photo_profile TEXT)")
    conn.commit()


async def create_profile(user_id, phone_number):
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, phone_number, '', '', '', '', '', '', '', '', ''))
        conn.commit()


async def edit_profile(user_id, first_name, last_name, age, region, size, photo_front, photo_back, photo_profile):
    cur.execute("UPDATE users SET first_name = '{}' last_name = '{}', age = '{}' region = '{}', size = '{}' photo_front = '{}', photo_back = '{}' photo_profile = '{}' WHERE user_id == '{}'".format(first_name, last_name, age, region, size, photo_front, photo_back, photo_profile, user_id))
    conn.commit()


def get_users(phone_number):
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT first_name, last_name, age, region, size, photo_front, photo_back, photo_profile FROM users WHERE phone_number == '{key}'".format(key=phone_number)).fetchone()
    return result