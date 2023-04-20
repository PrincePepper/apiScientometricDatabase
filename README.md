# Структура проекта:

```
apiScientometricDatabase
├── app
│   ├── api
│   │   └── routers
│   │   │   ├── user.py
│   │   ├── api.py # подключение всех роутеров к проекту
│   │   └── deps.py # хранит в себе зависимости для всех роутеров
│   ├── core
│   │   └── config.py # env vars и другие
│   └── crud
│   │   ├── __init__.py
│   │   ├── base.py # базовый crud класс от которого всё наследуется
│   │   └── crud_user.py # хранит в себе дописанные crud функции помимо базовых
│   └── db
│   │   ├── base.py # подключение всех моделей, для видемости alembic
│   │   ├── base_class.py # базовые настройки моделей для базы данных и alembic
│   │   └── sessions.py # подключение к базе данных
│   └── models
│   │   ├── __init__.py
│   │   └── users.py
│   └── schemas
│   │   ├── __init__.py
│   │   └── users.py
│   ├── main.py
│   └── manage.py # для запуска и дебаг режима через ide
├── migrations/ # папка alimbic
├── .env
├── .gitignore
├── alembic.ini
├── dataset.xlsx  # тестовая база данных
├── docker-compose.yaml
├── dockerfile
├── document_class.py  # предподготовочный файл чтобы из dataset.xlsx добавить в БД
└── requirements  # необходимые библиотеки
```

# Чтобы развернуть проект нужно сделать первоначальные шаги:

#### 1) создать виртуальное окружение:

`python -m venv venv`  
Чтобы начать пользоваться виртуальным окружением, необходимо его активировать:

```
venv\Scripts\activate.bat
 - для Windows;
source venv/bin/activate
 - для Linux и MacOS.
```

#### 2) установить зависимости: ``pip install -r requirements.txt``

#### 3) запустить две волшебные команды Docker:

```docker
docker build -t backend-task .  
docker compose --env-file .env up -d   
```

#### 4) запустить миграции БД, чтобы добавилась таблица User:

```
alembic revision --autogenerate -m 'initial'
alembic upgrade head  
```

#### 5) запустить `document_class.py`

#### 6) зайти на http://0.0.0.0:8000/api/docs и пользоваться

# Структура БД:

id # общее id строки  
guid # id сотрудника  
full_name # ФИО сотрудника  
scientometric_database # тип наукометрической база данных(scopus,wos,risc)  
document_count # кол-во публикаций  
citation_count # кол-во цитирований  
h_index # индекс Хирша  
url # ссылка на профиль  
created_at # время создание(добавление) в БД юзера

# Методы API

### Предисловие

Все запросы возвращают одну структуру ответа:

```
{
  "status": 200, # статус ответа
  "message": "ok", # пишет что не так если ошибка
  "data": [] # хранит в себе структуру Pydantic возвращаемых данных, требуемые от ручки(и один элемент, так и список хранить может)
}
```

1) get_profiles
   принимает в Body:
    ```
    {
          "filter": "scopus", #отвечает за тип наукометрической базы данных
          "page": 1, # номер страницы
          "page_size": 10, # размер страницы(не больше 10)
          "sort_hirsch": "up", # состояние up или down, сортировка по индексу Хирша
          "sort_time": "up" # состояние up или down, сортировка по времени(второстепенный фактор)
        }
    ```
   ответ:
    ```json
       {
      "status": 200,
      "message": "ok",
      "data": [
        {
          "full_name": "Ыы Ыы Ыы",
          "h_index": 0,
          "url": "https://github.com/FEFU-Analytics-Sector/backend-task"
        },
        {
          "full_name": "Иванов Василий Андреевич",
          "h_index": 14,
          "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"
        },
        {
          "full_name": "Иванов Михаил Владимирович ",
          "h_index": 24,
          "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"
        },
        {
          "full_name": "Петров Олег Федорович",
          "h_index": 43,
          "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"
        },
        {
          "full_name": "Иванов Юрий Борисович",
          "h_index": 115,
          "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"
        },
        {
          "full_name": "Петров Владимир Алексеевич",
          "h_index": 117,
          "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"
        }
      ]
    }
   ```
2) get_profile
   принимает в Body:
    ```
    {
      "guid": "3fa85f64-5717-4562-b3fc-2c963f66afa6", #guid сотрудника
      "scientometric_database": "scopus", # какую смотрим бд
      "fields": [ # Опциональное поле, хранит список доп данных а именно documents(document_count) и citations(citation_count)
        "documents","citations"
      ]
    }
    ```
   ответ:
    ```json
    {
      "status": 200,
      "message": "ok",
      "data": {
        "full_name": "Ыы Ыы Ыы",
        "h_index": 0,
        "url": "https://github.com/FEFU-Analytics-Sector/backend-task"
      }
    }
   ```
3) create
   принимает в Body:
    ```
    {
      "guid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "full_name": "ыы ыы ыы", # должно содержать три слова как ФИО
      "scientometric_database": "scopus", 
      "document_count": 0,
      "citation_count": 0,
      "h_index": 0,
      "url": "https://github.com/FEFU-Analytics-Sector/backend-task"
    }
    ```
   P.S. присутсвует валидация всех полей
   ответ:
    ```json
    {
      "status": 200,
      "message": "ok",
      "data": {
        "guid": "3fa85f64-5717-4562-b3fc-2c963f66afa5",
        "full_name": "Ыы Вы Ыы",
        "scientometric_database": "scopus",
        "document_count": 0,
        "citation_count": 0,
        "h_index": 0,
        "url": "https://github.com/FEFU-Analytics-Sector/backend-task",
        "created_at": 1681956678,
        "id": "96ea5b87-e943-4864-8807-cb0f187c8099"
      }
    }
   ```
4) get_stat
   не принимает ничего на вход
   ответ:
    ```json
    {
      "status": 200,
      "message": "ok",
      "data": [
        {
          "scientometric_database": "risc",
          "documents_sum": 10225,
          "citations_sum": 66691,
          "average_h_index": 54.2
        },
        {
          "scientometric_database": "wos",
          "documents_sum": 1854,
          "citations_sum": 61315,
          "average_h_index": 34.4
        },
        {
          "scientometric_database": "scopus",
          "documents_sum": 3368,
          "citations_sum": 177083,
          "average_h_index": 44.714285714285715
        }
      ]
    }
   ```
