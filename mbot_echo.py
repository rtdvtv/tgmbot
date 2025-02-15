from aiogram import types, F, Dispatcher
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from ai_chat import main_mistral
# from mbot import IntervalSetting
from handlers import (
    handle_setup, handle_interval, handle_go_back, handle_url_str, handle_admin,
    handle_help, handle_sound, handle_info, #handle_set_interval,
    IntervalSetting, handle_ai_menu, handle_check_status) #check_status,
# from status_str import handle_set_new_interval, handle_show_interval
from db_mbot import save_message
from keyboards import get_start_keyboard, get_main_menu_keyboard
from class_bot import EchoBotState, Interval
from status_str import command_set_interval, set_new_interval
#handle_show_stream_info

#from handlers import register_handlers


# class EchoBotState(StatesGroup): # Создаем класс состояний для эхо-бота
#     enabled = State() # Состояние "включен"
#     disabled = State() # Состояние "выключен"

dp = Dispatcher()
#echo_bot_enabled = False
# КОМАНДЫ для запуска эхо-бота

def register_echo_handlers(dp: Dispatcher):  # Принимаем dp как аргумент
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_run, F.text == "RUN")
    # dp.message.register(echo_on_command, Command("echo_on"))
    # dp.message.register(echo_off_command, Command("echo_off"))
    dp.message.register(handle_ai_menu, F.text == "AI")
    dp.message.register(echo_enabled, F.text == "ON")
    dp.message.register(echo_disabled, F.text == "OFF")
    dp.message.register(handle_setup, F.text == "SETUP")
    dp.message.register(handle_interval, F.text == "INTERVAL")
    dp.message.register(handle_url_str, F.text == "URL_STR")
    dp.message.register(handle_admin, F.text == "ADMIN")
    dp.message.register(handle_help, F.text == "HELP")
    dp.message.register(handle_sound, F.text == "SOUND")
    # dp.message.register(handle_show_stream_info, F.text == "INFO")
    dp.message.register(handle_check_status, F.text == "CHECK")
    dp.message.register(command_set_interval, F.text == "SET")
    # dp.message.register(Interval.time)(set_new_interval)  # Регистрируем обработчик для состояния Interval.time!!!!!!!!!!!!!!!!
    dp.message.register(set_new_interval, StateFilter(IntervalSetting.waiting_for_interval))
    # dp.message.register(handle_show_interval, F.text == "SHOW")
    # dp.message.register(online_menu_handler, F.text == "ONLINE-TV")
    dp.message.register(handle_go_back, F.text == "BACK")
    #dp.message.register(handle_escape, F.text == "ESCAPE")
    dp.message.register(echo_bot, ~F.text.startswith("/"))  # echo_bot - *после* команд!



async def cmd_start(message: Message):
    print("cmd_start:", message.text)  # Выводим текст сообщения
    try:
        save_message(
            user_id=message.from_user.id,
            user_name=message.from_user.full_name,
            message_text=message.text
        )
    except Exception as e:
        print(f"Ошибка при сохранении сообщения: {e}")

    # Приветственное сообщение
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Нажмите кнопку RUN, чтобы запустить программу.",
        reply_markup=get_start_keyboard())

async def handle_run(message: Message):
    print("handle_run:", message.text)  # Выводим текст сообщения
    green_circle = '\U0001F7E2'  # Зеленый кружок
    await message.answer(
        f"{green_circle} Программа инициализирована!\n\n"
        "Для запуска функционала в режиме автоматического мониторинга нажмите на кнопку CHECK. "
        "\n\nПосле обновления статуса потока программа перейдет в автоматический режим.\n"
        "Для ознакомления с функционалом перейдите в меню HELP, для тонкой настройки — в меню SETUP.",
        reply_markup=get_main_menu_keyboard())

# Функция "ON" для запуска ЭХОБОТА по кнопке
# @dp.message(F.text == "ON")
@dp.message(Command("ON"))
async def echo_enabled(message: types.Message, state: FSMContext):
    await state.set_state(EchoBotState.enabled)
    green_circle = '\U0001F7E2'
    await message.reply(f"{green_circle} AiChat включен.")


@dp.message(Command("OFF"))  # Обработчик для кнопки OFF
async def echo_disabled(message: types.Message, state: FSMContext):
    await state.set_state(EchoBotState.disabled)
    red_circle = '\U0001F534'
    await message.reply(f"{red_circle} AiChat выключен.")
    await message.answer(  # Переход в главное меню
        "Вы перешли в Главное меню",
        reply_markup=get_main_menu_keyboard()
    )

# ЭХОБОТ с интеграцией в МИСТРАЛ (модуль "ai_chat"
@dp.message(~F.text.startswith("/"))  # Первый обработчик
async def echo_bot(message: types.Message, state: FSMContext):
    current_state = await state.get_state()  # Получаем текущее состояние
    if current_state == EchoBotState.enabled.state:  # Проверяем, включен ли эхо-бот
        try:
            content = message.text
            res = await main_mistral(content)
            await message.answer(res)
        except TypeError:
            await message.reply(message.text)
    #else: # Если нужно какое-то сообщение для отключенного состояния
    #    await message.reply("Эхо-бот отключен.")

