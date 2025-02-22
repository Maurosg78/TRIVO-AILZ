import requests

def get_nutrient_data(ingredient, config):
    """
    Obtiene los datos nutricionales de un ingrediente usando la API de USDA.
    
    Args:
        ingredient (str): Nombre del ingrediente.
        config (dict): Configuración de la API (base_url y api_key).
    
    Returns:
        dict: Datos nutricionales del ingrediente.
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

def analyze_nutrients(ingredients, config):
    """
    Analiza los nutrientes de una lista de ingredientes.
    
    Args:
        ingredients (list): Lista de ingredientes.
        config (dict): Configuración de la API.
    
    Returns:
        dict: Resultados del análisis nutricional.
    """
    results = {}
    for ingredient in ingredients:
        nutrient_data = get_nutrient_data(ingredient, config)
        results[ingredient] = nutrient_data
    return results