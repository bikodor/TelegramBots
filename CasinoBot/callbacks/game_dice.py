import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.db import find_user, check_bonus, set_bet, change_money, check_bet
from keyboards.inline import generator_buttons
from utils.states import SetBet_Bones

router = Router()



@router.callback_query(F.data == 'bones')
async def bones_menu(query: CallbackQuery, state: FSMContext):
    await check_bonus(query=query)
    await state.set_state(SetBet_Bones.bet)
    user = find_user(query)
    if check_bet(message=query, bones=True):
        await query.message.edit_text(
            f'Ваша ставка: {user.bet_bones} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"',
            reply_markup=generator_buttons(['Начать', 'Назад'], ['bones_start', 'main_menu'], 2))
    else:
        await set_bet(query, bet='0', bones=True)
        await query.message.edit_text('Недостаточно средств для данной ставки или она некорректна, укажите другую')
        await query.message.answer(
            f'Чтобы начать, напишите желаемую ставку'
        )

@router.message(SetBet_Bones.bet)
async def set_bet_bones(message: Message):
    await check_bonus(message=message)
    bet = message.text
    await set_bet(message, bet, bones=True)
    user = find_user(message)
    await message.answer(f'Ваша ставка: {user.bet_bones} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"', reply_markup=generator_buttons(['Начать', 'Назад'], ['bones_start', 'main_menu'], 2))


@router.callback_query(F.data == 'bones_start')
async def bones_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, bones=True):
        await check_bonus(query=query)
        await query.message.answer('Ваш ход:')
        result_user = await query.message.answer_dice(emoji='🎲')
        await asyncio.sleep(4)
        await query.message.answer('Мой ход:')
        result_bot = await query.message.answer_dice(emoji='🎲')
        await asyncio.sleep(4)
        if result_bot.dice.value > result_user.dice.value:
            result = change_money(query, bones=True, win=False)
            await query.message.answer(f'Я выйграл! \n'
                                       f'{result}', reply_markup=generator_buttons(["Повторить", "Назад"],["bones_start", "bones"], 2))
        elif result_bot.dice.value < result_user.dice.value:
            result = change_money(query, bones=True, win=True)
            await query.message.answer(f'Поздравляю! Вы победили!\n'
                                       f'{result}', reply_markup=generator_buttons(["Повторить", "Назад"],["bones_start", "bones"], 2))
        else:
            user = find_user(query)
            await query.message.answer(f'Ничья!'
                                       f'У вас {user.money} 💰', reply_markup=generator_buttons(["Повторить", "Назад"],["bones_start", "bones"], 2))
    else:
        await query.message.answer('Укажите корректную ставку!', reply_markup=generator_buttons(["Назад"],["bones"], 1))



