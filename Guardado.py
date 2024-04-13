import requests
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

client = MongoClient('localhost', 27017)
db = client['PokemonApi']
collection = db['Pokemons']
base_url = 'https://pokeapi.co/api/v2'

def GuardarDatos():
    url = f'{base_url}/pokemon'
    Contador = 0
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemons = data['results']
            for pokemon in pokemons:
                pokemon_data = requests.get(pokemon['url']).json()
                collection.insert_one(pokemon_data)
                Contador += 1
                print(f'Se ha guardado el pokemon {pokemon_data["name"]} en la BDD')
            url = data['next']
        else:
            print('Error al obtener la lista de pokemons')
            break
    print(f'Se han guardado un total de {Contador} pokemons')

GuardarDatos()