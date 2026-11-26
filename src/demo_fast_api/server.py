import asyncio
import math
from tkinter.filedialog import Open
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.params import Body
import uvicorn

from demo_fast_api.dto.request import EquationRequest, ContactRequest
from demo_fast_api.dto.responses import EquationResponse, PokemonResponse
from demo_fast_api.infrastructure.mailer import Mailer

from demo_fast_api.models.pokemon import Pokemon
from demo_fast_api.services import OpenAIService, PokemonService

app = FastAPI()
# app.include_router(default_routes)
# app = FastAPI(root_path="/api")

@app.get("/pokemon/{pokemon_id}", response_model=PokemonResponse)
async def get_pokemon_full_info(pokemon_id: int, 
                                pokemon_service: Annotated[PokemonService, Depends(PokemonService)],
                                openai_service: Annotated[OpenAIService, Depends(OpenAIService)]):    
    result = {}    
    pokemon = await pokemon_service.get_pokemon(pokemon_id)    
    result["id"] = pokemon_id
    result["name"] = pokemon.name
    result["height"] = pokemon.height / 10
    result["weight"] = pokemon.weight / 10

    description = await openai_service.get_pokemons_description([pokemon.name])
    print(description)

    result["description"] = ""
    return result

@app.post('/pokemons')
async def get_full_pokemons(
    numeros: Annotated[list[int], Body()],
    pokemon_service: Annotated[PokemonService, Depends(PokemonService)],
    open_ai_service: Annotated[OpenAIService, Depends(OpenAIService)],
):
    try:
        pokemons: list[Pokemon] = await asyncio.gather(*[
            pokemon_service.get_pokemon(numero)
            for numero in numeros
        ])
        desc = await open_ai_service.get_pokemons_description([
            p.name for p in pokemons
        ])
        return [{
            'numero': p.id,
            'nom': p.name,
            'poids': p.weight / 10,
            'taille': p.height / 10,
            'description': d
        } for p, d in zip(pokemons, desc)]
        
    except ValueError as ex:
        print(str(ex))
        raise HTTPException(status_code=404)

def main():
    uvicorn.run(
        'demo_fast_api.server:app',
        port=8080,
        reload=True
    )