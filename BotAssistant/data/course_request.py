import requests
import xml.etree.ElementTree as ET

from data.db import check_russian_user
from keyboards import reply


async def request_rate_ru(data, message):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    response.raise_for_status()
    root = ET.fromstring(response.content)
    currency_info = {}
    for currency_code in ['USD', 'EUR']:
        for valute in root.findall('Valute'):
            if valute.find('CharCode').text == currency_code:
                currency_info[currency_code] = valute.find('Value').text

    usd_str = currency_info["USD"].replace(',', '.')
    eur_str = currency_info["EUR"].replace(',', '.')
    if data['valute_exchange'] == '🇪🇺 EUR':
        if data['valute_count'] == '🇪🇺 EUR':
            await message.answer(f'1 EUR = 1 EUR', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇺🇸 USD':
            await message.answer(f'1 EUR = {round(float(eur_str) / float(usd_str), 4)} USD', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇷🇺 RUB':
            await message.answer(f'1 EUR = {eur_str} RUB', reply_markup=reply.rmk)

    elif data['valute_exchange'] == '🇺🇸 USD':
        if data['valute_count'] == '🇪🇺 EUR':
            await message.answer(f'1 USD = {round(float(usd_str) / float(eur_str), 4)} EUR', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇺🇸 USD':
            await message.answer(f'1 USD = 1 USD', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇷🇺 RUB':
            await message.answer(f'1 USD = {usd_str} RUB', reply_markup=reply.rmk)

    elif data['valute_exchange'] == '🇷🇺 RUB':

        if data['valute_count'] == '🇪🇺 EUR':
            await message.answer(f'1 RUB = {round((1 / float(eur_str)), 4)} EUR', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇺🇸 USD':
            await message.answer(f'1 RUB = {round((1 / float(usd_str)), 4)} USD', reply_markup=reply.rmk)

        elif data['valute_count'] == '🇷🇺 RUB':
            await message.answer(f'1 RUB = 1 RUB', reply_markup=reply.rmk)

    else:
        if check_russian_user(message.from_user.id):
            await message.answer('Что-то пошло не так, попробуйте снова', reply_markup=reply.rmk)
        else:
            await message.answer('Something went wrong, try again', reply_markup=reply.rmk)


