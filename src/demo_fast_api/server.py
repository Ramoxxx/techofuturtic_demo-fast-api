import math
from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.params import Body
import uvicorn

from demo_fast_api.dto.request import EquationRequest, ContactRequest
from demo_fast_api.dto.responses import EquationResponse, PokemonResponse
from demo_fast_api.infrastructure.mailer import Mailer

from demo_fast_api.services import PokemonService

app = FastAPI(root_path="/api")

@app.get('/hello', response_model=str)
def say_hello(name: Annotated[str, Query()] = 'World'):
    return f"hello {name} !!"

@app.get('/fibo', response_model=int)
def fibo(n: Annotated[int, Query(ge=0)]):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return f"fibonacci number at {n} is {a}"

@app.get("/equation", response_model=EquationResponse)
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

@app.post("/contact", response_model=str)
async def contact(dto: Annotated[ContactRequest, Body()], mailer: Annotated[Mailer, Depends(Mailer)]):
    name = dto.name
    email = dto.email
    content = dto.content
    return "mail sending disabled"
    # try:
    #     await mailer.send_email([email], f"{name} sent a message from fast api.", content)
    #     return f"Mail sent to {email}"
    # except Exception as error:
    #     return str(error)
    
@app.get("/pokemon/{pokemon_id}", response_model=PokemonResponse)
async def get_pokemon_full_info(pokemon_id: int, pokemon_service: Annotated[PokemonService, Depends(PokemonService)]):    
    result = {}    
    pokemon_json = await pokemon_service.get_pokemon(pokemon_id)    
    result["id"] = pokemon_id
    result["name"] = pokemon_json["name"]
    result["height"] = float(pokemon_json["height"]) / 10
    result["weight"] = float(pokemon_json["weight"])

    

    result["description"] = ""
    return result


def main():
    uvicorn.run('demo_fast_api.server:app', port=8080, reload=True)