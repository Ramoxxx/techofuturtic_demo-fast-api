import json
import os
import httpx
from types import CoroutineType

from dotenv import load_dotenv
from demo_fast_api.models.pokemon import Pokemon

load_dotenv()

class PokemonService:
    async def get_pokemon(self, id: int):
        url = f"https://pokeapi.co/api/v2/pokemon/{id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            pokemon = Pokemon.model_validate_json(response.text)
            return pokemon

class OpenAIService:
    BASE_URL = 'https://api.openai.com/v1'
    PRE_POMPT = [
        { 'role': 'developer', 'content': 'User va te donner une liste de pokemons tu devras lui renvoyer la liste des descriptions de chaque pokemon dans le même ordre' }
    ]
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv('OPEN_AI_KEY')}'
    }
    JSON_SCHEMA = {
        'type': 'object',
        'required': ['descriptions'],
        'properties': { 'descriptions':
            { 'type': 'array', 'items': { 'type': 'string' } }
        }
    }
    async def get_pokemons_description(self, names: list[str]) -> CoroutineType[list[str]]:
            async with httpx.AsyncClient() as client:
                response = await client.post(f'{self.BASE_URL}/chat/completions', headers=self.HEADERS, json={
                    'model': 'gpt-4o-mini',
                    'messages': [
                        *self.PRE_POMPT,
                        { 'role': 'user', 'content': ','.join(names) }
                    ],
                    'response_format': {
                        'type': 'json_schema',
                        'json_schema': {
                            'name': 'descriptions',
                            'schema': self.JSON_SCHEMA
                        }
                    } 
                }, timeout=300)
                return json.loads(
                    response.json().get('choices')[0].get('message').get('content')
                ).get('descriptions')


