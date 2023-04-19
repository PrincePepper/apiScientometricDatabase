import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config
from app.core.config import settings


def connect_sqlalc():
    print('\nПопытка подключения к базе данных...\n')

    database_url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        host=settings.POSTGRES_SERVER_HOST,
        port=settings.POSTGRES_SERVER_PORT,
        user=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        db=settings.POSTGRES_DATABASE
    )
    settings.SQLALCHEMY_DATABASE_URI = database_url
    engine = create_engine(config.settings.SQLALCHEMY_DATABASE_URI)

    def timer(timeout):
        Timer = threading.Timer(timeout, helthcheck)
        Timer.start()

    def helthcheck():
        with engine.begin() as ddd:
            ddd.in_transaction()

    try:
        print(timer(2))
    except:
        print("База данных не существует или неверно введенные данные")
        print("\nПопытка подключения провалено...\n")
    else:
        print("\nК базе данных поключено...\n")
    return engine


engine = connect_sqlalc()
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)
