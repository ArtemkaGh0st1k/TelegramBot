import re
import sqlite3
import logging

from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton

from DataBase.DataBase import PATH_DATA_BASE
from MainParameters.CommonParams import TYPE_COMMAND, TYPE_COMMAND_DICTIONARY
from MainParameters.GetParams import NameSurnameList

logging.getLogger(__name__)

router_name_surname = Router()


@router_name_surname.message(lambda message: re.match(r"Узнать данные", str(message.text)))
async def send_NameAndSurname(message: Message):

    '''Описание:\n
    Выводит список имён и фамилий из базы данных'''

    logging.info(f'Enter to {send_NameAndSurname.__name__}')

    global NameSurnameList 
    global TYPE_COMMAND  

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


            await message.answer("Список людей", reply_markup=markup.adjust(1)
                                    .as_markup(input_field_placeholder="Выберите студента"))
            
            logging.info(f'Finish {send_NameAndSurname.__name__}')

            