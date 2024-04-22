from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardRemove

ru_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎰 Casino Bot 🎰'),
            KeyboardButton(text='🔮 Tarot Bot 🔮')
        ],
        [
            KeyboardButton(text='📊 PR Bot 📊'),
            KeyboardButton(text='А что ты умеешь делать?')
        ],
        [
            KeyboardButton(text='Обратная связь')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите бота для вывода подробного описания',
)

en_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎰 Casino Bot 🎰'),
            KeyboardButton(text='🔮 Tarot Bot 🔮')
        ],
        [
            KeyboardButton(text='📊 PR Bot 📊'),
            KeyboardButton(text='What can you do?')
        ],
        [
            KeyboardButton(text='Feedback')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Select a bot to display a detailed description',
)

rate_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🇷🇺 RUB'),
            KeyboardButton(text='🇺🇸 USD'),
            KeyboardButton(text='🇪🇺 EUR')
        ]
    ],
    resize_keyboard=True,
    sizes=3,
    one_time_keyboard=True,
    input_field_placeholder='Укажите валюту:',

)

rmk = ReplyKeyboardRemove()