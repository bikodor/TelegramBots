from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///assistant.db')
Base = declarative_base(name='Base')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)


Base.metadata.create_all(engine)

def check_russian_user(id_user):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = session.query(User).filter(User.id == id_user).first()
        if user and user.language == 'ru':
            return True
        else:
            return False
    finally:
        session.close()

def switch_lang(id_user):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.id == id_user).first()
        if user and user.language == 'ru':
            user.language = 'en'
            session.commit()
        elif user and user.language == 'en':
            user.language = 'ru'
            session.commit()
    finally:
        session.close()
