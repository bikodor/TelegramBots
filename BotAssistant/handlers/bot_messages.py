from aiogram import Router, F, Bot
from aiogram.types import Message

from config_reader import config
from keyboards import reply, inline
from data.db import check_russian_user
from aiogram.types.input_file import FSInputFile

router = Router()

@router.message(F.text == '🎰 Casino Bot 🎰')
async def casino_bot(message: Message):
    photo = FSInputFile('images/Casino_bot.png')
    await message.answer_photo(photo)
    if check_russian_user(message.from_user.id):
        await message.answer('🎰 <b>Casino Bot</b> 🎰\n\nБот, в котором можно сыграть в Казино игры, такие как:\n\n1. Рулетка.\n2. Блекджек.\n3. Кости.\n4. Покрутить игровой автомат.\n\nТакже в этом боте реализован функционал профиля, в котором есть Баланс и Псевдоним, который можно менять, но он должен быть уникальным, т.е. такого псевдонима не должно быть у других пользователей, баланс пополняется из ежедневных бонусов, который увеличивается, если каждый день заходить в игру (обновляется в 00:00 по МСК).\nВ дополнение бот запоминает пользователя и будет обращаться к нему не так, как при первом запуске (после указания псевдонима).', reply_markup=inline.casino_bot_ru)
    else:
        await message.answer("🎰 <b>Casino Bot</b> 🎰\n\nA bot with which you can play in Casino games, such as:\n\n1. Roulette.\n2. Blackjack.\n3. Bones.\n4. Spin the slot machine.\n\nThis bot also has a functional profile, which has Balances and an Alias that can be changed, but it must be improved, i.e. Other users should not have such an alias; the balance is replenished from daily bonuses, which increases if you enter the game every day (updated at 00:00 Moscow time).\nIn addition, the bot remembers the user and will contact him differently than when he first started (after specifying the alias).\n\nThis bot will only be in Russian.", reply_markup=inline.casino_bot_en)

@router.message(F.text == '🔮 Tarot Bot 🔮')
async def taro_bot(message: Message):
    photo = FSInputFile('images/Tarot_bot.png')
    await message.answer_photo(photo)
    if check_russian_user(message.from_user.id):
        await message.answer('🔮 <b>Tarot Bot</b> 🔮\n\nБот, в котором можно делать Таро расклады:\n\n1. Совет дня для Знаков зодиака (для каждого Знака зодиака сохраняется расклад на день, обновляется в 00:00 по МСК).\n2. Расклад на отношения и любовь.\n3. Расклад на работу и финансы.\n4. Расклад на вопрос "Да" или "Нет", отличается от других раскладов тем, что пользователь вводит свой вопрос, а затем выдается одна карта, вместо трёх, и даёт ответ: ближе к да или к нет.', reply_markup=inline.tarot_bot_ru)
    else:
        await message.answer('🔮 <b>Tarot Bot</b> 🔮\n\nBot in which you can make Tarot layouts:\n\n1. Tip of the day for Zodiac Signs (for each Zodiac Sign, the layout for the day is saved, updated at 00:00 Moscow time.\n2. Alignment for relationships and love.\n3. Alignment for work and finances.\n4. Alignment for the question “Yes” or “No” ", differs from other layouts in that the user enters his question, and then one card is given, instead of three, and gives the answer: closer to yes or no.\n\nThis bot will only be in Russian.', reply_markup=inline.tarot_bot_en)

@router.message(F.text == '📊 PR Bot 📊')
async def pr_bot(message: Message):
    photo = FSInputFile('images/PR_bot.png')
    await message.answer_photo(photo)
    if check_russian_user(message.from_user.id):
        await message.answer('📊 <b>PR Bot</b> 📊\n\nБот для чата, сам по себе ничего не делает, чтобы его проверить, можете зайти в чат @PR_chat_m и там если что-то напишете, бот удалит ваше сообщение и напишет, чтобы вы подписались на другой телеграмм канал, чтобы писать в этом чате. \n\nТакже если после этого вы подпишетесь на канал и попробуете передать ссылку, которая не ведёт на телеграмм канал или пользователя, например https://youtube.com, то Бот также удалит ваше сообщение и попросит вас не использовать ссылки не на телеграмм, тк они могут быть вредоносными.', reply_markup=inline.pr_bot_ru)
    else:
        await message.answer('📊 <b>PR Bot</b> 📊\n\nThe bot for chat does not do anything by itself, to check it, you can go to the chat @PR_chat_m and there if you write something, the bot will delete your message and write, so that you subscribe to another telegram channel in order to write in this chat. \n\nAlso, if after that you subscribe to the channel and try to send a link that does not lead to a telegram channel or user, for example https://youtube.com, then the Bot will also will delete your message and ask you not to use non-Telegram links, as they may be malicious.\n\nThis bot will only be in Russian.', reply_markup=inline.pr_bot_en)

@router.message(F.text.lower() == 'а что ты умеешь делать?')
async def functional_ru(message: Message):
    await message.answer('В целом, функционал у меня ограничен, но я умею: \n'
                         '1. Вывести последние новости за сегодня. \n'
                         '2. Cменить текущий язык. \n'
                         '3. Посчитать ввёденное вами выражение. \n'
                         '4. Узнать курс валюты.', reply_markup=inline.skills_kb_ru)

@router.message(F.text.lower() == 'обратная связь')
async def feedback_ru(message: Message):
    await message.answer('Для сотрудничества и предложений: @Tamazio', reply_markup=reply.ru_main_kb)






@router.message(F.text.lower() == 'what can you do?')
async def functional_en(message: Message):
    await message.answer('In general, my functionality is limited, but I can:\n'
                         '1. Display the latest news for today. \n'
                         '2. Change the current language. \n'
                         '3. Calculate the expression you entered. \n'
                         '4. Find out the exchange rate.', reply_markup=inline.skills_kb_en)

@router.message(F.text.lower() == 'feedback')
async def feedback_en(message: Message):
    await message.answer("For cooperation and suggestions: @Tamazio", reply_markup=reply.en_main_kb)




