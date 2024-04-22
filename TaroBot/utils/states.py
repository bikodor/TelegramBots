from aiogram.fsm.state import StatesGroup, State

class Zodiac(StatesGroup):
    zodiac = State()


class YesOrNot(StatesGroup):
    question = State()