import json, os, numpy as np

dir_path = "data/normalized_recipes"
training_data = {}

for file in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Asegurar que el archivo contiene los nutrientes correctamente
        if "nutrients" in data and isinstance(data["nutrients"], dict):
            training_data[data["name"]] = data["nutrients"]
        else:
            print(f"❌ Error cargando {file}: No se encontraron nutrients.")

    except Exception as e:
        print(f"❌ Error cargando {file}: {str(e)}")

# Guardar en un archivo numpy
np.save("data/training_data.npy", training_data)
print("✅ Datos normalizados guardados en data/training_data.npy")
