import json
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN

# --- Проверка или создание файла containers.json ---
if not os.path.exists('containers.json'):
    with open('containers.json', 'w') as file:
        json.dump({"containers": []}, file)

# --- Функции для работы с контейнерами ---
def add_container(container_number):
    with open('containers.json', 'r') as file:
        data = json.load(file)
    if container_number not in data["containers"]:
        data["containers"].append(container_number)
        with open('containers.json', 'w') as file:
            json.dump(data, file)
        return f"Контейнер {container_number} добавлен."
    return f"Контейнер {container_number} уже существует."

def remove_container(container_number):
    with open('containers.json', 'r') as file:
        data = json.load(file)
    if container_number in data["containers"]:
        data["containers"].remove(container_number)
        with open('containers.json', 'w') as file:
            json.dump(data, file)
        return f"Контейнер {container_number} удалён."
    return f"Контейнер {container_number} не найден."

def list_containers():
    with open('containers.json', 'r') as file:
        data = json.load(file)
    return "\n".join(data["containers"]) if data["containers"] else "Список пуст."

# --- Команды Telegram ---
def start(update, context):
    update.message.reply_text(
        "Привет! Я бот для трекинга контейнеров. Вот что я умею:\n"
        "/add <номер контейнера> - Добавить контейнер\n"
        "/remove <номер контейнера> - Удалить контейнер\n"
        "/list - Показать список контейнеров\n"
        "/help - Показать справку"
    )

def add_command(update, context):
    if not context.args:
        update.message.reply_text("Пожалуйста, укажите номер контейнера: /add <номер>")
        return
    container_number = context.args[0]
    message = add_container(container_number)
    update.message.reply_text(message)

def remove_command(update, context):
    if not context.args:
        update.message.reply_text("Пожалуйста, укажите номер контейнера: /remove <номер>")
        return
    container_number = context.args[0]
    message = remove_container(container_number)
    update.message.reply_text(message)

def list_command(update, context):
    message = list_containers()
    update.message.reply_text(f"Текущий список контейнеров:\n{message}")

def help_command(update, context):
    update.message.reply_text(
        "Вот что я умею:\n"
        "/add <номер контейнера> - Добавить контейнер\n"
        "/remove <номер контейнера> - Удалить контейнер\n"
        "/list - Показать список контейнеров\n"
        "/help - Показать справку"
    )

# --- Основной код бота ---
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_command))
    dp.add_handler(CommandHandler("remove", remove_command))
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()