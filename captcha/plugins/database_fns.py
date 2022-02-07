# (c) 2022 @xditya.
# Powered by apis.xditya.me

from . import db


# users to db
def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list):  # Returns String
    str = "".join(f"{x} " for x in list)
    return str.strip()


def is_added(var, id):  # Take int or str with numbers only , Returns Boolean
    if not str(id).isdigit():
        return False
    users = get_all(var)
    return str(id) in users


def add_to_db(var, id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    if not id.isdigit():
        return False
    try:
        users = get_all(var)
        users.append(id)
        db.set(var, list_to_str(users))
        return True
    except Exception as e:
        return False


def get_all(var):  # Returns List
    users = db.get(var)
    if users is None or users == "":
        return [""]
    else:
        return str_to_list(users)


def del_from_db(var, id):
    if is_added(var, id):
        a = get_all(var)
        a.remove(id)
        return db.set(var, a)
