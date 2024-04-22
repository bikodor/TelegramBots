from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.db import find_user, streak_count, check_bonus, edit_username, switch_updated_username
from keyboards.inline import generator_buttons
from utils.states import UsernameEdit

router = Router()

@router.callback_query(F.data == 'show_streak_bonus')
async def show_streak(query: CallbackQuery):
    await check_bonus(query=query)
    user = find_user(query)
    await query.message.edit_text(f'Ваш ежедневный бонус: {streak_count[user.streak]} 💸 \n\n'
                                  f'Если каждый день заходить в игру, то бонус увеличивается! \n'
                                  f'Первый день: {streak_count[0]} 💸 \n'
                                  f'Второй день: {streak_count[1]} 💸 \n'
                                  f'Третий день: {streak_count[2]} 💸 \n'
                                  f'Четвёртый день: {streak_count[3]} 💸 \n'
                                  f'Пятый день: {streak_count[4]} 💸 \n'
                                  f'Шестой день: {streak_count[5]} 💸 \n'
                                  f'Седьмой день: {streak_count[6]} 💸'
                                  )

@router.callback_query(F.data == 'show_streak')
async def show_streak(query: CallbackQuery):
    await check_bonus(query=query)
    user = find_user(query)
    await query.message.edit_text(f'Ваш ежедневный бонус: {streak_count[user.streak]} 💸 \n\n'
                                  f'Если каждый день заходить в игру, то бонус увеличивается!\n'
                                  f'Первый день: {streak_count[0]} 💸 \n'
                                  f'Второй день: {streak_count[1]} 💸 \n'
                                  f'Третий день: {streak_count[2]} 💸 \n'
                                  f'Четвёртый день: {streak_count[3]} 💸 \n'
                                  f'Пятый день: {streak_count[4]} 💸 \n'
                                  f'Шестой день: {streak_count[5]} 💸 \n'
                                  f'Седьмой день: {streak_count[6]} 💸 ', reply_markup=generator_buttons(['Вернуться назад'], ['profile'], 1)
                                  )

@router.callback_query(F.data == 'profile')
async def show_profile(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await check_bonus(query=query)
    user = find_user(query)
    await query.message.edit_text(f'👤 Ваш профиль 👤 \n'
                               f'Псевдоним: {user.username} \n'
                               f'Баланс: {user.money} 💸 \n', reply_markup=generator_buttons(['Изменить псевдоним', 'Ежедневный бонус', 'Главное меню'], ['edit_profile', 'show_streak', 'main_menu'], 1))

@router.callback_query(F.data == 'edit_profile')
async def edit_profile(query: CallbackQuery, state: FSMContext):
    await check_bonus(query=query)
    await state.set_state(UsernameEdit.username)
    user = find_user(query)
    await query.message.edit_text(f'Ваш псевдоним сейчас: {user.username}, введите новый или вернитесь назад', reply_markup=generator_buttons(['Вернуться назад'], ['profile'], 1))

@router.message(UsernameEdit.username)
async def confirm_edit(message: Message, state: FSMContext):
    await check_bonus(message=message)
    new_username = message.text
    update = await edit_username(new_username, message)
    user = find_user(message)
    if update:
        switch_updated_username(False, user)
        await state.clear()
        await message.answer(f'Псевдоним успешно изменен, {user.username}', reply_markup=generator_buttons(['Назад'], ['profile'], 1))

@router.callback_query(F.data == 'main_menu')
async def main_menu(query: CallbackQuery, state:FSMContext):
    await state.clear()
    await check_bonus(query=query)
    await query.message.edit_text('Вы вернулись в главное меню', reply_markup=generator_buttons(['♠️ Блэкджек ♠️', '🎰 Игровые автоматы 🎰', '🔴 Рулетка ⚫️', '🎲 Кости 🎲', '👤 Профиль 👤'], ['blackjack', 'casino', 'roulette', 'bones', 'profile'], 1))
