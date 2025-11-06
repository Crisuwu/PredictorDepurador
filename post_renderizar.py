import cv2
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --- Configuración ---
# ¡Asegúrate que este nombre coincida con tu archivo JSON!
json_path = 'result.json' 
video_path = 'video.avi' # ¡Verifica que este sea el nombre de tu video!
output_path = 'Video_depurado.mp4' 
font_path = 'arial.ttf' # IMPORTANTE: Debe estar en la misma carpeta
font_size = 20
line_width = 3

# --- Mapa de Colores (en RGB para Pillow) ---
COLOR_MAP = {
    0: (0, 255, 0),    # Casco -> Verde Brillante
    1: (255, 0, 0),    # Sin casco -> Rojo Brillante
    2: (0, 0, 255),    # Mascarilla -> Azul Brillante
    3: (255, 255, 0),  # Sin mascarilla -> Amarillo
    4: (0, 255, 255),  # Chaleco reflectante -> Cyan
    5: (255, 0, 255)   # Sin chaleco reflectante -> Magenta
}
FALLBACK_COLOR = (255, 255, 255) # Blanco

# #################################################################
# ###               INICIO DE LA SECCIÓN CORREGIDA              ###
# #################################################################

print(f"Cargando datos JSON desde {json_path}...")
data_por_fotograma = [] # La lista que usará el resto del script
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        # 1. Cargar el objeto JSON completo de una sola vez
        all_data_dict = json.load(f)
    
    # 2. Convertir el diccionario ({"frame_0":...}) a una lista ([...])
    #    ordenada numéricamente por el número de frame.
    
    # Ordenamos las claves (ej. "frame_1", "frame_10") por su número
    sorted_keys = sorted(all_data_dict.keys(), key=lambda k: int(k.split('_')[1]))
    
    # 3. Construimos la lista 'data_por_fotograma' en el orden correcto
    for key in sorted_keys:
        data_por_fotograma.append(all_data_dict[key])
        
    print(f"Se cargaron {len(data_por_fotograma)} fotogramas de datos JSON.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo JSON {json_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: El archivo {json_path} no es un JSON válido o está mal formado.")
    exit()
except Exception as e:
    print(f"Ocurrió un error inesperado al cargar el JSON: {e}")
    exit()

# #################################################################
# ###                 FIN DE LA SECCIÓN CORREGIDA               ###
# #################################################################


# --- Cargar la fuente personalizada ---
try:
    font = ImageFont.truetype(font_path, font_size)
    font_frame_counter = ImageFont.truetype(font_path, font_size + 10) # Fuente más grande para el contador
except IOError:
    print(f"Error: No se pudo cargar la fuente en {font_path}")
    print("Usando fuente por defecto de Pillow.")
    font = ImageFont.load_default()
    font_frame_counter = font
# --- Fin de carga de fuente ---


print(f"Abriendo video de entrada: {video_path}...")
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: No se pudo abrir el video {video_path}")
    exit()

# Propiedades del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# --- Codec MP4 para mejor calidad ---
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Usar 'mp4v' para .mp4
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
# --- FIN DE NUEVO CODEC ---

print("Procesando video y dibujando con Pillow...")
frame_idx = 0 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # --- PROCESO CON PILLOW ---
    # 1. Convertir fotograma de OpenCV (BGR) a Imagen de Pillow (RGB)
    cv_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_frame_rgb)
    
    # 2. Crear objeto de dibujo
    draw = ImageDraw.Draw(pil_img)
    # --- FIN PROCESO PILLOW ---

    # Dibujar detecciones (si existen para este frame)
    # Esta lógica ahora funciona porque 'data_por_fotograma' es una lista
    if frame_idx < len(data_por_fotograma):
        detections = data_por_fotograma[frame_idx]
        
        for det in detections:
            box = det['box']
            x1, y1, x2, y2 = int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2'])
            
            class_id = det.get('class')
            color = COLOR_MAP.get(class_id, FALLBACK_COLOR) 

            # Dibujar caja (con Pillow)
            draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=line_width)
            
            label = f"{det['name']} ({det['confidence']:.2f})"
            if 'track_id' in det:
                label += f" ID: {det['track_id']}"
            
            # Dibujar texto (con Pillow)
            text_y_pos = y1 - font_size - 5
            # Asegurarse que el texto no se dibuje fuera de la pantalla (arriba)
            if text_y_pos < 5:
                text_y_pos = y1 + 5 
            
            draw.text((x1, text_y_pos), label, font=font, fill=color)

    # Dibujar el número de fotograma (con Pillow)
    frame_text = f"Frame: {frame_idx}"
    draw.text((30, 40), frame_text, font=font_frame_counter, fill=(255, 255, 255))

    # --- DE VUELTA A OPENCV ---
    # 1. Convertir Imagen de Pillow (RGB) de nuevo a fotograma de OpenCV (BGR)
    frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    # --- FIN DE VUELTA A OPENCV ---
    
    out.write(frame_bgr)
    
    if frame_idx % 30 == 0:
        print(f"Procesado frame {frame_idx}...")
        
    frame_idx += 1

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"¡Proceso completado! Video guardado en: {output_path}")
