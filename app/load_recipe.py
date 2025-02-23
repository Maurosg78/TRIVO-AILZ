import json, sys

if len(sys.argv) < 2:
    print("❌ Error: Debes proporcionar el nombre de la receta como argumento.")
    sys.exit(1)

recipe_name = sys.argv[1].strip().lower()
file_path = f"data/processed_recipes/{recipe_name}.json"

try:
    with open(file_path, "r") as f:
        data = json.load(f)

    recipe_data = {
        "name": data.get("ingredient_name", recipe_name),
        "nutrients": data.get("nutrients", {})
    }

    print(json.dumps(recipe_data, indent=2))

except FileNotFoundError:
    print(f"❌ Error: No se encontró la receta {recipe_name}.", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"❌ Error: El archivo de la receta {recipe_name} no es un JSON válido.", file=sys.stderr)
    sys.exit(1)
