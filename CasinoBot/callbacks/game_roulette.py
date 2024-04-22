import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.db import find_user, check_bonus, set_bet, change_money, check_bet
from keyboards.inline import generator_buttons, generator_roulette_buttons, rmk
from utils.states import SetBet_Roulette, Roulette_Action
import random

router = Router()

fields = [
    '1🔴', '2⚫️', '3🔴', '4⚫️', '5🔴', '6⚫️', '7🔴', '8⚫️', '9🔴', '10⚫️', '11⚫️', '12🔴', '13⚫️', '14🔴', '15⚫️', '16🔴', '17⚫️', '18🔴', '19🔴', '20⚫️', '21🔴', '22⚫️', '23🔴', '24⚫️', '25🔴', '26⚫️', '27🔴', '28⚫️', '29⚫️', '30🔴', '31⚫️', '32🔴', '33⚫️', '34🔴', '35⚫️', '36🔴'
          ]
fields_roulette = [
    '0🟢','1🔴', '2⚫️', '3🔴', '4⚫️', '5🔴', '6⚫️', '7🔴', '8⚫️', '9🔴', '10⚫️', '11⚫️', '12🔴', '13⚫️', '14🔴', '15⚫️', '16🔴', '17⚫️', '18🔴', '19🔴', '20⚫️', '21🔴', '22⚫️', '23🔴', '24⚫️', '25🔴', '26⚫️', '27🔴', '28⚫️', '29⚫️', '30🔴', '31⚫️', '32🔴', '33⚫️', '34🔴', '35⚫️', '36🔴'
]
fields_1st = [1, 2, 3, 4, 13, 14, 15, 16, 25, 26, 27, 28]
fields_2nd = [5, 6, 7, 8, 17, 18, 19, 20, 29, 30, 31, 32]
fields_3rd = [9, 10, 11, 12, 21, 22, 23, 24, 33, 34, 35, 36]

red_fields = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_fields = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

def get_multiplier(action):
    result = random.randint(0,36)
    if action == '1st':
        if result in fields_1st:
            return result, 2
        else:
            return result, -1
    elif action == '2nd':
        if result in fields_2nd:
            return result, 2
        else:
            return result, -1
    elif action == '3rd':
        if result in fields_3rd:
            return result, 2
        else:
            return result, -1
    elif action == '1-18':
        if 1 <= result <= 18:
            return result, 1
        else:
            return result, -1
    elif action == '19-36':
        if 19 <= result <= 36:
            return result, 1
        else:
            return result, -1
    elif action[0:1].isdigit():
        if action in fields_roulette:
            num = int(action[0:1])
            if num > 36:
                return result, False
            elif num == result:
                return result, 35
            else:
                return result, -1
        else:
            return result, False
    elif action[0].isdigit():
        if action in fields_roulette:
            num = int(action[0])
            if result == 0:
                if num == result:
                    return result, 50
            elif num == result:
                return result, 35
            else:
                return result, -1
        else:
            return result, False

    elif action == 'Even':
        if result == 0:
            return result, -1
        elif result % 2 == 0:
            return result, 1
        else:
            return result, -1
    elif action == '🔴':
        if result in red_fields:
            return result, 1
        else:
            return result, -1

    elif action == '⚫️':
        if result in black_fields:
            return result, 1
        else:
            return result, -1
    elif action == 'Odd':
        if result == 0:
            return result, -1
        elif result % 2 != 0:
            return result, 1
        else:
            return result, -1
    else:
        return result, False





@router.callback_query(F.data == 'roulette')
async def casino_menu(query: CallbackQuery, state: FSMContext):
    await check_bonus(query=query)
    await state.set_state(SetBet_Roulette.bet)
    user = find_user(query)
    if check_bet(message=query, roulette=True):
        await query.message.edit_text(f'Ваша ставка: {user.bet_roulette} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"\nБаланс: {user.money}💰', reply_markup=generator_buttons(['Начать', 'Назад'], ['roulette_start', 'main_menu'], 2))
    else:
        await set_bet(query, bet='0', roulette=True)
        await query.message.edit_text('Недостаточно средств для данной ставки или она некорректна, укажите другую')
        await query.message.answer(
            f'Чтобы начать, напишите желаемую ставку'
        )



@router.message(SetBet_Roulette.bet)
async def set_bet_roulette(message: Message):
    await check_bonus(message=message)
    bet = message.text
    await set_bet(message, bet, roulette=True)
    user = find_user(message)
    await message.answer(
            f'Ваша ставка: {user.bet_roulette} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"',
            reply_markup=generator_buttons(['Начать', 'Назад'], ['roulette_start', 'main_menu'], 2))



@router.callback_query(F.data == 'roulette_start')
async def roulette_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, roulette=True):
        await check_bonus(query=query)
        user = find_user(message=query)
        await state.set_state(Roulette_Action.action)
        await query.message.answer(f'{user.username}, Ваша ставка: {user.bet_roulette} 💸\nУкажите поле, на которое хотите поставить (если вы на телефоне рекомендую повернуть экран горизонтально)\nБаланс: {user.money}💰',
                                   reply_markup=generator_roulette_buttons(fields, 12))
        await query.message.answer('Или вернитесь назад', reply_markup=generator_buttons(['Назад'], ['roulette'], 1))
    else:
        await query.message.answer('Укажите корректную ставку!',
                                   reply_markup=generator_buttons(["Назад"], ["roulette"], 1))


@router.message(Roulette_Action.action)
async def set_bet_roulette(message: Message, state:FSMContext):
    await check_bonus(message=message)
    action = message.text
    result, multiplier = get_multiplier(action)
    if multiplier:
        await state.clear()
        await message.answer(f"Результат: {fields_roulette[result]}", reply_markup=rmk)

        if multiplier == -1:
            res = change_money(message, roulette=True, win=False, multiplier=multiplier)
            await message.answer('К сожалению, вы проиграли... \n'+res, reply_markup=generator_buttons(['Повторить', 'Назад'], ['roulette_start', 'roulette'], 2))
        else:
            res = change_money(message, roulette=True, win=True, multiplier=multiplier)
            await message.answer('Поздравляю, вы выиграли🔥🔥🔥 \n'+res, reply_markup=generator_buttons(['Повторить', 'Назад'], ['roulette_start', 'roulette'], 2))
    else:
        await message.answer('Укажите значение из клавиатуры!')
