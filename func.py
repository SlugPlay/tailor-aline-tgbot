import re


def check(text, type):
    if type == 'lang':
        regex = "^[a-zA-Zа-яА-ЯёЁ]+$"
        pattern = re.compile(regex)
        return pattern.search(text) is not None
    if type == 'num':
        return text.isdigit()
