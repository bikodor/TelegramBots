import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.db import find_user, check_bonus, set_bet, change_money, check_bet
from keyboards.inline import generator_buttons
from utils.states import SetBet_Casino

router = Router()

def get_row(result_dice: int):
    slot_values = {
        1: ('Бар', 'Бар', 'Бар'),
        2: ('Виноград', 'Бар', 'Бар'),
        3: ('Лимон', 'Бар', 'Бар'),
        4: ('Семёрка', 'Бар', 'Бар'),
        5: ('Бар', 'Виноград', 'Бар'),
        6: ('Виноград', 'Виноград', 'Бар'),
        7: ('Лимон', 'Виноград', 'Бар'),
        8: ('Семёрка', 'Виноград', 'Бар'),
        9: ('Бар', 'Лимон', 'Бар'),
        10: ('Виноград', 'Лимон', 'Бар'),
        11: ('Лимон', 'Лимон', 'Бар'),
        12: ('Семёрка', 'Лимон', 'Бар'),
        13: ('Бар', 'Семёрка', 'Бар'),
        14: ('Виноград', 'Семёрка', 'Бар'),
        15: ('Лимон', 'Семёрка', 'Бар'),
        16: ('Семёрка', 'Семёрка', 'Бар'),
        17: ('Бар', 'Бар', 'Виноград'),
        18: ('Виноград', 'Бар', 'Виноград'),
        19: ('Лимон', 'Бар', 'Виноград'),
        20: ('Семёрка', 'Бар', 'Виноград'),
        21: ('Бар', 'Виноград', 'Виноград'),
        22: ('Виноград', 'Виноград', 'Виноград'),
        23: ('Лимон', 'Виноград', 'Виноград'),
        24: ('Семёрка', 'Виноград', 'Виноград'),
        25: ('Бар', 'Лимон', 'Виноград'),
        26: ('Виноград', 'Лимон', 'Виноград'),
        27: ('Лимон', 'Лимон', 'Виноград'),
        28: ('Семёрка', 'Лимон', 'Виноград'),
        29: ('Бар', 'Семёрка', 'Виноград'),
        30: ('Виноград', 'Семёрка', 'Виноград'),
        31: ('Лимон', 'Семёрка', 'Виноград'),
        32: ('Семёрка', 'Семёрка', 'Виноград'),
        33: ('Бар', 'Бар', 'Лимон'),
        34: ('Виноград', 'Бар', 'Лимон'),
        35: ('Лимон', 'Бар', 'Лимон'),
        36: ('Семёрка', 'Бар', 'Лимон'),
        37: ('Бар', 'Виноград', 'Лимон'),
        38: ('Виноград', 'Виноград', 'Лимон'),
        39: ('Лимон', 'Виноград', 'Лимон'),
        40: ('Семёрка', 'Виноград', 'Лимон'),
        41: ('Бар', 'Лимон', 'Лимон'),
        42: ('Виноград', 'Лимон', 'Лимон'),
        43: ('Лимон', 'Лимон', 'Лимон'),
        44: ('Семёрка', 'Лимон', 'Лимон'),
        45: ('Бар', 'Семёрка', 'Лимон'),
        46: ('Виноград', 'Семёрка', 'Лимон'),
        47: ('Лимон', 'Семёрка', 'Лимон'),
        48: ('Семёрка', 'Семёрка', 'Лимон'),
        49: ('Бар', 'Бар', 'Семёрка'),
        50: ('Виноград', 'Бар', 'Семёрка'),
        51: ('Лимон', 'Бар', 'Семёрка'),
        52: ('Семёрка', 'Бар', 'Семёрка'),
        53: ('Бар', 'Виноград', 'Семёрка'),
        54: ('Виноград', 'Виноград', 'Семёрка'),
        55: ('Лимон', 'Виноград', 'Семёрка'),
        56: ('Семёрка', 'Виноград', 'Семёрка'),
        57: ('Бар', 'Лимон', 'Семёрка'),
        58: ('Виноград', 'Лимон', 'Семёрка'),
        59: ('Лимон', 'Лимон', 'Семёрка'),
        60: ('Семёрка', 'Лимон', 'Семёрка'),
        61: ('Бар', 'Семёрка', 'Семёрка'),
        62: ('Виноград', 'Семёрка', 'Семёрка'),
        63: ('Лимон', 'Семёрка', 'Семёрка'),
        64: ('Семёрка', 'Семёрка', 'Семёрка')
    }
    return ', '.join(slot_values.get(result_dice)).capitalize()

def get_point(result_dice: int):
    if result_dice in (1, 22, 43):
        return 4
    elif result_dice in (6, 11, 16, 17, 27, 32, 33, 38, 48, 49, 54, 59):
        return 2
    elif result_dice == 64:
        return 10
    else:
        return -1

def get_result_text(result_dice: int, message):
    result = get_point(result_dice=result_dice)
    combination_text = get_row(result_dice=result_dice)

    if result > 0:
        text_for_gamer = f'Ваша комбинация: \r\n{combination_text}\r\nПоздравляем! Вы выйграли!\n{change_money(message=message, casino=True, win=True, multiplier=result)}'
    else:
        text_for_gamer = f'Ваша комбинация: \r\n{combination_text}\r\nВы проиграли... Попробуйте ещё раз.\n{change_money(message=message, casino=True, win=False)}'
    return text_for_gamer



@router.callback_query(F.data == 'casino')
async def casino_menu(query: CallbackQuery, state: FSMContext):
    await check_bonus(query=query)
    await state.set_state(SetBet_Casino.bet)
    user = find_user(query)
    if check_bet(message=query, casino=True):
        await query.message.edit_text(f'Ваша ставка: {user.bet_casino} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"', reply_markup=generator_buttons(['Начать', 'Назад'], ['casino_start', 'main_menu'], 2))
    else:
        await set_bet(query, bet='0', casino=True)
        await query.message.edit_text('Недостаточно средств для данной ставки или она некорректна, укажите другую')
        await query.message.answer(
            f'Чтобы начать, напишите желаемую ставку'
        )


@router.message(SetBet_Casino.bet)
async def set_bet_casino(message: Message):
    await check_bonus(message=message)
    bet = message.text
    await set_bet(message, bet, casino=True)
    user = find_user(message)
    await message.answer(
            f'Ваша ставка: {user.bet_casino} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"',
            reply_markup=generator_buttons(['Начать', 'Назад'], ['casino_start', 'main_menu'], 2))


@router.callback_query(F.data == 'casino_start')
async def bones_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, roulette=True):
        await state.clear()
        await check_bonus(query=query)
        result_dice = await query.message.answer_dice(emoji='🎰')
        await asyncio.sleep(3)
        text = get_result_text(result_dice=result_dice.dice.value, message=query)
        await query.message.answer(text=text, reply_markup=generator_buttons(['Повторить', 'Назад'], ['casino_start', 'casino'], 2))
    else:
        await query.message.answer('Укажите корректную ставку!', reply_markup=generator_buttons(["Назад"],["casino"], 1))

