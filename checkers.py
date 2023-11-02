# Номер телефона:

import re
def check_phone_number(phone_number):
    pattern = r"(\(\d{3}\) \d{3}-\d{4})|(\d{3}-\d{3}-\d{4})|(\d{10})"
    match = re.match(pattern, phone_number)
    return match


# Сложность пароля:


def check_password(password):
    # while True:
    if (len(password) <= 8):

        return ("В пароле должно быть не менее 8 символов")
    elif not re.search("[a-z]", password):

        return "В пароле должны быть строчные латинские буквы"
    elif not re.search("[A-Z]", password):

        return "В пароле должны быть заглавные латинские буквы"
    elif not re.search("[0-9]", password):

        return "В пароле должны быть цифры"
    elif not re.search("[_@$]", password):

        return "В пароле должны быть спец. символы"
    elif re.search("\s", password):

        return "В пароле не должно быть пробелов"
    else:

        return "OK"


# Логин:

def check_login(login):
    spaces = re.findall(r'\s', login)
    if len(spaces) > 0:
        return "В логине не должно быть пробелов"
    return "OK"
