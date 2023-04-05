import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import threading
import requests
import sqlite3

token = "" #Токен от бота
openAi_key = "" #Ключик от api OpenAi
buttons_g = ["📥Сменить язык ввода", "📤Сменить язык вывода", "💾Какие сейчас языки?", "🆘Помощь"]

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

def connect():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor
conn, cursor = connect()

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("[ANTIFLOOD] - STOP! FUCK STOP!")
    
@dp.message_handler(Text(equals="💾Какие сейчас языки?"))
@dp.throttled(anti_flood,rate=3)
async def language(message: types.Message):
    cursor.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
    row = cursor.fetchone()
    conn.commit()
    await bot.send_message(message.chat.id, f"В данный момент у вас установлены языки:\n\nВаш код на: {row[2]}\nЯзык в которй конвертируется код: {row[3]}")
    
@dp.message_handler(Text(equals="🆘Помощь"))
@dp.throttled(anti_flood,rate=3)
async def help(message: types.Message):
    await bot.send_message(message.chat.id, "Возниклик проблемы?\nОбратись к кодеру, он поможет если ему не похуй: @CTOHKC")
    
@dp.message_handler(Text(equals="📥Сменить язык ввода"))
@dp.throttled(anti_flood,rate=3)
async def input_set(message: types.Message):
    cursor.execute(f"SELECT input FROM users WHERE user_id = {message.chat.id}")
    row = cursor.fetchone()
    conn.commit()
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Python", callback_data="set_input:Python"),
        types.InlineKeyboardButton(text="PHP", callback_data="set_input:PHP"),
        types.InlineKeyboardButton(text="C", callback_data="set_input:C"),
        types.InlineKeyboardButton(text="C#", callback_data="set_input:C#"),
        types.InlineKeyboardButton(text="C++", callback_data="set_input:C++"),
        types.InlineKeyboardButton(text="Kotlin", callback_data="set_input:Kotlin"),
        types.InlineKeyboardButton(text="Ruby", callback_data="set_input:Ruby"),
        types.InlineKeyboardButton(text="Rust", callback_data="set_input:Rust"),
        types.InlineKeyboardButton(text="JavaScript", callback_data="set_input:JavaScript"),
        types.InlineKeyboardButton(text="Java", callback_data="set_input:Java"),
        types.InlineKeyboardButton(text="Отмена", callback_data="set_input:Back")
        ]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, f"В данный момент язык вашей программы: {row[0]}\nВыберите новый язык:", reply_markup=keyboard)
    
@dp.message_handler(Text(equals="📤Сменить язык вывода"))
@dp.throttled(anti_flood,rate=3)
async def out_set(message: types.Message):
    cursor.execute(f"SELECT output FROM users WHERE user_id = {message.chat.id}")
    row = cursor.fetchone()
    conn.commit()
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Python", callback_data="set:Python"),
        types.InlineKeyboardButton(text="PHP", callback_data="set:PHP"),
        types.InlineKeyboardButton(text="C", callback_data="set:C"),
        types.InlineKeyboardButton(text="C#", callback_data="set:C#"),
        types.InlineKeyboardButton(text="C++", callback_data="set:C++"),
        types.InlineKeyboardButton(text="Kotlin", callback_data="set:Kotlin"),
        types.InlineKeyboardButton(text="Ruby", callback_data="set:Ruby"),
        types.InlineKeyboardButton(text="Rust", callback_data="set:Rust"),
        types.InlineKeyboardButton(text="JavaScript", callback_data="set:JavaScript"),
        types.InlineKeyboardButton(text="Java", callback_data="set:Java"),
        types.InlineKeyboardButton(text="Отмена", callback_data="set:Back")
        ]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, f"В данный момент у вас для конвертации установлен язык: {row[0]}\nВыберите новый язык:", reply_markup=keyboard)
    
@dp.message_handler(commands="start")
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message):
    cursor.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
    row = cursor.fetchone()
    conn.commit()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons_g)
    if row != None:
        await bot.send_message(message.chat.id, "Вы уже авторизованы в боте!", reply_markup=keyboard)
    else:
        cursor.execute(f"INSERT INTO users(user_id) VALUES ({message.chat.id})")
        conn.commit()
        keyboard_one = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="Python", callback_data="save:Python"),
            types.InlineKeyboardButton(text="PHP", callback_data="save:PHP"),
            types.InlineKeyboardButton(text="C", callback_data="save:C"),
            types.InlineKeyboardButton(text="C#", callback_data="save:C#"),
            types.InlineKeyboardButton(text="C++", callback_data="save:C++"),
            types.InlineKeyboardButton(text="Kotlin", callback_data="save:Kotlin"),
            types.InlineKeyboardButton(text="Ruby", callback_data="save:Ruby"),
            types.InlineKeyboardButton(text="Rust", callback_data="save:Rust"),
            types.InlineKeyboardButton(text="JavaScript", callback_data="save:JavaScript"),
            types.InlineKeyboardButton(text="Java", callback_data="save:Java")
        ]
        keyboard_one.add(*buttons)
        await bot.send_message(message.chat.id, "Добро пожаловать в бота для конвертации языков программирования!\n\nКак использовать бота:\n1. Выбери язык программирования на котором написан твой код\n2. Отправь мне код\n3. Выбери язык в который нужно переконвертировать твой код\n4. Держи результат\nТак же не забываем про ограничения сообщений телеграм!", reply_markup=keyboard)
        await bot.send_message(message.chat.id, "Выберите язык на котором написан ваш код:", reply_markup=keyboard_one)
    
@dp.message_handler(content_types=["text"]) 
@dp.throttled(anti_flood,rate=6)
async def convert(message: types.Message):
    cursor.execute(f"SELECT output FROM users WHERE user_id = {message.chat.id}")
    row = cursor.fetchone()
    conn.commit()
    print(row[0])
    if row[0] == None:
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="Python", callback_data="convert:Python"),
            types.InlineKeyboardButton(text="PHP", callback_data="convert:PHP"),
            types.InlineKeyboardButton(text="C", callback_data="convert:C"),
            types.InlineKeyboardButton(text="C#", callback_data="convert:C#"),
            types.InlineKeyboardButton(text="C++", callback_data="convert:C++"),
            types.InlineKeyboardButton(text="Kotlin", callback_data="convert:Kotlin"),
            types.InlineKeyboardButton(text="Ruby", callback_data="convert:Ruby"),
            types.InlineKeyboardButton(text="Rust", callback_data="convert:Rust"),
            types.InlineKeyboardButton(text="JavaScript", callback_data="convert:JavaScript"),
            types.InlineKeyboardButton(text="Java", callback_data="convert:Java")
        ]
        keyboard.add(*buttons)
        await bot.send_message(message.chat.id, "Выберите язык в который будет переконвертирован ваш код:", reply_markup=keyboard)
    elif row[0] != None:
        cursor.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
        row = cursor.fetchone()
        check = await bot.send_message(message.chat.id, f"🔄Конвертирую ваш {row[2]} в {row[3]}...")
        headers = {
            'authority': 'ai-code-translator.vercel.app',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://ai-code-translator.vercel.app',
            'referer': 'https://ai-code-translator.vercel.app/',
            'sec-ch-ua': '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52',
        }
        json_data = {
            'inputLanguage': f'{row[2]}',
            'outputLanguage': f'{row[3]}',
            'inputCode': message.text,
            'model': 'gpt-3.5-turbo',
            'apiKey': openAi_key,
        }
        response = requests.post('https://ai-code-translator.vercel.app/api/translate', headers=headers, json=json_data)
        await check.edit_text(response.text)
    
@dp.callback_query_handler()
async def process_callback_button(callback_query: CallbackQuery): #Аня я тебя очень сильно люблю, именно ты вдохновляешь меня делать какие то новые проекты
    action = callback_query.data
    func = action.split(":")[0]
    if func == "save":
        cursor.execute(f"UPDATE users SET input = '{action.split(':')[1]}' WHERE user_id = {callback_query.message.chat.id}")
        conn.commit()
        await callback_query.message.edit_text(f"Ваш язык ввода был изменён на {action.split(':')[1]}")
    if func == "convert":
        cursor.execute(f"UPDATE users SET output = '{action.split(':')[1]}' WHERE user_id = {callback_query.message.chat.id}")
        conn.commit()
        cursor.execute(f"SELECT input FROM users WHERE user_id = {callback_query.message.chat.id}")
        row = cursor.fetchone()
        print(row)
        await callback_query.message.edit_text(f"🔄Конвертирую ваш {row[0]} код в {action.split(':')[1]} код...")
        headers = {
            'authority': 'ai-code-translator.vercel.app',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://ai-code-translator.vercel.app',
            'referer': 'https://ai-code-translator.vercel.app/',
            'sec-ch-ua': '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52',
        }
        json_data = {
            'inputLanguage': f'{row[0]}',
            'outputLanguage': f'{action.split(":")[1]}',
            'inputCode': callback_query.message.text,
            'model': 'gpt-3.5-turbo',
            'apiKey': openAi_key,
        }
        response = requests.post('https://ai-code-translator.vercel.app/api/translate', headers=headers, json=json_data)
        await callback_query.message.edit_text(f"{response.text}")
    if func == "set":
        if action.split(':')[1] == "Back":
            await callback_query.message.edit_text(f"Смена языка отменена!")
        else:
            cursor.execute(f"UPDATE users SET output = '{action.split(':')[1]}' WHERE user_id = {callback_query.message.chat.id}")
            conn.commit()
            await callback_query.message.edit_text(f"Теперь язык на который будет переводиться ваш код {action.split(':')[1]}")
    if func == "set_input":
        if action.split(':')[1] == "Back":
            await callback_query.message.edit_text(f"Смена языка отменена!")
        else:
            cursor.execute(f"UPDATE users SET input = '{action.split(':')[1]}' WHERE user_id = {callback_query.message.chat.id}")
            conn.commit()
            await callback_query.message.edit_text(f"Язык вашей программы был изменён на {action.split(':')[1]}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)