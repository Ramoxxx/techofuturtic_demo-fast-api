from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from psycopg2 import IntegrityError
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from demo_fast_api.domain.db import get_session
from demo_fast_api.domain.espece import Espece
from demo_fast_api.domain.type import Type
from demo_fast_api.dto.request import TypeRequest
from demo_fast_api.dto.responses import TypeDetailsResponse, TypeResponse
from demo_fast_api.services import OpenAIService

router = APIRouter(prefix='/type', tags=['Type'])

@router.get('', response_model=list[TypeResponse])
async def get_all(session: Annotated[Session, Depends(get_session)], openai_service: Annotated[OpenAIService, Depends(OpenAIService)]): 
    stmt = select(Type)   
    result = session.scalars(stmt).all()
    # if result is empty, get data from openai and insert in db
    if not result:
        pokemon_types = await openai_service.get_pokemon_types()
        session.add_all([Type(**t) for t in pokemon_types])
        session.flush()
        result = session.scalars(stmt).all()
    return result

@router.get('/{id}')
def get_by_id(id: Annotated[int, Path()], session: Annotated[Session, Depends(get_session)]):
    """
    si id existe pas renvoyer un code 404
    sinon renvoyer le nom, la couleur, la description, l'id
    et le nombre de pokemon possédant ce type dans la db
    """
    stmt = select(Type).where(Type.id == id)
    type = session.scalars(stmt).one_or_none()
    if not type:
        raise HTTPException(status_code=404, detail=f"(pokemon) Type with id {id} not found")
    else:
        stmt2 = (select(func.count())
        .select_from(Espece)
        .where(or_(Espece.type1_id == id, Espece.type2_id == id)))
        return TypeDetailsResponse(**type.__dict__,nb_especes= session.scalar(stmt2))

@router.post('', status_code=201)
def create(dto: Annotated[TypeRequest, Body()], session: Annotated[Session, Depends(get_session)]):
    """
    Ajouter un type dans la db
    """
    stmt = select(Type).where(Type.nom == dto.nom)
    if session.scalars(stmt).one_or_none():
        raise HTTPException(status_code=409, detail="Un type avec ce nom existe déjà.")
    t = Type(**dto.__dict__)
    session.add(t)
    session.flush()
    return t.id

@router.put('/{id}')
def update(dto: Annotated[TypeRequest, Body()], id: Annotated[int, Path()], session: Annotated[Session, Depends(get_session)]):  
    """
    maj un type dans la db
    """  
    stmt = select(Type).where(Type.nom == dto.nom, Type.id != id)
    type: Type|None = session.scalars(stmt).one_or_none()
    if type:
        raise HTTPException(status_code=409, detail="Le nom du type existe déjà")
    type_to_update = session.scalars(select(Type).where(Type.id == id)).one_or_none()
    if not type_to_update:
        raise HTTPException(status_code=404)
    type_to_update.nom = dto.nom
    type_to_update.couleur_hex = dto.couleur_hex
    type_to_update.description = dto.description
    return type_to_update.id

@router.delete('/{id}')
def delete(id: Annotated[int, Path()], session: Annotated[Session, Depends(get_session)]):
    """
    Supprimer un type de la db.
    Si des espèce sont associées au type, ne pas supprimer et renvoyer un code 400
    """
    stmt = select(Type).where(Type.id == id)
    type_to_delete = session.scalars(stmt).one_or_none()
    if not type:
        raise HTTPException(status_code=404, detail=f"(pokemon) Type with id {id} not found")
    else:
        stmt2 = (select(func.count())
        .select_from(Espece)
        .where(or_(Espece.type1_id == id, Espece.type2_id == id)))
    if session.scalar(stmt2):
        raise HTTPException(status_code=400)
    session.delete(type_to_delete)