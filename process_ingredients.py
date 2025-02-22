import json
import os

# Ruta de la carpeta que contiene los archivos JSON de los ingredientes
base_folder = "/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-AILZ/TRIVO-AILZ/data/ingredients_data"
greensy_folder = os.path.join(base_folder, "Greensy")
substitutes_folder = os.path.join(base_folder, "substitutes")

# Crear las carpetas si no existen
os.makedirs(greensy_folder, exist_ok=True)
os.makedirs(substitutes_folder, exist_ok=True)

# Función para cargar los archivos JSON de la carpeta
def load_ingredients():
    original_ingredients = {}
    substitute_ingredients = {}

    for filename in os.listdir(greensy_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(greensy_folder, filename)
            with open(filepath, "r") as f:
                ingredient_data = json.load(f)
                
                # Distinguimos entre ingredientes originales y sustitutos
                if "substitutes" in ingredient_data:
                    substitute_ingredients[filename] = ingredient_data
                    # Guardar los sustitutos en la carpeta correspondiente
                    with open(os.path.join(substitutes_folder, filename), w) as f_sub:
                        json.dump(ingredient_data, f_sub, indent=4)
                else:
                    original_ingredients[filename] = ingredient_data
    
    return original_ingredients, substitute_ingredients

# Cargar los ingredientes
original_ingredients, substitute_ingredients = load_ingredients()

# Mostrar los ingredientes cargados
print("Ingredientes originales:")
for ingredient, data in original_ingredients.items():
    print(fIngrediente: {ingredient})
    print(fDatos: {data})

print("
Sustitutos:")
for ingredient, data in substitute_ingredients.items():
    print(fIngrediente: {ingredient})
    print(fDatos: {data})
