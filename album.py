import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from bottle import HTTPError


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    '''
    Класс описывает таблицу album в БД
    '''

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    '''
    Создает соединение с БД, если его нет, и возвращает объект сессии
    '''
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    '''
    Ищет все альбомы переданного исполнителя
    '''
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_doubles(album, artist):
    '''
    Проверяет есть ли уже такой альбом у исполнителя
    '''
    session = connect_db()
    albums = session.query(Album).filter(Album.album == album).all()
    doubles = [el for el in albums if el.artist == artist]
    return doubles

def check_year(year):
    '''
    Проверяет корректность введенного года альбома
    '''
    try:
        datetime.strptime(year, '%Y-%m-%d')
    except ValueError:
        message = "Неверный формат даты, должен быть YYYY-MM-DD"
        return HTTPError(400, message)
    else:
        return True

def save_album(user_data):
    '''
    Сохраняет новый альбом в БД
    '''
    album = Album(
        year = user_data["year"],
        artist = user_data["artist"],
        genre = user_data["genre"],
        album = user_data["album"]
    )
    session = connect_db()
    session.add(album)
    session.commit()
