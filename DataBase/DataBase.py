import sqlite3
import logging
from os.path import exists
from random import randint, uniform

from russian_names import RussianNames

from MainParameters.CommonParams import OBJECT_LIST


PATH_DATA_BASE = "C:\\Users\\Артем\\Desktop\\TELEGRAMBOT-1\\DataBase\\server.db"

async def create_data_base():
        
        '''Описание:\n
        Функция, которая создаёт базу данных'''

        logging.info(f'Enter to {create_data_base.__name__}')

        #проверка на создание файла базы данных
        if (not exists(path=PATH_DATA_BASE)):

            #создание локальной базы данных
            with sqlite3.connect(database=PATH_DATA_BASE) as db:
                sql = db.cursor()

                sql.execute("""CREATE TABLE IF NOT EXISTS student (
                            first_name TEXT,
                            last_name TEXT,
                            number_group INTEGER,
                            obj TEXT,
                            semestr INTEGER,
                            mark REAL
                )""" )
                db.commit()

                rus_names = RussianNames(count = 15).get_batch()

                groupDB = randint(1,100)
                for rn in rus_names:
                    nameDB = rn.split(' ')[0]
                    surnameDB = rn.split(' ')[2]

                    semestrDB = 1
                    for i in range(len(OBJECT_LIST)):
                        
                        objectDB = OBJECT_LIST[semestrDB-1]
                        markDB = uniform(2.0, 5.0)

                        sql.execute("""INSERT INTO student (first_name, last_name, number_group, obj, semestr, mark) VALUES (?, ?, ?, ?, ?, ?)""",
                        (nameDB, surnameDB, groupDB, objectDB, semestrDB, markDB))

                        semestrDB+= 1
                db.commit()
            
            logging.info(f'Finish {create_data_base.__name__}')
