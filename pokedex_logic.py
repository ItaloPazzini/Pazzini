# pokedex_logic.py
import requests

def buscar_pokemon(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obter_species_url(pokemon_json):
    return pokemon_json["species"]["url"]

def buscar_cadeia_evolutiva(species_url):
    especie_resposta = requests.get(species_url)
    if especie_resposta.status_code != 200:
        return None
    
    especie_json = especie_resposta.json()
    evolution_chain_url = especie_json["evolution_chain"]["url"]
    
    cadeia_resposta = requests.get(evolution_chain_url)
    if cadeia_resposta.status_code != 200:
        return None
    
    return cadeia_resposta.json()

def extrair_evolucoes(cadeia_json):
    evolucoes = []
    
    def percorrer_cadeia(nodo):
        nome_atual = nodo["species"]["name"]
        evolucoes.append(nome_atual)
        if nodo["evolves_to"]:
            for proximo in nodo["evolves_to"]:
                percorrer_cadeia(proximo)
    
    cadeia = cadeia_json["chain"]
    percorrer_cadeia(cadeia)
    
    return evolucoes
