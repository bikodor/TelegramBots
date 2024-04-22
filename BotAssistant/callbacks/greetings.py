from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker
from data.db import engine, User
from keyboards import reply


router = Router()


# ru
@router.callback_query(F.data == 'ru_start')
async def greetings_russian(query: CallbackQuery):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_user = User(id=query.from_user.id, name=query.from_user.first_name, language='ru')
    session.add(new_user)
    session.commit()
    session.close()
    await query.message.answer(
        f"Привет, {query.from_user.first_name}, меня зовут {query.message.from_user.first_name} и я являюсь ассистентом Бучукури Тамаза! Примеры его работ вы можете посмотреть в меню, если оно у вас не отображается введите /menu",
        reply_markup=reply.ru_main_kb
    )

#en
@router.callback_query(F.data == 'en_start')
async def greetings_english(query: CallbackQuery):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_user = User(id=query.from_user.id, name=query.from_user.first_name, language='en')
    session.add(new_user)
    session.commit()
    session.close()
    await query.message.answer(
        f"Hello, {query.from_user.first_name}, my name is {query.message.from_user.first_name} and I am Buchukuri Tamaz's assistant! You can see examples of his work in the menu, if it is not displayed for you, enter /menu",
        reply_markup=reply.en_main_kb
)