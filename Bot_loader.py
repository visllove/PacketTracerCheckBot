import os
import json
import shutil
import subprocess
import asyncio
from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from webdav3.client import Client

# Поиск .env-файла с настройками
load_dotenv(find_dotenv)

data = json.loads(os.getenv('data'))
download_dir = os.getenv('download_dir')
bot_token = os.getenv('bot_token')
text_error = os.getenv('text_error')
text_start_message = os.getenv('text_start_message').replace('\\n', '\n')
text_format_error = os.getenv('text_format_error').replace('\\n', '\n')
text_format_error_length = os.getenv('text_format_error_length').replace('\\n', '\n')
cloud_dir = os.getenv('cloud_dir')
exe_name = os.getenv('exe_name')

dir_down = os.path.join(os.path.expanduser("~"), "Temp_bot")

if os.path.exists(os.path.join(os.path.expanduser("~"), "Temp_bot")):
    shutil.rmtree(dir_down)

if not os.path.exists(os.path.join(os.path.expanduser("~"), "Temp_bot")):
    dir_down = os.path.join(os.path.expanduser("~"), "Temp_bot")
    os.makedirs(dir_down)


client = Client(data)

router = Router()

API_TOKEN: str = bot_token

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Функция для стартового сообщения пользователю
while True:
    @dp.message(Command(commands=["start"]))
    async def process_start_command(message: Message):
        await message.answer(text_start_message)

# Парсинг полученного документа для его распределения в нужную папку
    async def get_document(message: Message):
        file = message.document
        file_id = file.file_id
        file_name = file.file_name

        if file_name.count(';') < 2:
            await message.answer(text_format_error)
            return -1
        elif len(file_name.strip()) < 11:
            await message.answer(text_format_error_length)
            return -1
        else:
            parts = file_name.split(';')
            file_form = parts[-1].split('.')
            lab_num = parts[0].strip()
            student = parts[1].strip()
            group = parts[-1].strip().upper()

            if 'doc' in parts[-1]:
                await message.answer(f'Получен отчет по {lab_num}, {student}')
            elif 'pka' in parts[-1]:
                await message.answer(f'Получен файл {lab_num}, {student}')
            else:
                await message.answer(f'Получен файл {lab_num}, {student}')

            if group.rfind('.'):
                group = group[:group.rfind('.')]
            file_nazv = lab_num + ' ' + student + ' ' + group

            if not os.path.exists(os.path.join(os.path.expanduser("~"), "Temp_bot")):
                os.makedirs(os.path.join(os.path.expanduser("~"), "Temp_bot"))

            group_dir = os.path.join(os.path.expanduser("~"), "Temp_bot") + '\\' + group

            file_path = os.path.join(group_dir, file_name)

            if not os.path.exists(group_dir):
                os.makedirs(group_dir)
            await bot.download(file_id, file_path)
            if not client.check(f"{cloud_dir}/{group}"):
                client.mkdir(f"{cloud_dir}/{group}")

            current_dir = os.getcwd()
            exe_file = exe_name
            exe_path = os.path.join(current_dir, exe_file)
            output = subprocess.check_output([exe_path, file_path], creationflags=subprocess.CREATE_NO_WINDOW)
            version: str = output.decode().strip()
            print(f"Получена работа {file_nazv}, ver {version[:6]}")
            try:
                client.upload_sync(remote_path=f"{cloud_dir}/{group}/{file_nazv}, ver {version[:6]}.{file_form[-1]}",
                                   local_path=file_path)
            finally:
                print(f"Сохранена работа {file_nazv}, ver {version[:6]}")
                await asyncio.sleep(2)

    # ответ с текстом ошибки при получении некорректного сообщения (например, с неправильным названием файла)
    async def send_echo(message: Message):
        await message.reply(text=text_error)

# запуск бота в режиме длинных запросов (long_polling)
    dp.message.register(get_document, F.document)
    dp.message.register(send_echo)
    if __name__ == '__main__':
        dp.run_polling(bot)
