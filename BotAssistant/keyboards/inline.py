from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


pr_bot_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти', url='https://t.me/PR_ChannelBot')
        ]
    ]
)

pr_bot_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Go', url='https://t.me/PR_ChannelBot')
        ]
    ]
)

tarot_bot_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти', url='https://t.me/tarot_layout_bot')
        ]
    ]
)

tarot_bot_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Go', url='https://t.me/tarot_layout_bot')
        ]
    ]
)

casino_bot_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти', url='https://t.me/Casino_Joe_Bot')
        ]
    ]
)

casino_bot_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Go', url='https://t.me/Casino_Joe_Bot')
        ]
    ]
)

retry_calc_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Повторить', callback_data='calc')
        ]
    ]
)

retry_calc_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Repeat', callback_data='calc')
        ]
    ]
)

language_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇬🇧 English', callback_data='en_start'),
            InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru_start')
        ]
    ]
)
skills_kb_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вывести последние новости', callback_data='news')
        ],
        [
            InlineKeyboardButton(text='Сменить язык', callback_data='change_lang')
        ],
        [
            InlineKeyboardButton(text='Посчитать выражение', callback_data='calc')
        ],
        [
            InlineKeyboardButton(text='Узнать курс валюты', callback_data='exchange')

        ]
    ],
    sizes=1,
    resize_keyboard=True
)
menu_assistant_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вывести последние новости', callback_data='news')
        ],
        [
            InlineKeyboardButton(text='Сменить язык', callback_data='change_lang')
        ],
        [
            InlineKeyboardButton(text='Посчитать выражение', callback_data='calc')
        ],
        [
            InlineKeyboardButton(text='Узнать курс валюты', callback_data='exchange')

        ],
        [
            InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)

other_button_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Другие функции', callback_data='other')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)
action_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Повторить', callback_data='exchange')
        ],
        [
            InlineKeyboardButton(text='Другие функции', callback_data='other')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)
action_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Repeat', callback_data='exchange')
        ],
        [
            InlineKeyboardButton(text='Other functions', callback_data='other')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)
other_button_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Other functions', callback_data='other')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)
decision_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='confirm_changing'),
            InlineKeyboardButton(text='Нет', callback_data='other')
        ]
    ],
    sizes=2,
    resize_keyboard=True
)
decision_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Yes', callback_data='confirm_changing'),
            InlineKeyboardButton(text='No', callback_data='other')
        ]
    ],
    sizes=2,
    resize_keyboard=True
)


def href_builder_ru(link):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Перейти к новости', url=link),
            ]
        ],
        resize_keyboard=True
    )


def href_builder_en(link):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Go to news', url=link),
            ]
        ],
        resize_keyboard=True
    )





menu_assistant_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Display the latest news', callback_data='news')
        ],
        [
            InlineKeyboardButton(text='Change language', callback_data='change_lang')
        ],
        [
            InlineKeyboardButton(text='Calculate expression', callback_data='calc'),
        ],
        [
            InlineKeyboardButton(text='Find out the exchange rate', callback_data='exchange'),

        ],
        [
            InlineKeyboardButton(text='Return to main menu', callback_data='menu')
        ]
    ],
    sizes=1,
    resize_keyboard=True
)
skills_kb_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Display the latest news', callback_data='news')
        ],
        [
            InlineKeyboardButton(text='Change language', callback_data='change_lang')
        ],
        [
            InlineKeyboardButton(text='Calculate expression', callback_data='calc'),
        ],
        [
            InlineKeyboardButton(text='Find out the exchange rate', callback_data='exchange'),

        ]
    ],
    sizes=1,
    resize_keyboard=True
)
