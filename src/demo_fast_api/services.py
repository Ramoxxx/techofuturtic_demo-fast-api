import httpx


class PokemonService:
    async def get_pokemon(self, id: int):
        url = f"https://pokeapi.co/api/v2/pokemon/{id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

class OpenAIService:
    async def get_description(name: str):
        pass


