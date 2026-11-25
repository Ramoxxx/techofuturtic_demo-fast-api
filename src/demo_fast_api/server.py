import math
from typing import Annotated
from fastapi import FastAPI, Query
import uvicorn

from demo_fast_api.dto.queries import EquationQuery
from demo_fast_api.dto.responses import EquationResponse


app = FastAPI()

@app.get('/api/hello', response_model=str)
def say_hello(name: Annotated[str, Query()] = 'World'):
    return f"hello {name} !!"

@app.get('/api/fibo', response_model=int)
def fibo(n: Annotated[int, Query(ge=0)]):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return f"fibonacci number at {n} is {a}"

@app.get("/api/equation", response_model=EquationResponse)
def equation(dto: Annotated[EquationQuery, Query()]):

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


def main():
    uvicorn.run('demo_fast_api.server:app', port=8080, reload=True)