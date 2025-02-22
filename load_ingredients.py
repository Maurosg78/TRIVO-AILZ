import json
import os

# Ruta de la carpeta con los archivos JSON
folder_path = "/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-AILZ/TRIVO-AILZ/data/ingredients_data/Greensy/"

# Lista para almacenar el contenido de los archivos
ingredients_data = {}

# Cargar los archivos JSON
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), "r") as f:
            ingredient_name = filename.replace(".json", "")  # Extraemos el nombre del ingrediente
            ingredients_data[ingredient_name] = json.load(f)

# Mostrar los ingredientes cargados
print(ingredients_data)
