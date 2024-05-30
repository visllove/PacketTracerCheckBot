# PacketTracerCheckBot
A bot for distributing .pka files into specific folders by groups

**Create a .env-file with next parameters:**

data = *данные для подключения к серверу*

download_dir = *путь к папке с загруженными .pka-файлами и отчетами*

bot_token = *Токен вашего Telegram-бота*

text_error = "Бот принимает только .pka-файлы и отчеты, пожалуйста, учтите это при следующей отправке"

text_start_message = "Привет!\nБот принимает файлы .pka и отчеты с названиями в формате\n<Номер работы> ; <Фамилия И.О.> ; <Группа>\nЗаполнять на русском языке!\nХорошего дня!"

text_format_error = "Формат названия неверный, не забывайте про ';'"

text_format_error_length = "Формат названия неверный, название файла слишком короткое"

cloud_dir = *Путь к директории в облаке (на облачном сервере)*

exe_name = *название exe-файла*
