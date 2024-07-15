import re
import sqlite3
import logging

from aiogram import Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DataBase.DataBase import PATH_DATA_BASE
from MainParameters.CommonParams import (TYPE_COMMAND, TYPE_COMMAND_DICTIONARY,
                                         OBJECT_LIST)
from MainParameters.DeleteParams import (PICK_NAME_SURNAME, PICK_OBJECT,
                                        NameSurnameList)

logging.getLogger(__name__)

router_command_3 = Router()


@router_command_3.message(lambda message: re.match(r"По предмету", str(message.text)))
async def send_info_object_delete(message: Message):

    '''Описание\n
    Функция, которая отправялет список
    предметов, по которым будет происходить удаление'''

    logging.info(f'Enter to {send_info_object_delete.__name__}')

    global TYPE_COMMAND
    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""SELECT DISTINCT obj FROM student""")
        except Exception as e:
            logging.exception('Exception')
            raise
        finally:
            markup = ReplyKeyboardBuilder()
        
            for object in sql.fetchall():
                markup.add(KeyboardButton(text=object[0]))

            await message.answer("Удаление по критерию 'По предмету'", reply_markup=markup.
                                adjust(1).as_markup(input_field_placeholder="Выберите предмет"))

            logging.info(f'Finish {send_info_object_delete.__name__}')
            

@router_command_3.message(lambda object: OBJECT_LIST.__contains__(str(object.text))) 
async def delete_object(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит выбранный предмет
    и удаляет все данные по этому предмету'''

    global PICK_OBJECT
    PICK_OBJECT = str(message.text)

    logging.info(f'Enter to {delete_object.__name__}')
    
    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""DELETE FROM student WHERE obj = ?""", (PICK_OBJECT,))
            sql.execute("""SELECT * FROM student ORDER BY first_name""")
        except Exception:
            logging.exception('Exception') 
            raise
        finally:
            db.commit()
            
            await message.answer("Данные успешны удалены!")
        
            logging.info(f'Finish {delete_object.__name__}')


@router_command_3.message(lambda message: re.match(r"По семместру", str(message.text)))
async def send_info_list_semestr_delete(message: Message):

    '''Описание:\n
    Функция, которая отправляет список семместров,
    по которым будет удаление'''

    logging.info(f'Enter to {send_info_list_semestr_delete.__name__}')

    global TYPE_COMMAND
    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='1')], 
        [KeyboardButton(text='2')], 
        [KeyboardButton(text='3')],
        [KeyboardButton(text='4')],
        [KeyboardButton(text='5')],
        [KeyboardButton(text='6')],
        [KeyboardButton(text='7')] ],
        resize_keyboard=True,
        input_field_placeholder="Выберите семестр")

    await message.answer("Удаление по критерию 'По семестру'", reply_markup=markup)       

    logging.info(f'Finish {send_info_list_semestr_delete.__name__}')


@router_command_3.message(lambda message: re.match(r"1|2|3|4|5|6|7", str(message.text)))
async def delete_semestr(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит выбранный семместр
    и удаляет все данные по этому семестру'''

    logging.info(f'Enter to {delete_semestr.__name__}')
        
    semestrDB = int(message.text)

    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""DELETE FROM student WHERE semestr = ?""", (semestrDB))
            sql.execute("""SELECT * FROM student ORDER BY first_name""")
        except Exception:
            logging.exception('Exception')
            raise
        finally:
            db.commit()

            await message.answer("Данные успешно удалены!")

            logging.info(f'Finish {delete_semestr.__name__}')


@router_command_3.message(lambda message: re.match(r"Полностью студента", str(message.text)))
async def send_info_name_surname_delete(message: Message):

    '''Описание:\n
    Функция, которая отправляет список имён и
    фамилий, по которым будут удалены данные'''

    logging.info(f'Enter to {send_info_name_surname_delete.__name__}')

    global TYPE_COMMAND
    global NameSurnameList

    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""SELECT DISTINCT first_name, last_name FROM student""")
        except Exception: 
            logging.exception('Exception')
            raise
        finally:
            queryList = sql.fetchall()

            nameList = []
            surnameList = []
            for elem in queryList:
                nameList.append(elem[0])
                surnameList.append(elem[1])

            #если не пустой список
            if NameSurnameList:
                NameSurnameList.clear()

            markup = ReplyKeyboardBuilder()

            for i in range(len(queryList)):
                markup.add(KeyboardButton(text=nameList[i] + ' ' + surnameList[i]))
                NameSurnameList.append(nameList[i] + ' ' + surnameList[i])


            await message.answer("Удаление по критерию 'Полностью студента'", reply_markup=markup.adjust(1).
                                as_markup(input_field_placeholder = "Выберите студента"))
            
            logging.info(f'Finish {send_info_name_surname_delete.__name__}')


@router_command_3.message(lambda student: NameSurnameList.__contains__(str(student.text)))
async def delete_name_surname(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит выбранную имя
    и фамилию и удаляет все данные(за все семестры)
    по этому человеку'''

    logging.info(f'Enter to {delete_name_surname.__name__}')

    global PICK_NAME_SURNAME
    PICK_NAME_SURNAME = message.text.split(' ')

    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""DELETE FROM student WHERE (first_name = ?) AND (last_name = ?)""",
                        (PICK_NAME_SURNAME[0], PICK_NAME_SURNAME[1]))
            sql.execute("""SELECT * FROM student ORDER BY first_name""")
        except Exception: 
            logging.exception('Exception')
            raise
        finally:
            db.commit()
            await message.answer("Данные успешны удалены!")

            logging.info(f'Finish {delete_name_surname.__name__}')
        
        
