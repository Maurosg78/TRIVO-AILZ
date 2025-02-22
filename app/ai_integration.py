import os
import requests
import json

# Ajusta tu API Key
USDA_API_KEY = "TU_API_KEY_AQUI"
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
HEADERS = {"Content-Type": "application/json"}

# Directorios de almacenamiento
INGREDIENTS_DIR="data/ingredients_data/Greensy"
SUBSTITUTES_DIR="data/sustitutos"
JSON_EXTENSION=".json"

def fetch_nutrient_data(ingredient_name):
    """
    Obtiene datos de la API USDA para un ingrediente, buscando alternativas más relevantes.
    """
    try:
        resp = requests.get(
            BASE_URL,
            params={
                "api_key": USDA_API_KEY,
                "query": f"{ingredient_name} alternative",  # Cambio en la consulta
                "pageSize": 10  # Aumentamos el número de resultados para filtrar
            },
            headers=HEADERS
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error al obtener datos para {ingredient_name}: {e}")
        return None

def store_substitute_data(ingredient_name, data, index=0):
    """
    Guarda en SUBSTITUTES_DIR un archivo JSON con la información de un sustituto relevante.
    """
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
    """
    Busca sustitutos en la API USDA y los filtra antes de guardarlos.
    """
    data = fetch_nutrient_data(ingredient_name)
    if not data or "foods" not in data:
        print(f"Advertencia: no se obtuvieron sustitutos para {ingredient_name}")
        return

    foods = data["foods"]
    if not foods:
        print(f"Advertencia: no hay resultados en la respuesta para {ingredient_name}")
        return

    valid_replacements = []
    
    for food_item in foods:
        if "foodCategory" in food_item and "coffee" not in food_item["foodCategory"].lower():
            valid_replacements.append(food_item)

    if not valid_replacements:
        print(f"No se encontraron sustitutos adecuados para {ingredient_name}")
        return
    
    for i, food_item in enumerate(valid_replacements[:3]):  # Guardar hasta 3
        store_substitute_data(ingredient_name, food_item, i)

if __name__ == "__main__":
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
