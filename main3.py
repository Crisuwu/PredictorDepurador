import cv2
from ultralytics import YOLO

# 1. --- Configuración y Carga del Modelo ---
# NOTA: Asegúrate de que 'ultralytics' y 'opencv-python' estén instalados
#       (pip3 install ultralytics opencv-python)

# Define la ruta de tu archivo de video. ¡Cámbiala según sea necesario!
VIDEO_PATH = '3_5fps.avi' 

# Carga un modelo YOLO. 'yolov8n.pt' (nano) es ideal por su ligereza.
try:
    model = YOLO('best.pt')
except Exception as e:
    print(f"Error al cargar el modelo YOLO: {e}")
    print("Asegúrate de tener conexión a internet para descargar el modelo la primera vez.")
    exit()

# Parámetros
CONFIDENCE_THRESHOLD = 0.5   # Umbral de confianza para las detecciones
NEW_SIZE = (640, 480)        # Tamaño para la optimización de la Raspberry Pi

# Inicializa la captura de video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f" Error: No se pudo abrir el archivo de video en {VIDEO_PATH}")
    exit()

# 2. --- Bucle de Procesamiento Optimizado ---
print("Iniciando la detección de objetos con optimización de resolución...")

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break  # Sale del bucle si no hay más frames

    # OPTIMIZACIÓN CLAVE: Reduce la resolución del frame antes de la detección
    # Esto reduce la carga computacional en el modelo.
    resized_frame = cv2.resize(frame, NEW_SIZE)

    # Realiza la detección en el frame reducido
    # El argumento 'conf' filtra las detecciones por el umbral
    results = model(resized_frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

    # El método .plot() de Ultralytics dibuja automáticamente las cajas en el frame
    annotated_frame = results[0].plot()

    # Muestra el frame anotado. El rendimiento dependerá de la potencia de tu Pi.
    cv2.imshow("Deteccion YOLO Optimizada", annotated_frame)
    
    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 3. --- Limpieza ---
cap.release()
cv2.destroyAllWindows()
print("Detección finalizada y recursos liberados.")
