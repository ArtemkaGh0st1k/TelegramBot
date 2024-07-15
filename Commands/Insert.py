import re
import logging

from aiogram import Router
from aiogram.types import Message

from MainParameters.CommonParams import TYPE_COMMAND, TYPE_COMMAND_DICTIONARY

logging.getLogger(__name__)

router_insert = Router()


@router_insert.message(lambda message: re.match(r"Внести данные", str(message.text)))
async def send_info_insert_data(message: Message):

    '''Описание:\n
    Функция, которая отображает шаблон
    заполнения данных в базу'''

    logging.info(f'Enter to {send_info_insert_data.__name__}')
    
    global TYPE_COMMAND
    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    await message.answer("Пожалуйста внесети данные согласно данному" + ' '
                        + "шаблону: Имя_Фамилия_группа_Предмет_семместр(1-7)_ср.бал" + ' '
                        + "где _ это <b>ПРОБЕЛ</b>")

    await message.answer("Подсказка для заполнения:\n"
                        +"<b>Математический анализ</b> -> <u>1 семмесетр</u>\n"
                        +"<b>Физика.Механика</b> -> <u>2 семместр</u>\n"
                        +"<b>Физика.Термодинамика</b> -> <u>3 семместр</u>\n"
                        +"<b>Физика.Оптика</b> -> <u>4 семместр</u>\n" 
                        +"<b>Линейная алгебра</b> -> <u>5 семместр</u>\n"
                        +"<b>Технологии программирования</b> -> <u>6 семместр</u>\n"
                        +"<b>Дифференциальные уравнения</b> -> <u>7 семместр</u>\n")
    
    logging.info(f'Finish {send_info_insert_data.__name__}')
    
