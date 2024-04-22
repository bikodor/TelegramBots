from data.calculator import calculate_expression
from data.course_request import request_rate_ru
from data.db import check_russian_user, switch_lang
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from utils.states import Exchange, CalcExpression
from keyboards import reply
from keyboards import inline
from keyboards.inline import href_builder_ru, href_builder_en
from aiogram.fsm.context import FSMContext
from data.main_news import get_main_news_ru, get_main_news_en


router = Router()



@router.callback_query(F.data == 'exchange')
async def exchange(query: CallbackQuery, state: FSMContext):
    await state.set_state(Exchange.valute_exchange)
    if check_russian_user(query.from_user.id):
        await query.message.answer( #edit text не работает с state
            "Укажите валюту, курс которой вы хотите узнать",
            reply_markup=reply.rate_kb)
    else:
        await query.message.answer(
            'Indicate the currency whose rate you want to know',
            reply_markup=reply.rate_kb
        )

@router.message(Exchange.valute_exchange)
async def exchange_to(message: Message, state: FSMContext):
    await state.update_data(valute_exchange=message.text)
    await state.set_state(Exchange.valute_count)
    if check_russian_user(message.from_user.id):
        await message.answer('Теперь укажите валюту, в которой вы хотите увидеть курс', reply_markup=reply.rate_kb)
    else:
        await message.answer('Now indicate the currency in which you want to see the rate', reply_markup=reply.rate_kb)


@router.message(Exchange.valute_count)
async def show_rate(message: Message, state: FSMContext):
    await state.update_data(valute_count=message.text)
    data = await state.get_data()
    await state.clear()
    await request_rate_ru(data, message)
    if check_russian_user(message.from_user.id):
        await message.answer('Выберите действие', reply_markup=inline.action_ru)
    else:
        await message.answer('Choose an action', reply_markup=inline.action_en)


@router.callback_query(F.data == 'calc')
async def calculate_message(query: CallbackQuery, state: FSMContext):
    await state.set_state(CalcExpression.result)
    if check_russian_user(query.from_user.id):
        await query.message.answer('Напишите математическое выражение, например: 25+62-75*(2**2/2)+(125^3), где \n'
                                   'x**n - это x возвести в n степень \n'
                                   'x^n - это сделать корень x в n степени (например 125^3 это кубический корень из 125):', reply_markup=reply.rmk)

    else:
        await query.message.answer('Write a mathematical expression, for example, 25+62-75*(2**2/2)+(125^3), where \n'
                                   'x**n is x raised to the n power \n'
                                   'x^n is the root of x raised to the n power (for example 125^3 is the cube root of 125):', reply_markup=reply.rmk)

@router.message(CalcExpression.result)
async def show_result(message: Message, state: FSMContext):
    result = calculate_expression(message.text)
    if check_russian_user(message.from_user.id):
        if result:
            await message.answer(f'Результат: {result}', reply_markup=inline.other_button_ru)
        else:
            await message.answer('Некорректное выражение, попробуйте снова, используя символы из примера', reply_markup=inline.retry_calc_ru)
    else:
        if result:
            await message.answer(f'Result: {result}', reply_markup=inline.other_button_en)
        else:
            await message.answer('Invalid expression, try again using the symbols from the example', reply_markup=inline.retry_calc_en)
    await state.update_data(message.text)
    await state.clear()

@router.callback_query(F.data == 'other')
async def menu_assistant(query: CallbackQuery, state:FSMContext):
    await state.clear()
    if check_russian_user(query.from_user.id):
        await query.message.edit_text('Вот все мои функции:', reply_markup=inline.menu_assistant_ru)
    else:
        await query.message.edit_text('Here are all my functions:', reply_markup=inline.menu_assistant_en)


@router.callback_query(F.data == 'menu')
async def main_menu(query: CallbackQuery):
    if check_russian_user(query.from_user.id):
        await query.message.answer('Вы вернулись в главное меню', reply_markup=reply.ru_main_kb)
    else:
        await query.message.answer('You are back to the main menu', reply_markup=reply.en_main_kb)


@router.callback_query(F.data == 'news')
async def calculate_message(query: CallbackQuery):
    if check_russian_user(query.from_user.id):
        response = get_main_news_ru()
        news_papers = ['Лента: ', 'Медуза: ', 'РИА Новости: ', 'BBC Russia: ']
        i = 0
        for post in response:
            await query.message.answer(f'🔥{news_papers[i]}{post["title"]}🔥', reply_markup=href_builder_ru(post['link']))
            i += 1
    else:
        response = get_main_news_en()
        news_papers = ['Breaking News: ', 'NBC News: ', 'World BBC News: ', 'Fox News: ']
        i = 0
        for post in response:
            await query.message.answer(f'🔥{news_papers[i]}{post["title"]}🔥', reply_markup=href_builder_en(post['link']))
            i += 1

@router.callback_query(F.data == 'change_lang')
async def change_language(query: CallbackQuery):
    if check_russian_user(query.from_user.id):
        await query.message.edit_text('Вы уверены что хотите сменить язык?', reply_markup=inline.decision_ru)
    else:
        await query.message.edit_text('Are you sure you want to change the language?', reply_markup=inline.decision_en)

@router.callback_query(F.data == 'confirm_changing')
async def confirm_changing(query: CallbackQuery):
    switch_lang(query.from_user.id)
    if check_russian_user(query.from_user.id):
        await query.message.edit_text('Вы успешно сменили язык', reply_markup=inline.menu_assistant_ru)
        await query.message.answer('Главное меню было изменено', reply_markup=reply.ru_main_kb)
    else:
        await query.message.edit_text('You have successfully changed the language', reply_markup=inline.menu_assistant_en)
        await query.message.answer('Main menu has changed', reply_markup=reply.en_main_kb)

