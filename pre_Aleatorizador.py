import os
import random
import shutil

# Carpetas
input_folder = "frames_seleccionados"
output_folder = "frames_aleatorios"

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Obtener lista de imágenes
imagenes = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Aletorizar
random.shuffle(imagenes)

# Nombrar con contador
for i, nombre in enumerate(imagenes, start=1):
    ruta_origen = os.path.join(input_folder, nombre)
    ruta_destino = os.path.join(output_folder, f"{i}.jpg")
    shutil.copy(ruta_origen, ruta_destino)

print(f"Se copiaron {len(imagenes)} imágenes en orden aleatorio a '{output_folder}'.")

