import re
import sqlite3
import logging
import numpy as np
import os

from matplotlib import pyplot as plt 
from aiogram import Router
from aiogram.types import (Message, KeyboardButton,
                            ReplyKeyboardMarkup, FSInputFile)
from aiogram.utils.keyboard import ReplyKeyboardBuilder 

from DataBase.DataBase import PATH_DATA_BASE
from MainParameters.CommonParams import OBJECT_LIST
from MainParameters.GetParams import (PICK_NAME_SURNAME, PICK_OBJECT,
                                      NameSurnameList)

logging.getLogger(__name__)

router_command_1 = Router()

PATH_SAVE_FIG = "C:\\Users\\Артем\\Desktop\\TELEGRAMBOT-1\\Plot"

@router_command_1.message(lambda student: NameSurnameList.__contains__(str(student.text)))
async def send_oject_list(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит имя и фамилию.
    которые были выбраны и отправляет 
    список предметов'''

    logging.info(f'Start to {send_oject_list.__name__}')

    #ловим Имя и Фамилию из базы данных глобально
    global PICK_NAME_SURNAME
    PICK_NAME_SURNAME = message.text.split(' ')
    
    
    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""SELECT obj FROM student WHERE (first_name = ?) AND (last_name = ?)""",
                    (PICK_NAME_SURNAME[0], PICK_NAME_SURNAME[1]))
        except Exception as e:
            logging.exception(str(e))
            raise
        finally:
            markup = ReplyKeyboardBuilder()

            for object in sql.fetchall():
                markup.add(KeyboardButton(text=object[0]))
            

            await message.answer("Список предметов", reply_markup=markup.adjust(1)
                                .as_markup(input_field_placeholder="Выберите предмет"))
            
            logging.info(f'Finish {send_oject_list.__name__}')


@router_command_1.message(lambda object: OBJECT_LIST.__contains__(str(object.text))) 
async def send_info_about_plot(message: Message):

    '''Описание:\n
    Лямбда-функция, которая ловит выбранный предмет
    и удаляет все данные по этому предмету'''

    logging.info(f'Start to {send_info_about_plot.__name__}')

    global PICK_OBJECT
    PICK_OBJECT = str(message.text)
    
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="График")], 
        [KeyboardButton(text="Гистограмма")], 
        [KeyboardButton(text="Диаграмма")] ],
        resize_keyboard=True,
        input_field_placeholder="Выбирите тип построения")

    await message.answer("Выбор графика", reply_markup=markup)

    logging.info(f'Finish {send_info_about_plot.__name__}')


@router_command_1.message(lambda message: re.match(r"График", str(message.text)))
async def plot_scatter(message: Message):

    '''Описание:\n
    Функция, которая отправляет график
    вида scatter(точечный график)'''

    logging.info(f'Enter to {plot_scatter.__name__}')

    nameDB = PICK_NAME_SURNAME[0]
    surnameDB =  PICK_NAME_SURNAME[1]
    objectDB = PICK_OBJECT

   
    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
    
        #Выбранный студент -> его семместр и ср.бал
        sql.execute("""SELECT semestr, mark FROM student WHERE (first_name = ?) AND (last_name = ?) AND (obj = ?)""",
                        (nameDB, surnameDB, objectDB))

        for elem in sql.fetchall():
            semestrDB = int(elem[0])
            avg_markDB = float(elem[1])

        try:
            #sql - запрос -> ср значение по ср.баллу по определлёному предмету 
            sql.execute("""SELECT AVG(mark) FROM student WHERE (obj = ?) AND (semestr = ?)""",
                        (objectDB, semestrDB))
        except Exception as e:
            logging.exception(str(e))
            raise 
        finally:
            for avg in sql.fetchall():
                avgmark_groupDB = avg[0]

            #x-лист -> семместры
            #y-лист -> ср.бал 
            x1 = np.array([semestrDB])
            y1 = np.array([avg_markDB])
            x2 = np.array([semestrDB])
            y2 = np.array([avgmark_groupDB])

            plt.figure(figsize=(6,5))
            plt.axis([0,7,0,5])
            plt.text(semestrDB, avg_markDB, f"{round(avg_markDB,2)}")
            plt.text(semestrDB, avgmark_groupDB, f"{round(avgmark_groupDB,2)}")
            plt.title('Scatter')
            plt.xlabel('Семместр')
            plt.ylabel('Средний бал')
            plt.grid(True)
            plt.scatter(x1,y1)
            plt.scatter(x2,y2)
            plt.yticks(np.linspace(0, 5, 20))
            lgd = plt.legend([nameDB + ' ' + surnameDB, 'Ср.бал группы'],loc ='center left', bbox_to_anchor=(1,0.5))
            plt.savefig(os.path.join(PATH_SAVE_FIG, 'scatter.png'), 
                        bbox_extra_artists=(lgd,), bbox_inches='tight')
            plt.close()

            await message.answer_photo(photo=FSInputFile(path=os.path.join(PATH_SAVE_FIG, "scatter.png")))

            logging.info(f'Finish {plot_scatter.__name__}')


@router_command_1.message(lambda message: re.match(r"Гистограмма", str(message.text)))
async def plot_bar(message: Message):

    '''Описание:\n
    Функция, которая отправляет график
    вида bar(гистограмма)'''

    logging.info(f'Enter to {plot_bar.__name__}')

    objectDB = PICK_OBJECT

    #Вытащить Имя и Фамилию студентов по выбранному предмету и средний бал
    
    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            sql.execute("""SELECT DISTINCT first_name, last_name, mark FROM student WHERE obj = ?""",
                            (objectDB,))
        except Exception as e:
            logging.exception(str(e))
            raise
        finally: 
            namesList = []
            avg_markList = []
            for elem in sql.fetchall():
                namesList.append(elem[0] + ' ' + elem[1])
                avg_markList.append(elem[2])

            index = 0
            for name in namesList:
                if name == PICK_NAME_SURNAME[0] + ' ' + PICK_NAME_SURNAME[1]:
                    break
                else:
                    index+=1

            plt.title('bar')
            plt.yticks(np.linspace(0,5,20))
            plt.text(index, avg_markList[index], f"{round(avg_markList[index], 2)}")

            plt.bar(np.arange(len(avg_markList)), avg_markList, color = 'blue')
            plt.bar(np.array(index), avg_markList[index], color = 'red')
            lgd = plt.legend(['Балы других студентов', namesList[index]], loc ='center left', bbox_to_anchor=(1,0.5))

            plt.savefig(os.path.join(PATH_SAVE_FIG, "bar.png"), 
                        bbox_extra_artists=(lgd,), bbox_inches='tight')
            plt.close()

            await message.answer_photo(photo=FSInputFile(path=os.path.join(PATH_SAVE_FIG, "bar.png")))

            logging.info(f'Finish {plot_bar.__name__}')


@router_command_1.message(lambda message: re.match(r"Диаграмма",str(message.text)))
async def plot_pie(message: Message):

    '''Описание:\n
    Функция, которая отправляет график
    вида pie(диаграмма)'''

    logging.info(f'Enter to {plot_pie.__name__}')

    objectDB = PICK_OBJECT

    with sqlite3.connect(database=PATH_DATA_BASE) as db:
        sql = db.cursor()
        try:
            #Вытащить Имя и Фамиля студентов по выбранному предмету и средний бал
            sql.execute("""SELECT DISTINCT first_name, last_name, mark FROM student WHERE obj = ?""",
                        (objectDB,))
        except Exception as e:
            logging.exception(str(e))
            raise
        finally:
            labels = []
            values = []
            for elem in sql.fetchall():
                labels.append(elem[0] + ' ' + elem[1])
                values.append(elem[2])

            #узнали где находится наш выбранный студент
            index = 0
            for label in labels:
                if label == PICK_NAME_SURNAME[0] + ' ' + PICK_NAME_SURNAME[1]:
                    break
                else:
                    index+= 1
            
            #для выбора кусочка диаграммы
            explode = []
            for i in range(len(labels)):
                if i==index:
                    explode.append(0.3)
                else:
                    explode.append(0)

            plt.title('Pie')
            plt.pie(values, labels = labels, explode=explode,shadow=True,autopct='%1.1f%%',startangle=180)
            plt.savefig(os.path.join(PATH_SAVE_FIG, "pie.png"))
            plt.close() 

            await message.answer_photo(photo=FSInputFile(path=os.path.join(PATH_SAVE_FIG, "pie.png")))
            
            logging.info(f'Finish {plot_pie.__name__}')