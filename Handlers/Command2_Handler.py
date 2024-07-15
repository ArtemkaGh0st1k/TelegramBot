import re
import sqlite3
import logging

from aiogram import Router
from aiogram.types import Message

from DataBase.DataBase import path_data_base

logging.getLogger(__name__)

router_command_2 = Router()


@router_command_2.message(lambda message: re.match(r"Добавить:", str(message.text)))
async def insert_value(message: Message):

    '''Описание:\n
    Функция, которая ловит слово Добавить и
    добавляет данные в базу'''

    logging.info(f'Start to {insert_value.__name__}')    

    #вычисляем количество подстрок (должно быть равно 7)
    countSubstrings = len(message.text.split(' '))
    if countSubstrings != 7: 
        await message.answer("Не до конца введены данные! Просьба проверить корректность")
        return

    substrings = message.text.split(' ')

              
    nameDB = substrings[1]
    surnameDB = substrings[2]
    groupDB = substrings[3]
    objectDB = substrings[4]
    semestrDB = substrings[5]
    averege_markDB = substrings[6]
    
    
    with sqlite3.connect(database=path_data_base) as db:
        sql = db.cursor()
    try:
        sql.execute("""INSERT INTO student (first_name, last_name, group, obj, semestr, mark) VALUES (?, ?, ?, ?, ?, ?)""",
        (nameDB, surnameDB, groupDB, objectDB, semestrDB, averege_markDB))
        sql.execute("""SELECT * FROM student ORDER BY first_name""")
    except Exception as e:
        logging.exception(str(e))
        raise
    finally:
        db.commit()

        await message.answer("Запись успешна добавлена в базу данных!")

        logging.info(f'Finish {insert_value.__name__}')