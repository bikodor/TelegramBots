import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.db import find_user, check_bonus, set_bet, change_money, check_bet, find_lobby, start_lobby, count_card, add_lobby, get_card, delete_lobby
from keyboards.inline import generator_buttons
from utils.states import SetBet_Blackjack

router = Router()





@router.callback_query(F.data == 'blackjack')
async def blackjack_menu(query: CallbackQuery, state: FSMContext):
    await check_bonus(query=query)
    await state.set_state(SetBet_Blackjack.bet)
    user = find_user(query)
    if check_bet(message=query, blackjack=True):
        await query.message.edit_text(
            f'Ваша ставка: {user.bet_blackjack} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"\nБаланс: {user.money}💰',
            reply_markup=generator_buttons(['Начать', 'Назад'], ['blackjack_start', 'main_menu'], 2))
    else:
        await set_bet(query, bet='0', blackjack=True)
        await query.message.edit_text('Недостаточно средств для данной ставки или она некорректна, укажите другую')
        await query.message.answer(
            f'Чтобы начать, напишите желаемую ставку'
        )



@router.message(SetBet_Blackjack.bet)
async def set_bet_blackjack(message: Message):
    await check_bonus(message=message)
    bet = message.text
    await set_bet(message, bet, blackjack=True)
    user = find_user(message)
    await message.answer(
            f'Ваша ставка: {user.bet_blackjack} 💸\nЧтобы начать, напишите желаемую ставку или нажмите "Начать"\nБаланс: {user.money}💰',
            reply_markup=generator_buttons(['Начать', 'Назад'], ['blackjack_start', 'main_menu'], 2))


@router.callback_query(F.data == 'blackjack_start')
async def blackjack_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, roulette=True):
        lobby = find_lobby(query)
        if lobby:
            await check_bonus(query=query)
            await query.message.edit_text('У вас незавершенная игра!\nПродолжить или начать новую?', reply_markup=generator_buttons(['Продолжить', 'Начать новую'], ['continue', 'start_new'], 2))


        else:
            await check_bonus(query=query)
            add_lobby(query)
            hand_user, hand_dealer = start_lobby(query)
            amount_user = count_card(hand_user)
            amount_dealer = count_card(hand_dealer)
            if amount_user == 21:
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ход дилера ...')
                await asyncio.sleep(1)
                card = get_card(query, dealer=True)
                hand_dealer += f', {card}'
                amount_dealer = count_card(hand_dealer)
                if amount_dealer == 21:
                    delete_lobby(query)
                    msg = change_money(query, blackjack=True, win=True, multiplier=0)
                    await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                                  f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                                  f'Ничья!\n{msg}',
                                                  reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                 ['blackjack_start', 'blackjack'], 2))
                else:
                    delete_lobby(query)
                    msg = change_money(query, blackjack=True, win=True, multiplier=1)
                    await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                                  f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                                  f'Вы победили!\n{msg}',
                                                  reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                 ['blackjack_start',
                                                                                  'blackjack'], 2))

            else:
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ваш ход:',
                                          reply_markup=generator_buttons(['Ещё', 'Хватит'], ['hit', 'stand'], 2))
    else:
        await query.message.answer('Укажите корректную ставку!',
                                   reply_markup=generator_buttons(["Назад"], ["blackjack"], 1))


@router.callback_query(F.data == 'hit')
async def blackjack_hit(query:CallbackQuery):
    await check_bonus(query=query)
    get_card(query, user=True)
    lobby = find_lobby(query)
    hand_user = lobby.hand_user
    hand_dealer = lobby.hand_dealer
    amount_user = count_card(hand_user)
    amount_dealer = count_card(hand_dealer)
    if amount_user > 21:
        msg = change_money(query, blackjack=True, win=False)
        delete_lobby(query)
        await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                      f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                      f'К сожалению, вы проиграли, у вас больше 21...\n{msg}', reply_markup=generator_buttons(['Повторить', 'Назад'], ['blackjack_start', 'blackjack'], 2))

    elif amount_user == 21:
        await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                      f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                      f'Ход дилера ...')
        await asyncio.sleep(1)
        lose = True
        while lose:
            card = get_card(query, dealer=True)
            hand_dealer += f', {card}'
            amount_dealer = count_card(hand_dealer)
            if amount_dealer == 21:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=0)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                      f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                      f'Ничья!\n{msg}', reply_markup=generator_buttons(['Повторить', 'Назад'], ['blackjack_start', 'blackjack'], 2))
            elif amount_dealer > 21:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=1)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Вы победили!\n{msg}', reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                               ['blackjack_start',
                                                                                                'blackjack'], 2))
            else:
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ход дилера ...')
                await asyncio.sleep(1)


    else:
        await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                      f'Ваша рука: \n{hand_user} ({amount_user})'
                                      f'Ваш ход:',
                                      reply_markup=generator_buttons(['Ещё', 'Хватит'], ['hit', 'stand'], 2))


@router.callback_query(F.data == 'stand')
async def blackjack_turn_dealer(query:CallbackQuery):
    await check_bonus(query=query)
    get_card(query, dealer=True)
    lobby = find_lobby(query)
    hand_user = lobby.hand_user
    hand_dealer = lobby.hand_dealer
    amount_user = count_card(hand_user)
    amount_dealer = count_card(hand_dealer)
    await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                  f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                  f'Ход дилера ...')
    await asyncio.sleep(1)
    lose = True
    while lose:

        if amount_dealer < 16:
            card = get_card(query, dealer=True)
            hand_dealer += f', {card}'
            amount_dealer = count_card(hand_dealer)
            if amount_dealer > 21:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=1)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer}  ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Вы победили!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start',
                                                                              'blackjack'], 2))


            else:
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer}  ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ход дилера ...')
                await asyncio.sleep(1)


        elif amount_dealer in (16,17):
            if amount_dealer > amount_user:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=False, multiplier=1)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'К сожалению, вы проиграли, у дилера больше очков...\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start', 'blackjack'], 2))
            elif amount_dealer < amount_user:
                card = get_card(query, dealer=True)
                hand_dealer += f', {card}'
                amount_dealer = count_card(hand_dealer)
                if amount_dealer > 21:
                    delete_lobby(query)
                    msg = change_money(query, blackjack=True, win=True, multiplier=1)
                    lose = False
                    await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                                  f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                                  f'Вы победили!\n{msg}',
                                                  reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                 ['blackjack_start',
                                                                                  'blackjack'], 2))
                elif amount_dealer > amount_user:
                    delete_lobby(query)
                    msg = change_money(query, blackjack=True, win=False, multiplier=1)
                    lose = False
                    await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                                  f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                                  f'К сожалению, вы проиграли, у дилера больше очков...\n{msg}',
                                                  reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                 ['blackjack_start', 'blackjack'], 2))

            else:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=0)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ничья!\n{msg}', reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                               ['blackjack_start',
                                                                                                'blackjack'], 2))
        else:
            if amount_dealer > amount_user:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=False, multiplier=1)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'К сожалению, вы проиграли, у дилера больше очков...\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start', 'blackjack'], 2))
            elif amount_dealer < amount_user:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=1)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Вы победили!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start',
                                                                              'blackjack'], 2))
            else:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=0)
                lose = False
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ничья!\n{msg}', reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                                               ['blackjack_start',
                                                                                                'blackjack'], 2))


@router.callback_query(F.data == 'continue')
async def blackjack_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, roulette=True):

        await check_bonus(query=query)
        lobby = find_lobby(query)
        hand_user = lobby.hand_user
        hand_dealer = lobby.hand_dealer
        amount_user = count_card(hand_user)
        amount_dealer = count_card(hand_dealer)
        if amount_user == 21:
            await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ход дилера ...')
            await asyncio.sleep(1)
            card = get_card(query, dealer=True)
            hand_dealer += f', {card}'
            amount_dealer = count_card(hand_dealer)
            if amount_dealer == 21:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=0)
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ничья!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start', 'blackjack'], 2))
            else:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=1)
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Вы победили!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start',
                                                                              'blackjack'], 2))

        else:
            await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ваш ход:',
                                          reply_markup=generator_buttons(['Ещё', 'Хватит'], ['hit', 'stand'], 2))
    else:
        await query.message.answer('Укажите корректную ставку!',
                                   reply_markup=generator_buttons(["Назад"], ["blackjack"], 1))

@router.callback_query(F.data == 'start_new')
async def blackjack_start_bet(query:CallbackQuery, state:FSMContext):
    await state.clear()
    if check_bet(message=query, roulette=True):
        delete_lobby(query)
        msg = change_money(query, blackjack=True, win=False)
        await query.message.edit_text(f'{msg}')
        await check_bonus(query=query)
        add_lobby(query)
        hand_user, hand_dealer = start_lobby(query)
        amount_user = count_card(hand_user)
        amount_dealer = count_card(hand_dealer)
        if amount_user == 21:
            await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ход дилера ...')
            await asyncio.sleep(1)
            card = get_card(query, dealer=True)
            hand_dealer += f', {card}'
            amount_dealer = count_card(hand_dealer)
            if amount_dealer == 21:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=0)
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Ничья!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start', 'blackjack'], 2))
            else:
                delete_lobby(query)
                msg = change_money(query, blackjack=True, win=True, multiplier=1)
                await query.message.edit_text(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                              f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                              f'Вы победили!\n{msg}',
                                              reply_markup=generator_buttons(['Повторить', 'Назад'],
                                                                             ['blackjack_start',
                                                                              'blackjack'], 2))

        else:
            await query.message.answer(f'Рука дилера: \n{hand_dealer} ({amount_dealer})\n'
                                          f'Ваша рука: \n{hand_user} ({amount_user})\n'
                                          f'Ваш ход:',
                                          reply_markup=generator_buttons(['Ещё', 'Хватит'], ['hit', 'stand'], 2))
    else:
        await query.message.answer('Укажите корректную ставку!',
                                   reply_markup=generator_buttons(["Назад"], ["blackjack"], 1))