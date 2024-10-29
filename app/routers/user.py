from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])

SessionDep = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_users(session: SessionDep):
    users = session.scalars(select(User)).all()
    return users

@router.get('/user_id')
async def user_by_id(session: SessionDep, user_id: int):
    user = session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return user
@router.post('/create')
async  def create_user(session: SessionDep, username: str, firstname: str, lastname: str, age: int):
    users_name = session.scalars(select(User.slug)).all()
    if slugify(username) in users_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with that username already exists'
        )
    session.execute(insert(User).values(username=username,
                                      firstname=firstname,
                                      lastname=lastname,
                                      age=age,
                                      slug=slugify(username)))
    session.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'}

@router.put('/update')
async def update_user(session: SessionDep, user_id: int, username: str, firstname: str, lastname: str, age: int):
    user = session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    session.execute(update(User).where(User.id == user_id).values(
            username=username,
            firstname=firstname,
            lastname=lastname,
            age=age,
            slug=slugify(username)))

    session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }

@router.delete('/delete')
async def delete_user(session: SessionDep, user_id: int):
    user = session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    session.execute(delete(User).where(User.id == user_id))
    session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }

