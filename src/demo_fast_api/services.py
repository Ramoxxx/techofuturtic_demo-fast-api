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
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv('OPEN_AI_KEY')}'
    }    
    async def get_pokemons_description(self, names: list[str]) -> CoroutineType[list[str]]:
        async with httpx.AsyncClient() as client:            
            PRE_POMPT = [
                    { 'role': 'developer', 'content': 'User va te donner une liste de pokemons tu devras lui renvoyer la liste des descriptions de chaque pokemon dans le même ordre' }
                ]
            JSON_SCHEMA = {
                'type': 'object',
                'required': ['descriptions'],
                'properties': { 'descriptions':
                    { 'type': 'array', 'items': { 'type': 'string' } }
                }
            }
            
            response = await client.post(f'{self.BASE_URL}/chat/completions', headers=self.HEADERS, json={
                'model': 'gpt-4o-mini',
                'messages': [
                    *PRE_POMPT,
                    { 'role': 'user', 'content': ','.join(names) }
                ],
                'response_format': {
                    'type': 'json_schema',
                    'json_schema': {
                        'name': 'descriptions',
                        'schema': JSON_SCHEMA
                    }
                } 
            }, timeout=300)
            return json.loads(
                response.json().get('choices')[0].get('message').get('content')
            ).get('descriptions')
            

    async def get_pokemon_types(self) -> CoroutineType[list[dict]]:
        async with httpx.AsyncClient() as client:            
            # PRE_POMPT = [
            #         { 'role': 'developer', 'content': 'Renvoie la liste des types de pokemon que tu peux trouver ici : https://pokeapi.co/api/v2/type/ . Pour chaque item, tu ajoutera une description correspondante' }
            #     ]
            JSON_SCHEMA = {
                "type": "object",
                "properties": {
                    "pokemon_types": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "nom": {
                                    "type": "string"
                                },
                                "couleur_hex": {
                                    "type": ["string", "null"]
                                },
                                "description": {
                                    "type": ["string", "null"]
                                }
                            },
                            "required": ["nom", "couleur_hex", "description"],                            
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["pokemon_types"],
                "additionalProperties": False
            }
            
            response = await client.post(f'{self.BASE_URL}/chat/completions', headers=self.HEADERS, json={
                'model': 'gpt-4o-mini',
                'messages': [
                    {
                        'role': 'developer',
                        'content': (
                            'Return all available Pokémon types from '
                            'https://pokeapi.co/api/v2/type/. '
                            'For each type, provide a corresponding description '
                            'and a representative hexadecimal color without #.'
                        )
                    },
                    {
                        'role': 'user',
                        'content': 'Return the complete list of Pokémon types.'
                    }
                ],
                'response_format': {
                    'type': 'json_schema',
                    'json_schema': {
                        'name': 'pokemon_types',
                        'strict': True,
                        'schema': JSON_SCHEMA
                    }
                } 
            }, 
            timeout=300)

            return json.loads(
                response.json().get('choices')[0].get('message').get('content')
            ).get('pokemon_types')
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            pokemon_types = json.loads(content)
            print(pokemon_types['pokemon_types'])
            

