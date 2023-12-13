from typing import List, Optional

import httpx
from fastapi import FastAPI
from pydantic import BaseModel  
import asyncio  

app = FastAPI()

async def fetch_pokemon_data(pokemon_id: int) -> dict:
    pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(pokeapi_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data from the PokeAPI. Status code: {response.status_code}"}

class Pokemon(BaseModel):
    name: str
    image: str
    types: List[str]

@app.get("/api/v1/pokemons", response_model=List[Pokemon])
async def get_pokemons():
    pokemon_data_list = await asyncio.gather(*[fetch_pokemon_data(pokemon_id) for pokemon_id in range(1, 11)])

    pokemons = []
    for data in pokemon_data_list:
        pokemon = {
            "name": data["name"],
            "image": data["sprites"]["front_default"],
            "types": [type_data["type"]["name"] for type_data in data["types"]],
        }
        pokemons.append(pokemon)

    return pokemons
