# nutrient_optimizer.py

import requests

def get_nutrient_data(ingredient, config):
    """
    Obtiene los datos nutricionales de un ingrediente usando la API de USDA.
    """
    base_url = config.get('base_url', 'https://api.nal.usda.gov/fdc/v1')
    api_key = config.get('api_key')
    search_url = f"{base_url}/foods/search"
    params = {
        "api_key": api_key,
        "query": ingredient,
        "pageSize": 1
    }
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('foods'):
            food = data['foods'][0]
            nutrients = {}
            for nutrient in food.get('foodNutrients', []):
                nutrient_name = nutrient.get('nutrientName')
                nutrient_value = nutrient.get('value')
                if nutrient_name and nutrient_value is not None:
                    nutrients[nutrient_name] = nutrient_value
            return nutrients
        else:
            return {"error": "No se encontraron resultados para este ingrediente."}
    else:
        return {"error": f"Error en la API: {response.status_code}"}

def optimize_specific_nutrient(ingredients, target_nutrient, target_value, config):
    """
    Optimiza una receta para mejorar un nutriente específico.
    
    Args:
        ingredients (dict): Ingredientes de la receta.
        target_nutrient (str): Nutriente objetivo (ej. "protein").
        target_value (float): Valor objetivo del nutriente.
        config (dict): Configuración de la API.
    
    Returns:
        dict: Datos nutricionales de los ingredientes optimizados.
    """
    nutrient_data = {}
    for ingredient in ingredients:
        nutrient_data[ingredient] = get_nutrient_data(ingredient, config)
    
    # Filtrar los nutrientes que necesitan optimización
    for ingredient, data in nutrient_data.items():
        if target_nutrient in data:
            current_value = data[target_nutrient]
            if current_value < target_value:
                # Proponer un reemplazo si el valor actual es menor que el objetivo
                replacement = suggest_replacement(ingredient, target_nutrient, target_value, config)
                print(f"Reemplazar {ingredient} con {replacement} para mejorar {target_nutrient}.")
    
    return nutrient_data

def suggest_replacement(ingredient, target_nutrient, target_value, config):
    """
    Sugiere un reemplazo basado en el nutriente objetivo.
    
    Args:
        ingredient (str): Ingrediente a reemplazar.
        target_nutrient (str): Nutriente objetivo (ej. "protein").
        target_value (float): Valor objetivo del nutriente.
        config (dict): Configuración de la API.
    
    Returns:
        str: Nombre del ingrediente de reemplazo.
    """
    if target_nutrient == "protein":
        potential_replacements = ["lentejas", "proteína de guisante", "tofu"]
        best_replacement = max(
            potential_replacements,
            key=lambda x: get_nutrient_data(x, config).get('protein', 0)
        )
        return best_replacement
    else:
        # Otros nutrientes como fibra, vitaminas, etc.
        return ingredient  # No se propone un reemplazo si no se encuentra algo mejor
