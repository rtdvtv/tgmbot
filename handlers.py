import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from status_str import StreamStatusChecker
from keyboards import (
    get_start_keyboard, get_main_menu_keyboard, get_setup_keyboard, get_interval_keyboard,
    get_url_str_keyboard, get_admin_keyboard, get_help_keyboard, get_sound_keyboard,
    get_info_keyboard, get_ai_keyboard, get_check_keyboard, get_str_info_keyboard, get_set_interval_keyboard, get_show_interval_keyboard)
from db_mbot import initialize_database, connection, save_message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import BOT_TOKEN, CHAT_ID, m3u8_url
from url_setting import (set_url_handler, save_url_handler, show_url_handler, delete_url_handler, show_log_handler, UrlSetting)
from class_bot import IntervalSetting
# # Состояния FSM
# class IntervalSetting(StatesGroup):
#     waiting_for_interval = State()  # Состояние ожидания
stream_checker = StreamStatusChecker(m3u8_url)  # Экземпляр StreamStatusChecker

# Обработчик кнопки BACK
async def handle_go_back(message: Message, ):
    await message.answer(
        "Вы перешли в Главное меню",
        reply_markup=get_main_menu_keyboard())

# #Обработчик кнопки ESCAPE
# async def handle_escape(message: Message, ):
#     await message.answer(
#         "Вы перешли в Главное меню",
#         reply_markup=get_main_menu_keyboard())

# Обработчик кнопки SETUP
async def handle_setup(message: Message):
    await message.answer(
        "Раздел SETUP. \nВыберите нужный пункт:",
        reply_markup=get_setup_keyboard())

# Обработчик кнопки INTERVAL
async def handle_interval(message: Message):
    await message.answer(
        "HANDLERS - handle_interval\n"
        "Устанавливаем интервал запроса статуса потока"
        "в фоновом режиме (не менее 60 секунд)\n"
        "Введите время в секундах:",
        reply_markup=get_interval_keyboard())

# Обработчик кнопки URL_STR
async def handle_url_str(message: Message):
    await message.answer(
        "Раздел URL_STR. \nВыберите нужный пункт:",
        reply_markup=get_url_str_keyboard())

# Обработчик кнопки ADMIN
async def handle_admin(message: Message):
    await message.answer(
        "Раздел ADMIN. \nВыберите нужный пункт:",
        reply_markup=get_admin_keyboard())

# Обработчик кнопки HELP
async def handle_help(message: Message):
    await message.answer(
        "Раздел HELP. \nВыберите нужный пункт:",
        reply_markup=get_help_keyboard())

# Обработчик кнопки SOUND
async def handle_sound(message: Message):
    await message.answer(
        "Раздел SOUND. \nВыберите нужный пункт:",
        reply_markup=get_sound_keyboard())

# Обработчик кнопки INFO
async def handle_info(message: Message):
    await message.answer(
        "Раздел INFO. \nВыберите нужный пункт:",
        reply_markup=get_info_keyboard())


# AI - обработка кнопки с подменю
async def handle_ai_menu(message: Message):
    yellow_circle = '\U0001F7E0'  # Зеленый кружок
    await message.answer(
        f"{yellow_circle} Для запуска 'AiChat' нажмите кнопку 'ON'."
        "\n\nТеперь вы можете использовать строку для ввода запросов в чат.\n"
        "Для завершения работы 'AiChat' и перехода в режим мониторинга"
        " нажмите кнопку 'OFF', затем 'BACK' для возврата функционала."
        "\n\nВо время использования чата, мониторинг работает в фоне и при изменении статуса"
        " потока выведет соответствующее уведомление не смотря на работу 'AiChat'.",
        reply_markup=get_ai_keyboard())


async def handle_check_status(message: Message):
    status = await stream_checker.check_stream_status()
    if status:
        yellow_triangle = '\U0001F7E1'
        await message.answer(f"{yellow_triangle} Обновление")
        await asyncio.sleep(2)
        green_circle = '\U0001F7E2'
        await message.answer(f"{green_circle} Check-Status: ONLINE")
    else:
        red_circle = '\U0001F534'
        await message.answer(f"{red_circle} Check-Status: OFFLINE")
        print("Def Check_status")

#
# # Отправка сообщения от имени бота любому чату (по ID).
# async def send_message(bot: Bot, chat_id: int, text: str):
#     await bot.send_message(chat_id, text)
#
# # Пример использования отправки сообщения
# async def send_to_chat(message: Message, bot: Bot):
#     """
#     Тестовая команда отправки сообщения по chat_id из config.py.
#     Вызов: /send
#     """
#     await send_message(bot, CHAT_ID, "Это сообщение отправлено в чат из Python-кода!")
#     await message.answer("Сообщение успешно отправлено в указанный чат!")
# CHECK - запрос статуса потока пользователем

async def handle_show_stream_info(message: types.Message, state: FSMContext):
    """Показываем информацию о потоке."""
    stream_checker = await state.get_data("stream_checker")
    if not stream_checker:
        await message.reply("Сначала нужно инициализировать stream_checker.")
        return

    stream_info = await stream_checker.get_stream_info()

    if stream_info:
        message_text = "Информация о потоке:\n"
        for stream in stream_info:
            message_text += f"Разрешение: {stream['resolution']}, Битрейт: {stream['bandwidth']}\n"
        await message.reply(message_text)
    else:
        await message.reply("Не удалось получить информацию о потоке.")
