import math
from typing import Annotated

from fastapi import APIRouter, FastAPI, Query

from demo_fast_api.dto.request import EquationRequest
from demo_fast_api.dto.responses import EquationResponse

router = APIRouter(tags=['Math'])

@router.get('/fibo', response_model=int)
def fibo(n: Annotated[int, Query(ge=0)]):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return f"fibonacci number at {n} is {a}"

@router.get("/equation", response_model=EquationResponse)
def equation(dto: Annotated[EquationRequest, Query()]):

    result = {}
    
    delta =  dto.b**2 - 4 * dto.a * dto.c
    result['delta'] = delta

    if delta >= 0:
        result['sol1'] = (-dto.b - math.sqrt(delta)) / (2 * dto.a)
        result['sol2'] = (-dto.b + math.sqrt(delta)) / (2 * dto.a)
    else:
        result['sol1'] = None
        result['sol2'] = None

    return result