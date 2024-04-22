from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



def generator_buttons(button_texts, callback_datas, row_width):

    buttons = [InlineKeyboardButton(text=text, callback_data=data)
               for text, data in zip(button_texts, callback_datas)]

    button_rows = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]

    keyboard = InlineKeyboardMarkup(inline_keyboard=button_rows)

    return keyboard

zodiac_signs = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='♈ Овен ♈'),
            KeyboardButton(text='♉ Телец ♉')
        ],
        [
            KeyboardButton(text='♊ Близнецы ♊'),
            KeyboardButton(text='♋ Рак ♋')
        ],
[
            KeyboardButton(text='♌ Лев ♌'),
            KeyboardButton(text='♍ Дева ♍')
        ],
[
            KeyboardButton(text='♎ Весы ♎'),
            KeyboardButton(text='♏ Скорпион ♏')
        ],
[
            KeyboardButton(text='♐ Стрелец ♐'),
            KeyboardButton(text='♑ Козерог ♑')
        ],
[
            KeyboardButton(text='♒ Водолей ♒'),
            KeyboardButton(text='♓ Рыбы ♓')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите знак зодиака'
)


rmk = ReplyKeyboardRemove()