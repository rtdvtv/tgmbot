import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from status_str import StreamStatusChecker
from keyboards import (
    get_start_keyboard, get_main_menu_keyboard, get_setup_keyboard, get_interval_keyboard,
    get_url_str_keyboard, get_admin_keyboard, get_help_keyboard, get_sound_keyboard,
    get_info_keyboard, get_str_info_keyboard, get_set_interval_keyboard, get_show_interval_keyboard, get_check_keyboard
)
from handlers import (
    handle_setup, handle_interval, handle_go_back, handle_url_str, handle_admin,
    handle_help, handle_sound, handle_info, IntervalSetting, handle_ai_menu, handle_check_status)
# handle_set_interval, handle_set_new_interval, handle_show_interval
from mbot_echo import register_echo_handlers

#from mbot_echo import (cmd_start, handle_run, echo_on_command, echo_off_command, echo_bot, register_echo_handlers)
from db_mbot import initialize_database, connection, save_message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import BOT_TOKEN, CHAT_ID, m3u8_url
from ai_chat import main_mistral


# # URL для потока
# m3u8_url = "http://cdn-br2.live-tv.cloud:8081/tgtv/1080i/playlist.m3u8"


# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
# dp = Dispatcher(storage=MemoryStorage())

# Инициализация базы данных
initialize_database()

# Состояния FSM
# class IntervalSetting(StatesGroup):
#     waiting_for_interval = State()  # Состояние ожидания

### Регистрация всех Handlers
#def register_handlers():
    # dp.message.register(cmd_start, Command("start"))
    # dp.message.register(handle_run, F.text == "RUN")
    # dp.message.register(handle_setup, F.text == "SETUP")
    # dp.message.register(handle_interval, F.text == "INTERVAL")
    # dp.message.register(handle_url_str, F.text == "URL_STR")
    # dp.message.register(handle_admin, F.text == "ADMIN")
    # dp.message.register(handle_help, F.text == "HELP")
    # dp.message.register(handle_sound, F.text == "SOUND")
    # dp.message.register(handle_info, F.text == "INFO")
    # dp.message.register(handle_check_status, F.text == "CHECK")
    # dp.message.register(set_interval, F.text == "SET")
    # dp.message.register(set_new_interval, StateFilter(IntervalSetting.waiting_for_interval))
    # dp.message.register(show_interval, F.text == "SHOW")
    # dp.message.register(echo_bot, F.text == "AI")
    # dp.message.register(handle_go_back, F.text == "BACK")
    # dp.message.register(send_to_chat, Command("send"))
    # dp.message.register(echo_on_command, Command("echo_on"))
    # dp.message.register(echo_off_command, Command("echo_off"))
    # dp.message.register(echo_bot, ~F.text.startswith("/"))  # echo_bot - *после* команд!



### БД Завершение
async def shutdown():
    print("Отключение бота и закрытие соединения с базой данных...")
    connection.close()



# Пример использования отправки сообщения
async def send_to_chat(message: Message):
    """
    Тестовая команда отправки сообщения по chat_id из config.py.
    Вызов: /send
    """
    await send_message(CHAT_ID, "Это сообщение отправлено в чат из Python-кода!")
    await message.answer("Сообщение успешно отправлено в указанный чат!")

### Главная функция
async def main():
    dp = Dispatcher()
    register_echo_handlers(dp)  #
    '''Передаем dp в функцию регистрации из echo_bot.py
    # register_handlers() # Передаем dp в функцию регистрации из mbot.py'''

    stream_checker = StreamStatusChecker(m3u8_url)  # Экземпляр StreamStatusChecker
    # stream_checker.start_monitoring(chat_id=CHAT_ID, bot=bot)  # Передаем CHAT_ID и bot из config.py




    print("Бот запущен и пашет как коняка!")
    try:
        # Запускаем мониторинг сразу после запуска бота
        stream_checker.start_monitoring(chat_id=520410415, bot=bot)  # Указываем ваш chat_id
        # Удаляем вебхуки, если есть
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот остановлен!")
    finally:
        await shutdown()


if __name__ == "__main__":
    asyncio.run(main())