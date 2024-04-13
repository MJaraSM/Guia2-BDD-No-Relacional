import requests
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

client = MongoClient('localhost', 27017)
db = client['PokemonApi']
collection = db['Pokemons']
base_url = 'https://pokeapi.co/api/v2'

def ObtenerPokemons(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

def GuardarPokemons():
    url = f'{base_url}/pokemon'
    Contador = 0
    pokemons_urls = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemons = data['results']
            pokemons_urls.extend([pokemon['url'] for pokemon in pokemons])
            url = data['next']
        else:
            print('Error al obtener la lista de Pokémon.')
            return
    
    with ThreadPoolExecutor() as executor:
        pokemons_data = executor.map(ObtenerPokemons, pokemons_urls)
        for pokemon_data in pokemons_data:
            collection.insert_one(pokemon_data)
            Contador += 1
            print(f'Se ha guardado el pokemon {pokemon_data["name"]} en la BDD')
    print(f'Se han guardado un total de {Contador} pokemons')

GuardarPokemons()