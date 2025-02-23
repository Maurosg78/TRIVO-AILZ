import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Concatenate
import numpy as np
import json
import os

# Directorios de datos
DATA_DIR = "data/normalized_recipes/"
SUBSTITUTES_DIR = "data/sustitutos/"

# Cargar lista de archivos JSON
recipe_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
substitutes_files = [f for f in os.listdir(SUBSTITUTES_DIR) if f.endswith(".json")]

def load_data():
    data = []
    context = []
    labels = []
    
    # Procesar recetas normales
    for file in recipe_files:
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            try:
                recipe = json.load(f)
                ingredients = recipe.get("ingredients", [])
                process = recipe.get("process", {})

                for ing in ingredients:
                    data.append([ing.get("amount", 0)])
                    context.append([
                        process.get("oven_type", 0),
                        process.get("mixer_type", 0),
                        process.get("temperature", 0),
                        process.get("fermentation_time", 0),
                        process.get("humidity", 0)
                    ])
                    labels.append(ing.get("optimized_amount", 0))
            except json.JSONDecodeError as e:
                print(f"⚠️ Error en archivo {file}: {e}")

    # Procesar sustitutos correctamente
    for file in substitutes_files:
        with open(os.path.join(SUBSTITUTES_DIR, file), "r", encoding="utf-8") as f:
            try:
                substitutes = json.load(f)

                if isinstance(substitutes, dict):
                    food_nutrients = substitutes.get("foodNutrients", [])
                    input_foods = substitutes.get("finalFoodInputFoods", [])

                    # Extraer peso desde foodNutrients si existe
                    amount = next((n["value"] for n in food_nutrients if n["nutrientName"] in ["Weight", "Gram Weight"]), 0)

                    # Extraer peso desde finalFoodInputFoods si foodNutrients no lo tiene
                    if amount == 0 and input_foods:
                        amount = sum(f["gramWeight"] for f in input_foods if "gramWeight" in f)

                    # Usamos una estimación para el "optimized_amount"
                    optimized_amount = amount * 0.9  # Supongamos que optimizamos reduciendo un 10%

                    # Agregar datos a la lista
                    data.append([amount])
                    labels.append(optimized_amount)
            except json.JSONDecodeError as e:
                print(f"⚠️ Error en archivo {file}: {e}")

    return (
        np.array(data, dtype=np.float32),
        np.array(context, dtype=np.float32).reshape(-1, 5),  # Asegurar forma correcta
        np.array(labels, dtype=np.float32)
    )

# Cargar datos
X, X_context, y = load_data()

# Verificar que hay datos
if len(X) == 0 or len(X_context) == 0 or len(y) == 0:
    raise ValueError("❌ Error: No se encontraron datos para entrenar. Verifica los archivos en data/normalized_recipes/ y data/sustitutos/")

# Definir arquitectura del modelo con dos entradas
input_ingredients = Input(shape=(1,), name="ingredient_input")
input_context = Input(shape=(5,), name="context_input")  # Ahora garantizamos que X_context tenga 5 columnas

# Red neuronal para ingredientes
hidden_layer = Dense(32, activation="relu")(input_ingredients)
hidden_layer = Dense(64, activation="relu")(hidden_layer)

# Red neuronal para variables contextuales
context_layer = Dense(32, activation="relu")(input_context)
context_layer = Dense(64, activation="relu")(context_layer)

# Fusionar las capas
merged = Concatenate()([hidden_layer, context_layer])
merged = Dense(32, activation="relu")(merged)
output_layer = Dense(1, activation="linear")(merged)

# Crear modelo
model = keras.Model(inputs=[input_ingredients, input_context], outputs=output_layer)

# Compilar modelo
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])

# Entrenar modelo
model.fit([X, X_context], y, epochs=50, batch_size=16)

# Guardar modelo
MODEL_PATH = "app/models/nutrient_optimizer.keras"
model.save(MODEL_PATH)
print(f"✅ Modelo guardado en: {MODEL_PATH}")
