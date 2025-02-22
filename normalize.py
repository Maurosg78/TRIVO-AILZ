
import json

def normalize_data(data):
    normalized_data = {}
    for ingredient, values in data.items():
        normalized_values = {}
        for key, value in values.items():
            normalized_values[key.lower().replace(" ", "_")] = value
        normalized_data[ingredient] = normalized_values
    return normalized_data

if __name__ == "__main__":
    with open("ingredients.json") as f:
        ingredients_data = json.load(f)

    print(normalize_data(ingredients_data))

