import requests
import json

# Base URL for USDA API
base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Your USDA API key
api_key = "VoUZcYnQ04PKmQU6x34ZlvJaMmgb4ad7dQ CwMK38"

# Load the ingredients data
with open('ingredients.json', 'r') as f:
    ingredients_data = json.load(f)

def get_substitute(ingredient_name):
    # Perform a query to USDA API for ingredient
    response = requests.get(f"{base_url}?query={ingredient_name}&api_key={api_key}")
    if response.status_code == 200:
        data = response.json()
        # Returning substitutes if available, you can refine this depending on the actual API response
        substitutes = [item['description'] for item in data.get('foods', [])]
        return substitutes
    else:
        return []

# Testing substitution for an ingredient
ingredient_name = 'chickpea'  # Example ingredient name, you can loop through your data
substitutes = get_substitute(ingredient_name)

print(substitutes)
