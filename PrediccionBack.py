from ultralytics import YOLO
import os
import json

# --- Nombres de archivos ---
model_path = 'best.pt'
video_path = 'video.avi'

# 1. Cargar el modelo
model = YOLO(model_path)

resultados = model.track(
      source=video_path,
      persist=True,
      imgsz=640,
      verbose=False,
      save=True,
      line_width=1
  )
print("¡Video procesado con éxito! ")
print("Iniciando escritura de resultados en archivo JSON ")

result_dict = {}

for i in range(len(resultados)):
  json_string = resultados[i].to_json()
  frame_number = f'frame_{i}'
  result_dict[frame_number] = json.loads(json_string)

with open('result.json', 'w') as fp:
    json.dump(result_dict, fp, indent=4)
    
print("Finalizando escritura de resultados en archivo JSON ")    