import aiogram
from aiogram import types
from aiogram.dispatcher.filters import state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md

import asyncio
import functools
import itertools
import logging
import time
import typing

import aiohttp
from aiohttp.helpers import sentinel
storage= MemoryStorage()
Bot = aiogram.Bot
dp = aiogram.Dispatcher(bot, storage=storage)

select_subjects_keyboard_add =  InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="#математика", callback_data="add_math"),
        InlineKeyboardButton(text="#физика", callback_data="add_phis"),
        InlineKeyboardButton(text="#программирование", callback_data="add_proga"),
        InlineKeyboardButton(text="#ОПД", callback_data="add_OPD"),
        InlineKeyboardButton(text="#дискретка", callback_data="add_discr"),
        InlineKeyboardButton(text="#английский", callback_data="add_eng"),
        InlineKeyboardButton(text="#философия", callback_data="add_filosof"),
        InlineKeyboardButton(text="#ХОД", callback_data="add_XOD"),
        InlineKeyboardButton(text="#прочее", callback_data="add_another"),
)
select_subjects_keyboard_remove =  InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="#математика", callback_data="remove_math"),
        InlineKeyboardButton(text="#физика", callback_data="remove_phis"),
        InlineKeyboardButton(text="#программирование", callback_data="remove_proga"),
        InlineKeyboardButton(text="#ОПД", callback_data="remove_OPD"),
        InlineKeyboardButton(text="#дискретка", callback_data="remove_discr"),
        InlineKeyboardButton(text="#английский", callback_data="remove_eng"),
        InlineKeyboardButton(text="#философия", callback_data="remove_filosof"),
        InlineKeyboardButton(text="#ХОД", callback_data="remove_XOD"),
        InlineKeyboardButton(text="#прочее", callback_data="remove_another"),
)
settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
temp_button_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
subjects_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
button_main_menu = types.KeyboardButton("Подтверждаю")
button_start = types.KeyboardButton('Поехали 💖💖💖')
keyboard.add(button_start)
settings_button = ["добавить теги в избранное","удалить теги из избранных","список заявок","вернуться в главное меню"]
settings_keyboard.add(*settings_button)
buttons = ['Показать заявки', 'Создать заявку', 'Настройки']
temp_button_keyboard.add(*buttons)
subjects_buttons = ["#математика","#физика","#программирование",
                    "#ОПД","#дискретка","#английский",
                    "#философия","#ХОД","#прочее"]
subjects_keyboard.add(*subjects_buttons)

class Form(StatesGroup):
    tag = State()
    title = State()
    text = State()


mas=[]

@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    name = message.from_user.first_name
    await message.answer('Привет, ' + name + "!" + '\n' + "Давай начнем!" + "\n" + 'Если хочешь посмотреть список всех доступных команд, то введи /help', reply_markup=keyboard)

    @dp.message_handler(commands=['help'])
    async def start(message: aiogram.types.Message):
        await message.reply('Список доступных команд:' '\n' + 'Переход к главному меню: /menu')



    @dp.message_handler(text=['Поехали 💖💖💖', 'вернуться в главное меню'])
    async def main_menu(message: aiogram.types.message):
        await message.answer("Выбери дальнейшее дейсвтие", reply_markup=temp_button_keyboard)


        @dp.callback_query_handler(text="Start")
        async def start_callback(query: CallbackQuery):
            await query.message.edit_text(text="Сохранено!")
            await query.message.answer("Выбери дальнейшее действие", reply_markup=temp_button_keyboard)

        @dp.message_handler(text='Создать заявку')
        async def cmd_start(message: types.Message):
            await Form.tag.set()
            await message.answer("Выбирай тег!", reply_markup=subjects_keyboard)


        @dp.message_handler(lambda message: (not message.text == "#математика"
                                             and not message.text == "#физика"
                                             and not message.text == "#программирование"
                                             and not message.text == "#ОПД"
                                             and not message.text == "#дискретка"
                                             and not message.text == "#английский"
                                             and not message.text == "#философия"
                                             and not message.text == "#ХОД"
                                             and not message.text == "#прочее"),state=Form.tag)
        async def process_tag_invalid(message: types.Message):
            return await message.reply("Используй теги с клавиатуры, не жульничай!.\n Давай попробуем еще раз!",
                                       reply_markup=subjects_keyboard)

        @dp.message_handler(state=Form.tag)
        async def process_name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['tag'] = message.text
            await Form.next()
            await message.answer("Какое будет оглавление?")

        @dp.message_handler(state=Form.title)
        async def process_age(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['title'] = message.text
            await Form.next()
            await message.answer("А текст заявки укажешь?")

        @dp.message_handler(state=Form.text)
        async def process_age(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['text'] = message.text
            await Form.next()
            await message.answer("Молодец, заявка успешно сохранена!", reply_markup=temp_button_keyboard)

            print(md.text("my tag", md.bold(data['tag'])),
                  md.text("my title", md.bold(data['title'])),
                  md.text("my text", md.bold(data['text'])), sep="\n")

        @dp.message_handler(text='Показать заявки')
        async def main_menu(message: aiogram.types.message):
            await message.answer("Не покажу заявки", reply_markup=temp_button_keyboard)

        @dp.message_handler(text='Настройки')
        async def main_menu(message: aiogram.types.message):
            await message.answer("Выбери дельнейшее дейсвтие", reply_markup=settings_keyboard)
##+++   ADD SUBJECTS
            @dp.callback_query_handler(text=["add_math"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#математика добавлена!")
                print("добавили #математика")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_phis"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#физика добавлена!")
                print("добавили #физика")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_proga"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#программирование добавлена!")
                print("добавили #программирование")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_OPD"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#ОПД добавлена!")
                print("добавили #ОПД")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_discr"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#дискретка добавлена!")
                print("добавили #дискретка")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_eng"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#английский добавлена!")
                print("добавили #английский")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_filosof"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#философия добавлена!")
                print("добавили #философия")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_XOD"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#ХОД добавлена!")
                print("добавили #ХОД")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)

            @dp.callback_query_handler(text=["add_another"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#прочее добавлена!")
                print("добавили #прочее")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_add)
##---   ADD SUBJECTS

##+++   REMOVE SUBJECTS
            @dp.callback_query_handler(text=["remove_math"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#математика удалена!")
                print("удалили #математика")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_phis"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#физика удалена!")
                print("удалили #физика")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_proga"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#программирование удалена!")
                print("удалили #программирование")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_OPD"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#ОПД удалена!")
                print("удалили #ОПД")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_discr"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#дискретка удалена!")
                print("удалили #дискретка")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_eng"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#английский удалена!")
                print("удалили #английский")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_filosof"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#философия удалена!")
                print("удалили #философия")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_XOD"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#ХОД удалена!")
                print("удалили #ХОД")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)

            @dp.callback_query_handler(text=["remove_another"])
            async def start_callback(query: CallbackQuery):
                await query.message.edit_text(text="#прочее удалена!")
                print("удалили #прочее")
                await query.message.answer("Выбери дальнейшее действие", reply_markup=select_subjects_keyboard_remove)


##---   REMOVE SUBJECTS

            @dp.message_handler(text='добавить теги в избранное')
            async def main_menu(message: aiogram.types.message):
                await message.answer("Добавь теги в любимые!", reply_markup=select_subjects_keyboard_add)

            @dp.message_handler(text='удалить теги из избранных')
            async def main_menu(message: aiogram.types.message):
                await message.answer("Убери теги из любимых!", reply_markup=select_subjects_keyboard_remove)





            @dp.message_handler(text='список заявок')
            async def main_menu(message: aiogram.types.message):
                await message.answer("Вывод список заявок")







if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)