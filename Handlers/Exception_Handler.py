import logging

from aiogram import Router
from aiogram.types import Message

logging.getLogger(__name__)

router_exception = Router()


@router_exception.message(lambda message: True)
async def catch_anybad_text(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит все вводимые данные,
    который не предусмотренны'''

    logging.info('Start to cath_anybad_text')

    await message.answer("Извините, невозможно обработать текст!")

    logging.info('Finish cath_anybad_text')