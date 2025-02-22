#!/usr/bin/env python3
import os
import requests
import json
from app.nutrient_analysis import get_nutrient_data  # Asegurar que existe
import app.recipe_optimizer

# Ajusta tu API Key y rutas a tu gusto
USDA_API_KEY = "VoUZcYnQ04PKmQU6x34ZlvJaMmgb4ad7dQCwMK38"
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
HEADERS = {"Content-Type": "application/json"}

# Directorio donde guardaremos los ingredientes originales (ej. la receta del cliente)
INGREDIENTS_DIR = "data/ingredients_data/Greensy"
# Directorio donde guardaremos los posibles sustitutos
SUBSTITUTES_DIR = "data/sustitutos"
# Extensión JSON
JSON_EXTENSION = ".json"

def fetch_nutrient_data(ingredient_name):
    """ Obtiene datos de nutrientes de la API de USDA. """
    try:
        resp = requests.get(
            BASE_URL,
            params={
                "api_key": USDA_API_KEY,
                "query": ingredient_name,
                "pageSize": 3
            },
            headers=HEADERS
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error al obtener datos para {ingredient_name}: {e}")
        return None

def store_substitute_data(ingredient_name, data, index=0):
    """ Guarda datos de sustitutos en JSON. """
    safe_name = ingredient_name.lower().replace(" ", "_")
    file_name = f"{safe_name}_sub{index}{JSON_EXTENSION}"
    file_path = os.path.join(SUBSTITUTES_DIR, file_name)
    
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Guardado sustituto de {ingredient_name} en {file_name}")
    except OSError as err:
        print(f"No se pudo guardar {file_name}: {err}")

def process_substitutes_for(ingredient_name):
    """ Busca sustitutos en la API USDA y los almacena. """
    query_for_substitutes = f"{ingredient_name} substitute"
    data = fetch_nutrient_data(query_for_substitutes)
    if not data or "foods" not in data:
        print(f"Advertencia: no se obtuvieron sustitutos para {ingredient_name}")
        return
    
    foods = data["foods"]
    if not foods:
        print(f"Advertencia: no hay 'foods' en la respuesta para {ingredient_name}")
        return
    
    for i, food_item in enumerate(foods[:3]):
        store_substitute_data(ingredient_name, food_item, i)

def find_best_replacement(ingredient_list, config=None):
    """ Encuentra el mejor sustituto basado en datos de USDA. """
    potential_replacements = []
    
    for ingredient in ingredient_list:
        nutrient_data = get_nutrient_data(ingredient, config)
        if nutrient_data:
            score = app.recipe_optimizer.compare_ingredients(nutrient_data)
            potential_replacements.append((ingredient, score))
    
    if not potential_replacements:
        return None

    potential_replacements.sort(key=lambda x: x[1], reverse=True)
    return potential_replacements[0][0]

def main():
    """ Carga los ingredientes y busca sustitutos. """
    os.makedirs(INGREDIENTS_DIR, exist_ok=True)
    os.makedirs(SUBSTITUTES_DIR, exist_ok=True)
    
    for fname in os.listdir(INGREDIENTS_DIR):
        if not fname.endswith(JSON_EXTENSION):
            continue
        
        full_path = os.path.join(INGREDIENTS_DIR, fname)
        try:
            with open(full_path, "r") as f:
                original_data = json.load(f)
        except (json.JSONDecodeError, OSError) as err:
            print(f"Error leyendo {fname}: {err}")
            continue
        
        ingredient_name = original_data.get("description") or \
                          original_data.get("name") or \
                          original_data.get("food_name", fname.replace(JSON_EXTENSION, ""))

        if not ingredient_name:
            print(f"No se encontró un nombre de ingrediente en {fname}")
            continue
        
        print(f"Buscando sustitutos para: {ingredient_name}")
        process_substitutes_for(ingredient_name)

if __name__ == "__main__":
    main()
