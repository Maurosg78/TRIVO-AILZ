
import requests
import json

def get_nutrients(ingredient):
    api_key = 'VoUZcYnQ04PKmQU6x34ZlvJaMmgb4ad7dQCwMK38'
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={ingredient}&api_key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'API request failed with status code {response.status_code}'}

# Example usage
ingredients = ['chickpea', 'cauliflower']
nutrient_data = {}

for ingredient in ingredients:
    nutrient_data[ingredient] = get_nutrients(ingredient)

print(json.dumps(nutrient_data, indent=4))

