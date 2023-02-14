from pykeepass import PyKeePass, create_database
from pykeepass.exceptions import CredentialsError
from pathlib import Path
import string
import random


path = Path('password/dbs/').absolute()


def check_path():
    x = Path.exists(path)
    if not x:
        Path.mkdir(path)


def create_new_file(user_id, password):
    check_path()
    file = f"{path}/{user_id}.kdbx"
    db = create_database(filename=file, password=password)
    return db


def open_file(user_id, pwd_db):
    try:
        file = f"{path}/{user_id}.kdbx"
        pyk = PyKeePass(filename=file, password=pwd_db)
        return pyk
    except FileNotFoundError:
        return False
    except CredentialsError:
        return False


def change_file_password(user_id, pwd_db, password):
    pyk = open_file(user_id, pwd_db)
    pyk.password = password
    pyk.save()


def add_password(pwd_db, user_id, title, username, password, url):
    pyk = open_file(user_id, pwd_db)
    pyk.add_entry(title=title, username=username, password=password, url=url, destination_group=pyk.root_group)
    pyk.save()


def password_update(pwd_db, user_id, title, new_title, username, password, url):
    pyk = open_file(user_id, pwd_db)
    entry = pyk.find_entries(title=title, first=True)
    entry.title = new_title
    entry.username = username
    entry.password = password
    entry.url = url
    pyk.save()


def delete_password(pwd_db, user_id, title):
    pyk = open_file(user_id, pwd_db)
    entry = pyk.find_entries(title=title, first=True)
    pyk.delete_entry(entry=entry)
    pyk.save()


def random_pwd(length):
    characters = string.ascii_letters + string.digits
    amount = int(length)
    result_str = ''.join(random.choice(characters) for i in range(amount))
    return result_str


def check_exists(pwd_db, new_name, user_id):
    pyk = open_file(user_id, pwd_db)
    entries = pyk.entries
    for x in entries:
        if x.title == new_name:
            return x
    return False


def check_pwd(pwd):
    if len(pwd) < 3:
        password = random_pwd(int(pwd))
        return password
    else:
        return pwd
