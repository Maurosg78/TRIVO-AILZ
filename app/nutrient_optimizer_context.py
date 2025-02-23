import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Concatenate
import numpy as np
import json
import os

# Cargar datos normalizados
DATA_DIR = "data/normalized_recipes/"
recipe_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def load_data():
    data = []
    context = []
    for file in recipe_files:
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            recipe = json.load(f)
            ingredients = recipe.get("ingredients", [])
            process = recipe.get("process", {})  # Cargar variables contextuales

            for ing in ingredients:
                data.append([ing["amount"]])  # Cantidad en gramos o ml
                context.append([
                    process.get("oven_type", 0),
                    process.get("mixer_type", 0),
                    process.get("temperature", 0),
                    process.get("fermentation_time", 0),
                    process.get("humidity", 0)
                ])

    return np.array(data, dtype=np.float32), np.array(context, dtype=np.float32)

# Cargar datos
X, X_context = load_data()

# Definir arquitectura del modelo con dos entradas
input_ingredients = Input(shape=(1,), name="ingredient_input")
input_context = Input(shape=(5,), name="context_input")  # 5 Variables contextuales

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
model.compile(optimizer="adam", loss="mean_squared_error")

# Resumen del modelo
model.summary()

# Guardar modelo en "app/models/"
MODEL_DIR = "app/models/"
os.makedirs(MODEL_DIR, exist_ok=True)
model.save(os.path.join(MODEL_DIR, "nutrient_optimizer_context.h5"))

print("✅ Modelo de optimización con variables contextuales guardado en:", MODEL_DIR)
