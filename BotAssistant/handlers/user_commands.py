from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker
from data.db import check_russian_user
from data.db import engine, User
from keyboards import inline, reply
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == message.from_user.id).first()
    session.close()
    if user:
        if user.language == 'ru':
            await message.answer(f'И снова здравствуйте, {message.from_user.first_name}, чем я могу вам помочь?', reply_markup=reply.ru_main_kb)
        else:
            await message.answer(f'Hello again, {message.from_user.first_name}, how can I help you?', reply_markup=reply.en_main_kb)
    else:
        await message.answer('Please select a language', reply_markup=inline.language_kb)


@router.message(Command('menu'))
async def menu(message: Message):
    if check_russian_user(message.from_user.id):
        await message.answer('Клавиатура должна отобразиться снизу', reply_markup=reply.ru_main_kb)
    else:
        await message.answer('The keyboard should appear at the bottom', reply_markup=reply.en_main_kb)


