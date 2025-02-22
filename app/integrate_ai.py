import os
import json
import numpy as np
from tensorflow import keras

MODEL_PATH = "app/models/modelo_trivo_ai.h5"
ORIGINAL_DIR = "/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-AILZ/TRIVO-AILZ/data/ingredients_data/Greensy/"
SUBSTITUTES_DIR = "/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-AILZ/TRIVO-AILZ/data/sustitutos/"
JSON_EXTENSION = ".json"

# Carga el modelo
model = keras.models.load_model(MODEL_PATH)

def extract_and_vectorize(food_data):
    """
    Extrae nutrientes clave y los vectoriza en el orden que el modelo espera.
    Ajusta las claves si tu modelo fue entrenado con otras variables.
    """
    nutrient_keys = ["Protein", "Carbohydrate", "Fat", "Fiber", "Calcium"]
    vector = []
    # food_data debería tener la forma:
    # { "description": "...", "foodNutrients": [{ "nutrientName": "...", "value": ... }, ... ] }
    for nutrient in nutrient_keys:
        found = next((n for n in food_data.get("foodNutrients", [])
                      if n["nutrientName"] == nutrient), None)
        vector.append(found["value"] if found else 0.0)
    return np.array(vector, dtype=np.float32)

def predict_substitute(original_features, substitute_features):
    """
    Predice si un sustituto es adecuado (0..1).
    """
    input_data = np.concatenate([original_features, substitute_features])
    input_data = np.expand_dims(input_data, axis=0)
    prediction = model.predict(input_data)[0][0]
    return prediction

def find_best_substitute(original_data, substitute_candidates):
    """
    Compara cada candidato con la IA.
    Si la predicción > 0.5, lo consideramos válido.
    Devuelve lista ordenada por score desc.
    """
    original_features = extract_and_vectorize(original_data)
    substitutes = []
    for sub_data in substitute_candidates:
        sub_features = extract_and_vectorize(sub_data)
        if sub_features is None:
            continue
        score = predict_substitute(original_features, sub_features)
        if score > 0.5:
            # description es la clave que usaremos como nombre del sustituto
            substitutes.append((sub_data.get("description", "Unknown"), score))
    return sorted(substitutes, key=lambda x: x[1], reverse=True)

def fetch_substitute_data(ingredient_name):
    """
    Busca archivos .json en SUBSTITUTES_DIR que contengan la cadena del ingrediente.
    Los carga y devuelve la data en forma de lista de dicts.
    """
    results = []
    if not os.path.isdir(SUBSTITUTES_DIR):
        print(f"Error: Directorio de sustitutos no encontrado en {SUBSTITUTES_DIR}")
        return results

    # Convertir el nombre en algo más estandar
    name_lower = ingredient_name.lower().replace(" ", "_")

    for sub_file in os.listdir(SUBSTITUTES_DIR):
        if not sub_file.endswith(JSON_EXTENSION):
            continue
        # Ej: si sub_file = "chickpea_flour_alternative.json" y name_lower = "chickpea_flour"
        # checamos si "chickpea_flour" in "chickpea_flour_alternative.json"
        if name_lower in sub_file.lower():
            file_path = os.path.join(SUBSTITUTES_DIR, sub_file)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                # data debería ser un dict con "description" y "foodNutrients"
                results.append(data)
            except Exception as e:
                print(f"Error cargando {file_path}: {e}")
    return results

def print_recommendations(recommendations):
    print("\nRecomendaciones finales de sustitutos:")
    for ingredient, subs in recommendations.items():
        print(f"\n{ingredient}:")
        if not subs:
            print("  (Ningún sustituto con score > 0.5)")
        for i, (name, score) in enumerate(subs, 1):
            print(f"  {i}. {name} ({score:.2%})")

def integrate_ai_for_substitutes():
    """
    Recorre los .json en ORIGINAL_DIR, extrae su description,
    busca sustitutos y llama al modelo.
    """
    all_recommended = {}
    if not os.path.isdir(ORIGINAL_DIR):
        print(f"Error: Directorio de ingredientes no encontrado en {ORIGINAL_DIR}")
        return

    for filename in os.listdir(ORIGINAL_DIR):
        if not filename.endswith(JSON_EXTENSION):
            continue
        file_path = os.path.join(ORIGINAL_DIR, filename)
        try:
            with open(file_path, "r") as f:
                original_data = json.load(f)
        except Exception as e:
            print(f"Error abriendo {file_path}: {e}")
            continue

        # Nombre del ingrediente original
        # Podría estar en "description", "name" o "food_name"
        # si no, usamos el nombre del archivo
        ingredient_name = (original_data.get("description")
                           or original_data.get("name")
                           or original_data.get("food_name")
                           or filename.replace(JSON_EXTENSION, ""))

        # Buscamos sustitutos
        substitutes_data = fetch_substitute_data(ingredient_name)
        if not substitutes_data:
            print(f"Advertencia: No se encontraron sustitutos para {ingredient_name}")
            continue

        # IA decide
        best = find_best_substitute(original_data, substitutes_data)
        all_recommended[ingredient_name] = best

    print_recommendations(all_recommended)

if __name__ == "__main__":
    integrate_ai_for_substitutes()

