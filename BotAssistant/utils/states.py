from aiogram.fsm.state import StatesGroup, State

class Exchange(StatesGroup):
    valute_exchange = State()
    valute_count = State()


class CalcExpression(StatesGroup):
    result = State()

