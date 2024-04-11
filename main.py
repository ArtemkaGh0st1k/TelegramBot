import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'), parse_mode='html')
dp = Dispatcher()

