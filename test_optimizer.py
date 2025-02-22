import json

def analyze_ingredients(ingredients):
    with open("ingredients.json") as f:
        ingredients_data = json.load(f)

    analysis_results = {}
    for ingredient in ingredients:
        # Convertir a minúsculas para uniformidad
        ingredient = ingredient.lower()

        if ingredient in ingredients_data:
            substitutes = ingredients_data[ingredient]
            analysis_results[ingredient] = {"substitutes": substitutes}
        else:
            analysis_results[ingredient] = {"error": "No se encontraron sustitutos para este ingrediente."}

    return analysis_results


# Ejemplo de uso
ingredients = ["cauliflower", "rice flour", "salt", "water"]
analysis_results = analyze_ingredients(ingredients)
print(analysis_results)
