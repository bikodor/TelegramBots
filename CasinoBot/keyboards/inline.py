from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



def generator_buttons(button_texts, callback_datas, row_width):

    buttons = [InlineKeyboardButton(text=text, callback_data=data)
               for text, data in zip(button_texts, callback_datas)]

    button_rows = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]

    keyboard = InlineKeyboardMarkup(inline_keyboard=button_rows)

    return keyboard



def generator_roulette_buttons(button_texts, row_width):

    buttons = [KeyboardButton(text=text)
               for text in button_texts]

    button_rows = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]
    plus_buttons = [KeyboardButton(text='1st'),
                    KeyboardButton(text='2nd'),
                    KeyboardButton(text='3rd')]
    last_buttons = [KeyboardButton(text='1-18'),
                    KeyboardButton(text='Even'),
                    KeyboardButton(text='🔴'),
                    KeyboardButton(text='⚫️'),
                    KeyboardButton(text='Odd'),
                    KeyboardButton(text='19-36'),
                    ]
    zero_button = [KeyboardButton(text='0🟢')]
    button_rows.append(plus_buttons)
    button_rows.append(last_buttons)
    button_rows.append(zero_button)
    keyboard = ReplyKeyboardMarkup(keyboard=button_rows)

    return keyboard

rmk = ReplyKeyboardRemove()