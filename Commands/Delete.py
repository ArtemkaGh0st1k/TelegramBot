import re
import logging

from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup 

from MainParameters.CommonParams import (TYPE_COMMAND_DICTIONARY, PICK_DELETE_COMMAND,
                                         TYPE_COMMAND)

logging.getLogger(__name__)

router_delete = Router()


@router_delete.message(lambda message: re.match(r"Удалить данные", str(message.text)))
async def send_delete_command(message: Message):
    
    '''Описание:\n
    Функция, которая отображает
    виды команды удаления\n
    1)По предмету\n
    2)По семместру\n
    3)Полностью студента'''

    logging.info(f'Enter to {send_delete_command.__name__}')

    global TYPE_COMMAND  
    TYPE_COMMAND = TYPE_COMMAND_DICTIONARY[str(message.text)]

    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=PICK_DELETE_COMMAND[0])],
        [KeyboardButton(text=PICK_DELETE_COMMAND[1])],
        [KeyboardButton(text=PICK_DELETE_COMMAND[2])] ],
        resize_keyboard=True,
        input_field_placeholder="Выберите тип удаления"
        )

    # можно выделить parse_mode как html(жирный, курсивный и т.д)
    await message.answer("Вам прделагается удлаить данные о студенты в таком формате:\n"
                        +"<b>По предмету</b> -> удаляет студентов по выбранному <u>предмету</u>\n" 
                        +"<b>По семместру</b> -> удаляет студента по выюранному <u>семместру</u>\n"
                        +"<b>Полностью студента</b> -> удаляет данные выбранного студента <u>по всем семместрам</u>")
    
    await message.answer('Тип удаления', reply_markup=markup)

    logging.info(f'Finish {send_delete_command.__name__}')
                         
    