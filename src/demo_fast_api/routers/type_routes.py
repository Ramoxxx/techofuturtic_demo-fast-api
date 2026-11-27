from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fast_api.domain.db import get_session
from demo_fast_api.domain.type import Type
from demo_fast_api.dto.responses import TypeResponse

router = APIRouter(prefix='/type', tags=['Type'])

@router.get('', response_model=list[TypeResponse])
def get_all(session: Annotated[Session, Depends(get_session)]): 
    stmt = select(Type)   
    result = session.scalars(stmt).all()
    return result

@router.get('/{id}')
def get_by_id(id: Annotated[int, Path()]):
    pass

@router.post('')
def create():
    pass

@router.put('/{id}')
def update(id: Annotated[int, Path()]):    
    pass

@router.get('/{id}')
def delete(id: Annotated[int, Path()]):
    pass