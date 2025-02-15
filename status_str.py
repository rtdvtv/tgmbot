# import types

import aiohttp
import asyncio
import logging
import m3u8

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from class_bot import Interval

dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StreamStatusChecker:
    def __init__(self, m3u8_url: str, default_interval: int = 300):
        self.m3u8_url = m3u8_url
        self.current_interval = max(default_interval, 60)  # Интервал по умолчанию, но не менее 60 сек.
        self.is_stream_online = False
        self.task = None


    # Этот блок дублировал блок ниже выполняя такую же функцию. Пока отключил
    async def monitor_stream(self, chat_id: int, bot):
        """Мониторим поток в фоне."""
        while True:
            try:
                status = await self.check_stream_status()
                if status != self.is_stream_online:
                    self.is_stream_online = status
                    if status:
                        green_circle = '\U0001F7E2'
                        await bot.send_message(chat_id, f"{green_circle} Status: Run-Stream ONLINE")
                        logging.info("Log:Run-Stream-ONLINE")
                    else:
                        red_circle = '\U0001F534'
                        await bot.send_message(chat_id, f"{red_circle} Status: Stream-Error OFFLINE")
                        logging.error("Log:Stream-Error-OFFLINE")
            except Exception as e:
                logging.exception(f"ERROR в monitor_stream: {e}")
            await asyncio.sleep(self.current_interval)
            print("Monitor_Stream")

    def start_monitoring(self, chat_id: int, bot):
        """Запускаем мониторинг в фоне."""
        if self.task is None:
            try:
                self.task = asyncio.create_task(self.monitor_stream(chat_id, bot))
                logging.info("Запущен мониторинг потока")
            except Exception as e:
                logging.exception(f"Ошибка запуска мониторинга: {e}")

    async def check_stream_status(self) -> bool:
        """
        Проверяю доступность потока (m3u8). Возвращаем True, если доступен, иначе False.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.m3u8_url, timeout=10) as response:
                    return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:  # Ловим конкретные исключения
            logging.error(f"Ошибка проверки статуса потока: {e}")  # Логируем ошибку
            print("check_stream_status")
            return False

def start_monitoring(self, chat_id: int, bot):
        """
        Запускаем мониторинг в фоне только один раз.
        """
        if self.task is None:  # Проверяем, не запущена ли уже задача
            self.task = asyncio.create_task(self.monitor_stream(chat_id, bot))
            print("start_monitoring")

# Функции для работы с интервалом (INTERVAL->(SET/SHOW))
@dp.message(Command("set_interval"))
async def command_set_interval(message: Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста, введите только числовое значение"),
    await state.set_state(Interval.time)

@dp.message(Interval.time)
async def set_new_interval(message: Message, state: FSMContext) -> None:
    try:
        time = int(message.text)  # Получаем message.text *внутри* функции
        if time < 60:
            await message.reply("Интервал не может быть меньше 60 секунд.")
            return

        await state.update_data(time=time)
        current_state = await state.get_state()
        await message.answer(f"Интервал обновлен: {current_state} секунд.")
        await state.clear()
        print(set_new_interval)

    except ValueError:
        await message.reply("Пожалуйста, введите только числовое значение")
        return

    except Exception as e:
        logging.error(f"Ошибка при установке интервала: {e}")
        await message.reply("Произошла ошибка при установке интервала. Попробуйте еще раз.")
        return
# @dp.message(Interval.time)
# async def set_new_interval(message: Message, state: FSMContext) -> None:
#     time = int(message.text)
#     await state.update_data(time=time)  # Обновляем данные в state
#     await message.answer(f"Интервал обновлен: {time} секунд.")
#     await state.clear()
#     print(set_new_interval)

# запрос информации о потоке - через кнопку STR_INFO
# вывод информации через CHAT_ID
async def get_stream_info(self):
    """Получаем информацию о потоке (битрейт, разрешение)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.m3u8_url, timeout=10) as response:
                if response.status == 200:
                    playlist_content = await response.text()
                    playlist = m3u8.loads(playlist_content)  # загружаем m3u8
                    # Получаем информацию о вариантах потока
                    streams = []
                    for variant in playlist.playlists:
                        resolution = variant.stream_inf.resolution
                        bandwidth = variant.stream_inf.bandwidth
                        streams.append({
                            "resolution": resolution,
                            "bandwidth": bandwidth
                        })
                    return streams
                else:
                    logging.error(f"Ошибка получения m3u8: {response.status}")
                    return None
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.error(f"Ошибка запроса m3u8: {e}")
        return None

# BITRATE stream - запрос битрейта потока - через кнопку STR_INFO
async def get_bitrate(self):
    """Получаем битрейт потока."""
    stream_info = await self.get_stream_info()
    if stream_info:
        bitrates = [stream['bandwidth'] for stream in stream_info]
        return bitrates
    return None

# RESOLUTION screen - запрос разрешение экрана - через кнопку STR_INFO
async def get_resolution(self):
    """Получаем разрешение видео."""
    stream_info = await self.get_stream_info()
    if stream_info:
        resolutions = [stream['resolution'] for stream in stream_info]
        return resolutions
    return None

# @dp.message(commands=("INFO"), state=None)
# async def handle_show_stream_info(message: types.Message):
#     await message.answer("Пожалуйста, введите только числовое значение")