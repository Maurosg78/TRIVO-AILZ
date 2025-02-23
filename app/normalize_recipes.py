import os
import sys
import json

recipe_name = sys.argv[1]
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, '..', 'data', 'processed_recipes', f'{recipe_name}.json')

try:
    with open(data_path) as f:
        data = json.load(f)
except json.JSONDecodeError:
    print(f'❌ Error: {recipe_name}.json tiene formato inválido.')
    sys.exit(1)
except FileNotFoundError:
    print(f'❌ Error: Archivo {recipe_name}.json no encontrado.')
    sys.exit(1)

# Construye el diccionario "food" correctamente
food = {
    'foodNutrients': data.get('foodNutrients', []),
    'name': data.get('name', recipe_name)
}

# Debugging para verificar los datos
print(f"Debug: {recipe_name} -> Claves: {food.keys()}, Nutrientes: {len(food.get('foodNutrients', []))}")


# Valida usando "food", no "data"
if food.get('foodNutrients') and isinstance(food['foodNutrients'], list) and len(food['foodNutrients']) > 0:
    print(f'✅ Nutrientes encontrados en {recipe_name}: {len(food["foodNutrients"])} elementos.')
    # Procesa los nutrientes aquí
else:
    print(f'❌ Error: No se encontraron nutrientes en la receta {recipe_name}.')
