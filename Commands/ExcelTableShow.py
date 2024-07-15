import re
import sqlite3
import logging
from os import remove

from openpyxl import Workbook
from aiogram import Router
from aiogram.types import Message, FSInputFile

from DataBase.DataBase import PATH_DATA_BASE
from MainParameters.CommonParams import TYPE_COMMAND, TYPE_COMMAND_DICTIONARY

logging.getLogger(__name__)

router_excel = Router()


@router_excel.message(lambda message: re.match(r"Посмотреть таблицу", str(message.text)))
async def send_excel_data(message: Message):

    '''Описание:\n
    Функция, которая отправляет
    excel файл, заполненный всеми данными
    из базы'''

    logging.info(f'Start to {send_excel_data.__name__}')

    global TYPE_COMMAND
    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    
    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""SELECT * FROM student ORDER BY first_name""")
        except Exception:
            logging.exception('Exception')
            raise
        finally:
            columnsDB = [description[0] for description in sql.description]

            columnName = []
            columnSurname = []
            columnGroup = []
            columnObject = []
            columnSemestr = []
            columnAVGMark = []
            for elem in sql.fetchall():
                columnName.append(elem[0])
                columnSurname.append(elem[1])
                columnGroup.append(elem[2])
                columnObject.append(elem[3])
                columnSemestr.append(elem[4])                    
                columnAVGMark.append(elem[5])

            workbook = Workbook()
            sheet = workbook.active

            # Заполнение столбцов
            # В помощь таблица ASCII
            for i in range(len(columnsDB)):
                sheet[f"{chr(i+65)}{1}"] = columnsDB[i]

            for row in range(len(columnName)):
                sheet[row+2][0].value = columnName[row]
                sheet[row+2][1].value = columnSurname[row]
                sheet[row+2][2].value = columnGroup[row]
                sheet[row+2][3].value = columnObject[row]
                sheet[row+2][4].value = columnSemestr[row]
                sheet[row+2][5].value = columnAVGMark[row]

            workbook.save(filename="C:\\Users\\Артем\\Desktop\\TELEGRAMBOT-1\\DataBase\\DataBaseExcel.xlsx")
                                                    
            workbook.close()

            await message.answer_document(document=FSInputFile("C:\\Users\\Артем\\Desktop\\TELEGRAMBOT-1\\DataBase\\DataBaseExcel.xlsx"))

            logging.info(f'Finish {send_excel_data.__name__}')