from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.inline import generator_buttons, zodiac_signs
from aiogram.fsm.context import FSMContext
from utils.states import Zodiac, YesOrNot
from data.db import get_zodiac_tip_day
from parse_taro import parse_layout, tarot_cards_with_values



router = Router()

@router.message(CommandStart())
async def start(message: Message, state:FSMContext):
    await state.clear()
    await message.answer(f'Привет, {message.from_user.first_name}! Я Таро Бот.\n'
                         f'Выбери расклад:', reply_markup=generator_buttons(['🔮 Совет дня 🔮', '🔮 Расклад на любовь и отношения 🔮', '🔮 Расклад на работу и финансы 🔮', '🔮 Расклад "Да или Нет" 🔮'],['tip_day', 'layout_love', 'layout_money', 'layout_yes_or_not'], 1))

@router.callback_query(F.data == 'tip_day')
async def tip_day(query: CallbackQuery, state:FSMContext):
    await state.set_state(Zodiac.zodiac)
    await query.message.answer('Выбери Знак зодиака для расклада:', reply_markup=zodiac_signs)

@router.message(Zodiac.zodiac)
async def show_tip_day(message: Message, state:FSMContext):
    zodiac = message.text
    text = await get_zodiac_tip_day(zodiac, message)
    if text:
        await message.answer(f'Совет дня для Знака зодиака {zodiac}\n'
                             f'{text}', reply_markup=generator_buttons(['Назад'], ['menu'], 1))
        await state.clear()


@router.callback_query(F.data == 'menu')
async def menu(query: CallbackQuery, state:FSMContext):
    await state.clear()
    await query.message.edit_text('Выбери расклад:', reply_markup=generator_buttons(['🔮 Совет дня 🔮', '🔮 Расклад на любовь и отношения 🔮', '🔮 Расклад на работу и финансы 🔮', '🔮 Расклад "Да или Нет" 🔮'],['tip_day', 'layout_love', 'layout_money', 'layout_yes_or_not'], 1))

@router.callback_query(F.data == 'layout_love')
async def layout_love(query: CallbackQuery):
    text = parse_layout(tarot_cards_with_values, layout_love=True)
    await query.message.answer(f'Совет карт в любви и отношениях.\n{text}', reply_markup=generator_buttons(['Назад'], ['menu'], 1))

@router.callback_query(F.data == 'layout_money')
async def layout_money(query: CallbackQuery):
    text = parse_layout(tarot_cards_with_values, layout_money=True)
    await query.message.answer(f'Совет карт в работе и финансах.\n{text}', reply_markup=generator_buttons(['Назад'], ['menu'], 1))


@router.callback_query(F.data == 'layout_yes_or_not')
async def layout_money(query: CallbackQuery, state: FSMContext):
    await state.set_state(YesOrNot.question)
    await query.message.answer(f'Задайте свой вопрос:')


@router.message(YesOrNot.question)
async def layout_money(message: Message, state: FSMContext):
    await state.clear()
    text = parse_layout(tarot_cards_with_values, layout_yes_or_not=True)
    await message.answer(f'Совет карт на вопрос Да или Нет.\n{text}', reply_markup=generator_buttons(['Назад'], ['menu'], 1))