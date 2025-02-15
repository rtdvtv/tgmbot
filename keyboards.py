from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher


# Клавиатура с начальной кнопкой "RUN"
def get_start_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="RUN")]], # Одна кнопка в строке после команды START
    resize_keyboard=True)

# Клавиатура с начальной кнопкой "CHECK"
def get_check_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="CHECK")]], # Кнопка в главном меню
    resize_keyboard=True)

# Клавиатура с начальной кнопкой "BACK"
def get_go_back():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="BACK")]], # Одна кнопка из каждого подменю возврат в Главное меню
    resize_keyboard=True)

# Клавиатура с начальной кнопкой "STOP"
def get_go_back():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="STOP")]], # Кнопка в главном меню
    resize_keyboard=True)

# ГЛАВНОЕ МЕНЮ с кнопками RUN, CHECK, STOP (первая строка)
# и SETUP, INFO, ONLINE (вторая строка)
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="CHECK"),  # Первая строка
            KeyboardButton(text="ONLINE"),
            KeyboardButton(text="STOP")],
        [KeyboardButton(text="SETUP"),  # Вторая строка
            KeyboardButton(text="STR-INFO"),
            KeyboardButton(text="HELP")]
    ], resize_keyboard=True)

# Подменю для кнопки SETUP
def get_setup_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="INTERVAL"),  KeyboardButton(text="URL-STR"),
            KeyboardButton(text="SOUND")],
        [KeyboardButton(text="ADMIN"), KeyboardButton(text="BACK")]],
        resize_keyboard=True)


# Подменю для кнопки INTERVAL
def get_interval_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SET"), KeyboardButton(text="SHOW"), KeyboardButton(text="BACK")]],
        resize_keyboard=True)


# Подменю для кнопки URL-STR
def get_url_str_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="SET_URL"),KeyboardButton(text="URL_LIST"), KeyboardButton(text="DEL_URL")],
            [KeyboardButton(text="LOG"), KeyboardButton(text="BACK")]],    # Вторая строка: кнопка BACK
        resize_keyboard=True)


# Подменю для кнопки ADMIN
def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="BUT1"), KeyboardButton(text="BUT2"), KeyboardButton(text="BUT3")],
            [KeyboardButton(text="SUPPOR"), KeyboardButton(text="BACK")]], # Вторая строка: кнопка BACK
        resize_keyboard=True)

# Подменю для кнопки HELP
def get_help_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SCHEDULER"), KeyboardButton(text="COMMAND"), KeyboardButton(text="INFO")],
            [KeyboardButton(text="AI"), KeyboardButton(text="BACK")]],  # Вторая строка: кнопка BACK
            resize_keyboard=True)

# Подменю для кнопки AI
def get_ai_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ON"), KeyboardButton(text="OFF")]],  # Кнопка OFF это стоп для ИИ и выход в меню
            resize_keyboard=True)

# Подменю для кнопки SOUND
def get_sound_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SILENT"), KeyboardButton(text="SPEAKER"), KeyboardButton(text="BACK")]],
            resize_keyboard=True)


# Клавиатура с начальной кнопкой "INFO"
def get_info_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="INFO"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для вызова ответного сообщения с описанием программы и контактов автора

# Клавиатура с начальной кнопкой "STR-INFO"
def get_str_info_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="STR_INFO"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для вызова ответного сообщения с описанием параметров потока

# Клавиатура с начальной кнопкой "SET"
def get_set_interval_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="SET"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для ввода временного интервала для мониторинга потока

# Клавиатура с начальной кнопкой "SHOW"
def get_show_interval_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="SHOW"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для просмотра установленного интервала времени обращений для мониторинга потока