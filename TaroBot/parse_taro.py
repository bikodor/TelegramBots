import random

from bs4 import BeautifulSoup
import requests


tarot_cards_with_values = [
    ("Дурак", '/znachenie_kart_taro_na_sovet/durak'),
    ("Маг", '/znachenie_kart_taro_na_sovet/mag'),
    ("Верховная жрица", '/znachenie_kart_taro_na_sovet/jrica'),
    ("Императрица", '/znachenie_kart_taro_na_sovet/imperatrica'),
    ("Император", '/znachenie_kart_taro_na_sovet/imperator'),
    ("Иерофант", '/znachenie_kart_taro_na_sovet/jrec'),
    ("Влюбленные", '/znachenie_kart_taro_na_sovet/vlublennie'),
    ("Колесница", '/znachenie_kart_taro_na_sovet/kolesnica'),
    ("Сила", '/znachenie_kart_taro_na_sovet/sila'),
    ("Отшельник", '/znachenie_kart_taro_na_sovet/otshelnik'),
    ("Колесо Фортуны", '/znachenie_kart_taro_na_sovet/koleso_fortuni'),
    ("Справедливость", '/znachenie_kart_taro_na_sovet/pravosudie'),
    ("Повешенный", '/znachenie_kart_taro_na_sovet/poveshenniy'),
    ("Смерть", '/znachenie_kart_taro_na_sovet/smert'),
    ("Умеренность", '/znachenie_kart_taro_na_sovet/vozderzhanie'),
    ("Дьявол", '/znachenie_kart_taro_na_sovet/dyavol'),
    ("Башня", '/znachenie_kart_taro_na_sovet/bashnya'),
    ("Звезда", '/znachenie_kart_taro_na_sovet/zvezda'),
    ("Луна", '/znachenie_kart_taro_na_sovet/luna'),
    ("Солнце", '/znachenie_kart_taro_na_sovet/solnce'),
    ("Суд", '/znachenie_kart_taro_na_sovet/sud'),
    ("Мир", '/znachenie_kart_taro_na_sovet/mir'),
    ("Туз Жезлов", '/znachenie_kart_taro_na_sovet/tuz_jezlov'),
    ("Двойка Жезлов", '/znachenie_kart_taro_na_sovet/dvoyka_jezlov'),
    ("Тройка Жезлов", '/znachenie_kart_taro_na_sovet/troyka_jezlov'),
    ("Четверка Жезлов", '/znachenie_kart_taro_na_sovet/chetverka_jezlov'),
    ("Пятерка Жезлов", '/znachenie_kart_taro_na_sovet/pyaterka_jezlov'),
    ("Шестерка Жезлов", '/znachenie_kart_taro_na_sovet/shesterka_jezlov'),
    ("Семерка Жезлов", '/znachenie_kart_taro_na_sovet/semerka_jezlov'),
    ("Восьмерка Жезлов", '/znachenie_kart_taro_na_sovet/vosmerka_jezlov'),
    ("Девятка Жезлов", '/znachenie_kart_taro_na_sovet/devyatka_jezlov'),
    ("Десятка Жезлов", '/znachenie_kart_taro_na_sovet/desyatka_jezlov'),
    ("Паж Жезлов", '/znachenie_kart_taro_na_sovet/paj_jezlov'),
    ("Рыцарь Жезлов", '/znachenie_kart_taro_na_sovet/ricar_jezlov'),
    ("Королева Жезлов", '/znachenie_kart_taro_na_sovet/koroleva_jezlov'),
    ("Король Жезлов", '/znachenie_kart_taro_na_sovet/korol_jezlov'),
    ("Туз Чаш", '/znachenie_kart_taro_na_sovet/tuz_kubkov'),
    ("Двойка Чаш", '/znachenie_kart_taro_na_sovet/dvoyka_kubkov'),
    ("Тройка Чаш", '/znachenie_kart_taro_na_sovet/troyka_kubkov'),
    ("Четверка Чаш", '/znachenie_kart_taro_na_sovet/chetverka_kubkov'),
    ("Пятерка Чаш", '/znachenie_kart_taro_na_sovet/pyaterka_kubkov'),
    ("Шестерка Чаш", '/znachenie_kart_taro_na_sovet/shesterka_kubkov'),
    ("Семерка Чаш", '/znachenie_kart_taro_na_sovet/semerka_kubkov'),
    ("Восьмерка Чаш", '/znachenie_kart_taro_na_sovet/vosmerka_kubkov'),
    ("Девятка Чаш", '/znachenie_kart_taro_na_sovet/devyatka_kubkov'),
    ("Десятка Чаш", '/znachenie_kart_taro_na_sovet/desyatka_kubkov'),
    ("Паж Чаш", '/znachenie_kart_taro_na_sovet/paj_kubkov'),
    ("Рыцарь Чаш", '/znachenie_kart_taro_na_sovet/ricar_kubkov'),
    ("Королева Чаш", '/znachenie_kart_taro_na_sovet/koroleva_kubkov'),
    ("Король Чаш", '/znachenie_kart_taro_na_sovet/korol_kubkov'),
    ("Туз Мечей", '/znachenie_kart_taro_na_sovet/tuz_mechey'),
    ("Двойка Мечей", '/znachenie_kart_taro_na_sovet/dvoyka_mechey'),
    ("Тройка Мечей", '/znachenie_kart_taro_na_sovet/troyka_mechey'),
    ("Четверка Мечей", '/znachenie_kart_taro_na_sovet/chetverka_mechey'),
    ("Пятерка Мечей", '/znachenie_kart_taro_na_sovet/pyaterka_mechey'),
    ("Шестерка Мечей", '/znachenie_kart_taro_na_sovet/shesterka_mechey'),
    ("Семерка Мечей", '/znachenie_kart_taro_na_sovet/semerka_mechey'),
    ("Восьмерка Мечей", '/znachenie_kart_taro_na_sovet/vosmerka_mechey'),
    ("Девятка Мечей", '/znachenie_kart_taro_na_sovet/devyatka_mechey'),
    ("Десятка Мечей", '/znachenie_kart_taro_na_sovet/desyatka_mechey'),
    ("Паж Мечей", '/znachenie_kart_taro_na_sovet/paj_mechey'),
    ("Рыцарь Мечей", '/znachenie_kart_taro_na_sovet/ricar_mechey'),
    ("Королева Мечей", '/znachenie_kart_taro_na_sovet/koroleva_mechey'),
    ("Король Мечей", '/znachenie_kart_taro_na_sovet/korol_mechey'),
    ("Туз Пентаклей", '/znachenie_kart_taro_na_sovet/tuz_pentakley'),
    ("Двойка Пентаклей", '/znachenie_kart_taro_na_sovet/dvoyka_pentakley'),
    ("Тройка Пентаклей", '/znachenie_kart_taro_na_sovet/troyka_pentakley'),
    ("Четверка Пентаклей", '/znachenie_kart_taro_na_sovet/chetverka_pentakley'),
    ("Пятерка Пентаклей", '/znachenie_kart_taro_na_sovet/pyaterka_pentakley'),
    ("Шестерка Пентаклей", '/znachenie_kart_taro_na_sovet/shesterka_pentakley'),
    ("Семерка Пентаклей", '/znachenie_kart_taro_na_sovet/semerka_pentakley'),
    ("Восьмерка Пентаклей", '/znachenie_kart_taro_na_sovet/vosmerka_pentakley'),
    ("Девятка Пентаклей", '/znachenie_kart_taro_na_sovet/devyatka_pentakley'),
    ("Десятка Пентаклей", '/znachenie_kart_taro_na_sovet/desyatka_pentakley'),
    ("Паж Пентаклей", '/znachenie_kart_taro_na_sovet/paj_pentakley'),
    ("Рыцарь Пентаклей", '/znachenie_kart_taro_na_sovet/ricar_pentakley'),
    ("Королева Пентаклей", '/znachenie_kart_taro_na_sovet/koroleva_pentakley'),
    ("Король Пентаклей", '/znachenie_kart_taro_na_sovet/korol_pentakley')
]


def find_tip_day(tag):
    return tag.name == 'h2' and 'Совет дня' in tag.text

def find_layout_money(tag):
    return tag.name == 'h2' and 'в работе и финансах' in tag.text

def find_layout_love(tag):
    return tag.name == 'h2' and 'в любви и отношениях' in tag.text

def find_layout_yes_or_not(tag):
    return tag.name == 'h2' and 'да или нет' in tag.text

url = "https://magya-online.ru/znachenie_kart_taro_na_sovet/korol_pentakley"
response = requests.get(url)
html_content = response.text


def get_layout_three_cards(cards):

    random_index = random.randrange(len(cards))
    card1 = cards.pop(random_index)

    random_index = random.randrange(len(cards))
    card2 = cards.pop(random_index)

    random_index = random.randrange(len(cards))
    card3 = cards.pop(random_index)


    return [card1, card2, card3]






def parse_layout(tarot_cards_with_values, tip_day=False, layout_money=False, layout_love=False, layout_yes_or_not=False):
    main_url = "https://magya-online.ru"
    cards = get_layout_three_cards(tarot_cards_with_values)
    msg = ''
    if tip_day:
        for card in cards:
            url = main_url + card[1]
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            target_h3 = soup.find(find_tip_day)
            next_element = target_h3.find_next_sibling() if target_h3 else None
            text = next_element.get_text() if next_element else 'Что-то пошло не так, обратитесь к администратору @Tamazio'
            msg += f'\n✨ Карта: {card[0]} ✨\n{text}\n'
        return msg
    elif layout_money:
        for card in cards:
            url = main_url + card[1]
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            target_h3 = soup.find(find_layout_money)
            next_element = target_h3.find_next_sibling() if target_h3 else None
            text = next_element.get_text() if next_element else 'Что-то пошло не так, обратитесь к администратору @Tamazio'
            msg += f'\n💸 Карта: {card[0]} 💸\n{text}\n'
        return msg
    elif layout_love:
        for card in cards:
            url = main_url + card[1]
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            target_h3 = soup.find(find_layout_love)
            next_element = target_h3.find_next_sibling() if target_h3 else None
            text = next_element.get_text() if next_element else 'Что-то пошло не так, обратитесь к администратору @Tamazio'
            msg += f'\n❤️ Карта: {card[0]} ❤️\n{text}\n'
        return msg
    elif layout_yes_or_not:
        random_index = random.randrange(len(tarot_cards_with_values))
        card = tarot_cards_with_values.pop(random_index)
        url = main_url + card[1]
        new_url = url.replace('/znachenie_kart_taro_na_sovet/', '/znachenie_kart_taro_na_vopros_da_ili_net/')
        response = requests.get(new_url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        target_h3 = soup.find(find_layout_yes_or_not)
        next_element = target_h3.find_next_sibling() if target_h3 else None
        text = next_element.get_text() if next_element else 'Что-то пошло не так, обратитесь к администратору @Tamazio'
        msg += f'\n🔮 Карта: {card[0]} 🔮\n{text}\n'
        return msg
    else:
        return 'Что-то пошло не так, обратитесь к администратору @Tamazio'