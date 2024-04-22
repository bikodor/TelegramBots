import re

from sqlalchemy import create_engine, Column, String, Date, Integer
from datetime import date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from parse_taro import get_layout_three_cards, tarot_cards_with_values, parse_layout

engine = create_engine('sqlite:///tip_day.db')
Base = declarative_base(name='Base')

class TipDay(Base):
    __tablename__ = 'tip_day'
    id = Column(Integer, primary_key=True)
    zodiac = Column(String)
    text = Column(String)
    update_date = Column(Date)


Base.metadata.create_all(engine)

def clean_string(s):
    return re.sub(r'\W+', '', s)

async def get_zodiac_tip_day(zodiac, message):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        text = clean_string(zodiac)
        zodiac_sign = session.query(TipDay).filter(TipDay.search_field == text).first()
        if zodiac_sign:
            if zodiac_sign.update_date == date.today():
                return zodiac_sign.text
            else:
                txt = parse_layout(tarot_cards_with_values, tip_day=True)
                zodiac_sign.text = txt
                zodiac_sign.update_date = date.today()
                session.commit()
                return zodiac_sign.text
        else:
            raise ValueError
    except:
        await message.answer('Был указан некорректный знак зодиака, пожалуйста, укажите его из клавиатуры')

    finally:
        session.close()


