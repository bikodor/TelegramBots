import random

from sqlalchemy import create_engine, Integer, Column, String, Date, Boolean
from datetime import date, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from keyboards.inline import generator_buttons
from data.Errors import BetMoreThanMoney, BetNotNumber
engine = create_engine('sqlite:///casino.db')
Base = declarative_base(name='Base')

deck = ['2♠️', '3♠️', '4♠️', '5♠️', '6♠️', '7♠️', '8♠️', '9♠️', '10♠️', 'J♠️', 'Q♠️', 'K♠️', 'A♠️',
        '2♥️', '3♥️', '4♥️', '5♥️', '6♥️', '7♥️', '8♥️', '9♥️', '10♥️', 'J♥️', 'Q♥️', 'K♥️', 'A♥️',
        '2♣️', '3♣️', '4♣️', '5♣️', '6♣️', '7♣️', '8♣️', '9♣️', '10♣️', 'J♣️', 'Q♣️', 'K♣️', 'A♣️',
        '2♦️', '3♦️', '4♦️', '5♦️', '6♦️', '7♦️', '8♦️', '9♦️', '10♦️', 'J♦️', 'Q♦️', 'K♦️', 'A♦️'
        ]
str_deck = '2♠️, 3♠️, 4♠️, 5♠️, 6♠️, 7♠️, 8♠️, 9♠️, 10♠️, J♠️, Q♠️, K♠️, A♠️, 2♥️, 3♥️, 4♥️, 5♥️, 6♥️, 7♥️, 8♥️, 9♥️, 10♥️, J♥️, Q♥️, K♥️, A♥️, 2♣️, 3♣️, 4♣️, 5♣️, 6♣️, 7♣️, 8♣️, 9♣️, 10♣️, J♣️, Q♣️, K♣️, A♣️, 2♦️, 3♦️, 4♦️, 5♦️, 6♦️, 7♦️, 8♦️, 9♦️, 10♦️, J♦️, Q♦️, K♦️, A♦️'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True, nullable=True)
    updated_username = Column(Boolean)
    status = Column(Integer)
    money = Column(Integer)
    date_registration = Column(Date)
    last_launch = Column(Date)
    streak = Column(Integer)
    start_bonus = Column(Boolean)
    bet_bones = Column(Integer)
    bet_casino = Column(Integer)
    bet_blackjack = Column(Integer)
    bet_roulette = Column(Integer)


class Lobby(Base):
    __tablename__ = 'lobby'
    id = Column(Integer, primary_key=True)
    deck = Column(String)
    hand_dealer = Column(String)
    hand_user = Column(String)
    finished = Column(Boolean)


Base.metadata.create_all(engine)

def add_lobby(message):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_lobby = Lobby(id=message.from_user.id, deck=str_deck, hand_dealer=None, hand_user=None, finished=False)
    session.add(new_lobby)
    session.commit()
    session.close()

def delete_lobby(message):
    Session = sessionmaker(bind=engine)
    session = Session()
    lobby = session.query(Lobby).filter(Lobby.id == message.from_user.id).first()
    session.delete(lobby)
    session.commit()
    session.close()

def start_lobby(message):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        lobby = session.query(Lobby).filter(Lobby.id == message.from_user.id).first()
        cards = lobby.deck
        cards = cards.split(', ')
        card1 = cards.pop(random.randint(0, len(cards) - 1))
        card2 = cards.pop(random.randint(0, len(cards) - 1))
        lobby.hand_user = f'{card1}, {card2}'
        card_dealer = cards.pop(random.randint(0, len(cards) - 1))
        lobby.hand_dealer = f'{card_dealer}'
        lobby.deck = ', '.join(cards)
        session.commit()
        return lobby.hand_user, lobby.hand_dealer
    finally:
        session.close()


def find_lobby(message):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        lobby = session.query(Lobby).filter(Lobby.id == message.from_user.id).first()
        return lobby
    finally:
        session.close()


def get_card(message, dealer=False, user=False):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        lobby = session.query(Lobby).filter(Lobby.id == message.from_user.id).first()
        cards = lobby.deck
        cards = cards.split(', ')
        card = cards.pop(random.randint(0, len(cards) - 1))
        lobby.deck = ', '.join(cards)
        if user:
            lobby.hand_user += f', {card}'
        if dealer:
            lobby.hand_dealer += f', {card}'
        session.commit()
        return card
    finally:
        session.close()


def count_card(hand):
    cards = hand.split(', ')
    amount = 0
    aces = 0


    for card in cards:
        if card[:-2].isdigit():
            amount += int(card[:-2])
        elif card[:-2] in ['J', 'Q', 'K']:
            amount += 10
        elif card[:-2] == 'A':
            aces += 1

    for _ in range(aces):
        if amount + 11 > 21:
            amount += 1
        else:
            amount += 11

    return amount







streak_count = [500, 1000, 1500, 2000, 2500, 3000, 3500]

def find_user(message):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        return user
    finally:
        session.close()

def add_user(message):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_user = User(id=message.from_user.id, name=message.from_user.first_name, username=None, updated_username=False, status=0, money=0, date_registration=date.today(), last_launch=date.today(), streak=0, start_bonus=False, bet_bones=10, bet_casino=10, bet_blackjack=10, bet_roulette=10)
    session.add(new_user)
    session.commit()
    session.close()

def switch_updated_username(value, user):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user.updated_username = value
        session.commit()
        return user.updated_username
    finally:
        session.close()

async def edit_username(name, message):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        if name == user.username:
            await message.answer('Вы указали тот же псевдоним, пожалуста укажите другой или вернитесь в профиль', reply_markup=generator_buttons(['Вернуться в профиль'], ['profile'], 1))
        else:
            user.username = name
            session.commit()
            update = switch_updated_username(True, user)
            return update
    except IntegrityError:
        await message.answer('Такой псевдоним уже существует, пожалуйста, укажите другой')
        session.rollback()
    finally:
        session.close()

def get_username(message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == message.from_user.id).first()
    session.close()
    return user.username

async def check_bonus(message=None, query=None):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        if message is not None:
            user = session.query(User).filter(User.id == message.from_user.id).first()
            if user:
                one_day = timedelta(days=1)
                if user.start_bonus == False:
                    user.start_bonus = True
                    user.money += streak_count[user.streak]
                    session.commit()
                    await message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))

                elif date.today() == user.last_launch + one_day:
                    user.last_launch = date.today()
                    user.streak += 1
                    user.money += streak_count[user.streak]
                    session.commit()
                    await message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))
                elif date.today() != user.last_launch:
                    user.last_launch = date.today()
                    user.streak = 0
                    user.money += streak_count[user.streak]
                    session.commit()
                    await message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))
        elif query is not None:
            user = session.query(User).filter(User.id == query.from_user.id).first()
            if user:
                one_day = timedelta(days=1)
                if user.start_bonus == False:
                    user.start_bonus = True
                    user.money += streak_count[user.streak]
                    session.commit()
                    await query.message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))

                elif date.today() == user.last_launch + one_day:
                    user.last_launch = date.today()
                    user.streak += 1
                    user.money += streak_count[user.streak]
                    session.commit()
                    await query.message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))
                elif date.today() != user.last_launch:
                    user.last_launch = date.today()
                    user.streak = 0
                    user.money += streak_count[user.streak]
                    session.commit()
                    await query.message.answer(f'Вам начислен бонус в размере {streak_count[user.streak]} очков!',
                                         reply_markup=generator_buttons(['Посмотреть'], ['show_streak_bonus'], 1))
        else:
            print('Что-то пошло не так')
    finally:
        session.close()
def check_bet(message, blackjack=False, roulette=False, bones=False, casino=False):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        if blackjack:
            if user.money >= user.bet_blackjack and user.bet_blackjack != 0:
                return True
            else:
                return False
        elif roulette:
            if user.money >= user.bet_roulette and user.bet_roulette != 0:
                return True
            else:
                return False
        elif casino:
            if user.money >= user.bet_casino and user.bet_casino != 0:
                return True
            else:
                return False
        elif bones:
            if user.money >= user.bet_bones and user.bet_bones != 0:
                return True
            else:
                return False

    finally:
        session.close()

async def set_bet(message, bet, blackjack=False, roulette=False, bones=False, casino=False):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        if bet.isdigit():
            bet_num = int(bet)
            if bet_num <= user.money and bet_num != 0:
                if blackjack:
                    user.bet_blackjack = bet_num
                    session.commit()
                elif roulette:
                    user.bet_roulette = bet_num
                    session.commit()
                elif bones:
                    user.bet_bones = bet_num
                    session.commit()
                elif casino:
                    user.bet_casino = bet_num
                    session.commit()
            else:
                raise BetMoreThanMoney
        else:
            raise BetNotNumber
    except ValueError:
        await message.answer('Укажите целое, положительное число!')
    except BetNotNumber:
        await message.answer('Укажите целое, положительное число!')
    except BetMoreThanMoney:
        await message.answer('Указанная ставка больше чем ваш баланс или некорректна!')
    finally:
        session.close()

def change_money(message, blackjack=False, roulette=False, bones=False, casino=False, win=False, multiplier=1):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        if blackjack:
            if win:
                user.money += user.bet_blackjack
                session.commit()
                return f'+{user.bet_blackjack*multiplier} очков 💲\n' \
                       f'Всего: {user.money} 💰'
            else:
                user.money -= user.bet_blackjack
                session.commit()
                return f'-{user.bet_blackjack} очков 🔻\n' \
                       f'Всего: {user.money} 💰'
        elif roulette:
            if win:
                user.money += user.bet_roulette*multiplier
                session.commit()
                return f'+{user.bet_roulette*multiplier} очков 💲\n' \
                       f'Всего: {user.money} 💰'
            else:
                user.money -= user.bet_roulette
                session.commit()
                return f'-{user.bet_roulette} очков 🔻\n' \
                       f'Всего: {user.money} 💰'
        elif bones:
            if win:
                user.money += user.bet_bones
                session.commit()
                return f'+{user.bet_bones} очков 💲\n' \
                       f'Всего: {user.money} 💰'
            else:
                user.money -= user.bet_bones
                session.commit()
                return f'-{user.bet_bones} очков 🔻\n' \
                       f'Всего: {user.money} 💰'
        elif casino:
            if win:
                user.money += user.bet_casino*multiplier
                session.commit()
                return f'+{user.bet_casino*multiplier} очков 💲 \n' \
                       f'Всего: {user.money} 💰'
            else:
                user.money -= user.bet_casino
                session.commit()
                return f'-{user.bet_casino} очков 🔻\n' \
                       f'Всего: {user.money} 💰'
    finally:
        session.close()


