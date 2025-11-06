import cv2
import os
import numpy as np

# Configuración
video_path = "4fps5.mp4"
output_folder = "frames_seleccionados"
num_muestras = 50
start_index = 100   # <-- donde quieres empezar a contar

# Abrir video
video = cv2.VideoCapture(video_path)
if not video.isOpened():
    print("Error al abrir el video")
    exit()

# Propiedades
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Crear carpeta de salida
os.makedirs(output_folder, exist_ok=True)

# Calcular los índices de frames a extraer
indices = np.linspace(0, frame_count - 1, num_muestras, dtype=int)

print(f"Frames totales: {frame_count}, Extrayendo: {num_muestras}")

for idx, frame_number in enumerate(indices):
    # Mover al frame correspondiente
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video.read()
    
    if not ret:
        continue

    # Guardar con offset en el nombre
    filename = os.path.join(output_folder, f"frame_{idx + start_index:03d}.jpg")
    cv2.imwrite(filename, frame)

video.release()
print(f"Listo ✅. Se guardaron {num_muestras} frames en la carpeta '{output_folder}', comenzando en {start_index}.")

