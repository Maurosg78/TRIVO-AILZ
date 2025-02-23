import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, Concatenate
import numpy as np
import json
import os

# Cargar datos normalizados
DATA_DIR = "data/normalized_recipes/"
recipe_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def load_data():
    data = []
    for file in recipe_files:
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            recipe = json.load(f)
            ingredients = recipe.get("ingredients", [])
            for ing in ingredients:
                data.append([
                    ing["amount"], # Cantidad en gramos o ml
                ])
    return np.array(data, dtype=np.float32)

# Cargar datos
X = load_data()

# Definir arquitectura del modelo
input_layer = Input(shape=(1,))  # Entrada: cantidad del ingrediente
hidden_layer = Dense(32, activation="relu")(input_layer)
hidden_layer = Dense(64, activation="relu")(hidden_layer)
hidden_layer = Dense(32, activation="relu")(hidden_layer)
output_layer = Dense(1, activation="linear")(hidden_layer)  # Salida: Ajuste de cantidad

# Crear modelo
model = keras.Model(inputs=input_layer, outputs=output_layer)

# Compilar modelo
model.compile(optimizer="adam", loss="mean_squared_error")

# Resumen del modelo
model.summary()

# Guardar modelo en "app/models/"
MODEL_DIR = "app/models/"
os.makedirs(MODEL_DIR, exist_ok=True)
model.save(os.path.join(MODEL_DIR, "nutrient_optimizer.h5"))

print("✅ Modelo de optimización de nutrientes guardado en:", MODEL_DIR)
