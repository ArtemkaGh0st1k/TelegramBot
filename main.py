import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.command import Command

from TOKEN import TOKEN
from MainParameters.CommonParams import COMMAND_LIST
from DataBase.DataBase import create_data_base
from Commands.Delete import router_delete
from Commands.Insert import router_insert
from Commands.NameSurnameShow import router_name_surname
from Commands.ExcelTableShow import router_excel
from Handlers.Exception_Handler import router_exception
from Handlers.Command1_Handler import router_command_1
from Handlers.Command2_Handler import router_command_2
from Handlers.Command3_Handler import router_command_3


bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher()


count_start = 0
@dp.message(Command("start"))
async def start_handler(message: Message):

    '''Описание ->\n
    Инициализирует четыре кнопки:\n
    1)Узнать данные о студенте(ов)\n
    2)Внести данные о новом студенте\n
    3)Удалить данные о студенте\n
    4)Посмотреть таблицу'''

    logging.info("Enter to start_handler")

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=COMMAND_LIST[0])], 
        [KeyboardButton(text=COMMAND_LIST[1])], 
        [KeyboardButton(text=COMMAND_LIST[2])],
        [KeyboardButton(text=COMMAND_LIST[3])] ],
        resize_keyboard=True,
        input_field_placeholder="Выберите тип команды")
    
    await message.answer(text="Клавиатура",reply_markup=keyboard)
    await create_data_base()


@dp.message(Command("help"))
async def help_handler(message: Message):

    '''Описание:\n
    Вспомогательная функция, которая
    расскажет описание бота при /help '''

    logging.info("Enter to help_handler")

    if message.from_user.last_name != None:
        await message.answer("Привет" + " " + f"{message.from_user.first_name}" + " " 
                        + f"{message.from_user.last_name} " + "(" 
                        + f"{message.from_user.username}" + ").\n" 
                        + "Моя основная цель это предоставление информации о студентах\n" 
                        + "Чтобы подробнее ознакомится с моими возможностями, воспользуйся" + " " 
                        + "командой /start")
    else:
       await message.answer("Привет" + " " + f"{message.from_user.first_name}" + " " + "(" 
                        + f"{message.from_user.username}" + ").\n" 
                        + "Моя основная цель это предоставление информации о студентах\n" 
                        + "Чтобы подробнее ознакомится с моими возможностями, воспользуйся" + " " 
                        + "командой /start")
       
async def main():
    dp.message.register(start_handler, Command("start"))
    dp.message.register(help_handler, Command("help"))

    dp.include_router(router_name_surname)
    dp.include_router(router_insert)
    dp.include_router(router_delete)
    dp.include_router(router_excel)
    dp.include_router(router_command_1)
    dp.include_router(router_command_2)
    dp.include_router(router_command_3)
    dp.include_router(router_exception)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
            '{lineno} - {name} - {message}',
        style='{',
        filename="mylog.log",
        filemode='w',
        encoding="UTF-8"
    )
    asyncio.run(main())