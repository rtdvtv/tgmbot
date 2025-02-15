from aiogram.fsm.state import State, StatesGroup

class EchoBotState(StatesGroup): # Создаем класс состояний для эхо-бота
    enabled = State() # Состояние "включен"
    disabled = State() # Состояние "выключен"

# Состояния FSM
class IntervalSetting(StatesGroup):
    waiting_for_interval = State()  # Состояние ожидания

#  Класс для ввода интервала времени INTERVAL
class Interval(StatesGroup):
    time = State()
    # waiting_for_interval = State()