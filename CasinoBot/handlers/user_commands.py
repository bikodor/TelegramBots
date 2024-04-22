from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import generator_buttons
from utils.states import Username
from data.db import edit_username, add_user, find_user, check_bonus

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = find_user(message)
    if user:
        await check_bonus(message=message)
        await message.answer(f'Рад тебя видеть, {user.username}, во что поиграем?', reply_markup=generator_buttons(['♠️ Блэкджек ♠️', '🎰 Игровые автоматы 🎰', '🔴 Рулетка ⚫️', '🎲 Кости 🎲', '👤 Профиль 👤'], ['blackjack', 'casino', 'roulette', 'bones', 'profile'], 1))
    else:
        await state.set_state(Username.username)
        await message.answer(f'Привет, {message.from_user.first_name}! Меня зовут Бот Джо и я являюсь крупье во всех играх, представленных здесь, укажите ваш псевдоним, под которым вы будете играть (его будут видеть все игроки)')

@router.message(Username.username)
async def set_username(message: Message, state: FSMContext):
    username = message.text
    user = find_user(message)
    if user is None:
        add_user(message)
        await edit_username(username, message)
        user = find_user(message)
    else:
        await edit_username(username, message)
        user = find_user(message)
    if user is not None and user.username:
        await state.clear()
        await message.answer(f'Псевдоним успешно добавлен, {user.username}, в какую игру сыграем?', reply_markup=generator_buttons(['♠️ Блэкджек ♠️', '🎰 Игровые автоматы 🎰', '🔴 Рулетка ⚫️', '🎲 Кости 🎲', '👤Профиль👤'], ['blackjack', 'casino', 'roulette', 'bones', 'profile'], 1))
        await check_bonus(message=message)
