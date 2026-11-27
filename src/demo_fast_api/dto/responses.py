from dataclasses import dataclass

from pydantic import BaseModel

from demo_fast_api.domain.type import Type


@dataclass
class EquationResponse:
    delta: float
    sol1: float|None
    sol2: float|None

@dataclass
class PokemonResponse:
    id: int
    name: str
    height: float
    weight: float
    description: str


class TypeResponse(BaseModel):
    id: int
    nom: str
    couleur_hex: str

class TypeDetailsResponse(TypeResponse):
    description: str
    nb_especes: int
