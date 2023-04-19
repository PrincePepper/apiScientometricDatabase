from operator import attrgetter
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.deps import BaseGenericResponse
from app.schemas.users import User as schemas_User, UserCreate, UserGet, StatGet, ProfilesGet, ProfileGet, TestUserGet

router = APIRouter()


def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=attrgetter(key), reverse=reverse)
    return xs


@router.post("/get_profiles", response_model=BaseGenericResponse[List[UserGet]])
def get_profiles(
        profiles: ProfilesGet,
        db: Session = Depends(deps.get_db),
):
    '''
    Метод получения списка профилей
    :param filter: обязательный параметр - наукометрическая база данных.
    :param page_size: на одной странице должно присутствовать не более 10 профилей.
    Сортировки: по индексу Хирша (возрастание/убывание) и по дате создания в БД (возрастание/убывание).
    :return:  ФИО автора, индекс Хирша, ссылка на профиль в НБД.
    '''
    start = (profiles.page - 1) * profiles.page_size
    users = crud.crud_user.user.get_multi_users(db, filter=profiles.filter.name, skip=start, limit=profiles.page_size)
    if profiles.sort_hirsch == 'up':
        sort_hirsch = False
    elif profiles.sort_hirsch == 'down':
        sort_hirsch = True

    if profiles.sort_time == 'up':
        sort_time = False
    elif profiles.sort_time == 'down':
        sort_time = True

    return {'data': multisort(list(users), (('h_index', sort_hirsch), ('created_at', sort_time)))}


@router.post("/get_profile", response_model=BaseGenericResponse[TestUserGet], response_model_exclude_none=True)
def get_profile(
        profile: ProfileGet,
        db: Session = Depends(deps.get_db),
):
    '''
    Метод получения профиля сотрудника
    Обязательные параметры - уникальный идентификатор сотрудника, наукометрическая база данных.
    Обязательные поля в ответе: ФИО автора, индекс Хирша, ссылка на профиль в НБД;
    Опциональные поля (можно запросить, передав параметр fields): количество цитирований, количество публикаций.
    '''
    aaa = crud.user.get_profile(db=db, id=profile.guid, database=profile.scientometric_database.name)
    if profile.fields is None:
        aaa.citation_count = None
        aaa.document_count = None
    else:
        if 'documents' not in profile.fields:
            aaa.document_count = None
        if 'citations' not in profile.fields:
            aaa.citation_count = None

    return {'data': aaa}


@router.post("/create", response_model=BaseGenericResponse[schemas_User])
def create_user(
        user_in: UserCreate,
        db: Session = Depends(deps.get_db)
):
    '''
    Метод создания профиля автора:
    :param user_in: Принимает все вышеперечисленные поля: идентификатор сотрудника, ФИО автора, индекс Хирша, количество цитирований, количество публикаций, ссылка на профиль в НБД;
    :return: Возвращает внутренний ID созданного профиля и код результата (ошибка или успех).
    '''
    user_in.created_at = None
    user = crud.user.create(db, obj_in=user_in)
    user.scientometric_database = user.scientometric_database.name
    return {'data': user}


@router.get("/get_stat", response_model=BaseGenericResponse[List[StatGet]])
def get_stat(
        db: Session = Depends(deps.get_db)
):
    '''
    Метод подсчета статистики публикационной активности
    Обязательная группировка: по наукометрической базе данных.
    Ожидаемые поля: общее количество публикаций, цитирований всех авторов, средний индекс Хирша авторов.
    '''
    return {'data': crud.user.get_stat_groupby_scientometric(db=db)}
