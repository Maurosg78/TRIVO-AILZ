import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd

# Configuración inicial
input_shape = (10,)  # Suponiendo que tenemos 10 características de entrada
output_shape = 1  # Suponiendo que tenemos una salida

# Construcción de la red neuronal profunda
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=input_shape),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(output_shape, activation='sigmoid')  # Salida binaria, puede ajustarse según el problema
])

# Compilación del modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Resumen del modelo
model.summary()

# Guardar el modelo
model.save('/Users/mauriciosobarzo/Desktop/2025/Greensy/Lanzadera/TRIVO-AILZ/TRIVO-AILZ/app/models/modelo_trivo_ai.h5')

