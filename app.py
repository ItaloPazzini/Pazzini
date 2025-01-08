# app.py
from flask import Flask, render_template, request, jsonify
from pokedex_logic import (
    buscar_pokemon,
    obter_species_url,
    buscar_cadeia_evolutiva,
    extrair_evolucoes
)

app = Flask(__name__)

@app.route("/")
def index():
    """
    Rota que renderiza a página inicial (templates/index.html).
    """
    return render_template("index.html")

@app.route("/api/pokemon", methods=["GET"])
def api_pokemon():
    """
    Rota que recebe ?nomePokemon=xxx e retorna (em JSON) 
    as informações do Pokémon e sua cadeia evolutiva.
    """
    nome = request.args.get("nomePokemon", "").strip()
    if not nome:
        return jsonify({"error": "Nenhum nome de Pokémon foi fornecido."}), 400
    
    pokemon_data = buscar_pokemon(nome)
    if not pokemon_data:
        return jsonify({"error": f"Pokémon '{nome}' não encontrado."}), 404
    
    # Extrair informações relevantes
    nome_pokemon = pokemon_data["name"]
    pokemon_id = pokemon_data["id"]
    tipos = [t["type"]["name"] for t in pokemon_data["types"]]
    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}
    habilidades = [ab["ability"]["name"] for ab in pokemon_data["abilities"]]
    imagem = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
    
    # Cadeia evolutiva
    species_url = obter_species_url(pokemon_data)
    cadeia_json = buscar_cadeia_evolutiva(species_url)
    
    evolucoes = []
    if cadeia_json:
        evolucoes = extrair_evolucoes(cadeia_json)
    
    return jsonify({
        "nome": nome_pokemon,
        "id": pokemon_id,
        "tipos": tipos,
        "stats": stats,
        "habilidades": habilidades,
        "imagem": imagem,
        "cadeia_evolutiva": evolucoes
    })


if __name__ == "__main__":
    # Rodar servidor Flask
    app.run(debug=True)
