from aiogram.fsm.state import StatesGroup, State

class Username(StatesGroup):
    username = State()

class UsernameEdit(StatesGroup):
    username = State()

class SetBet_Bones(StatesGroup):
    bet = State()

class SetBet_Casino(StatesGroup):
    bet = State()

class SetBet_Roulette(StatesGroup):
    bet = State()

class Roulette_Action(StatesGroup):
    action = State()

class SetBet_Blackjack(StatesGroup):
    bet = State()