import cv2
from ultralytics import YOLO

VIDEO_PATH = '3_5fps.avi' 

# cargar modelo
try:
    model = YOLO('best.pt')
except Exception as e:
    print(f"Error al cargar el modelo YOLO: {e}")
    print("Asegúrate de tener conexión a internet para descargar el modelo la primera vez.")
    exit()

# Parámetros
CONFIDENCE_THRESHOLD = 0.5   
NEW_SIZE = (640, 480)      
# Inicializa la captura de video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f" Error: No se pudo abrir el archivo de video en {VIDEO_PATH}")
    exit()

print("Iniciando la detección de objetos con optimización de resolución...")

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break  # Sale del bucle si no hay más frames

    resized_frame = cv2.resize(frame, NEW_SIZE)

    results = model(resized_frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

    # El método .plot() de Ultralytics dibuja automáticamente las cajas en el frame
    annotated_frame = results[0].plot()

    # Muestra el frame anotado. El rendimiento dependerá de la potencia de tu Pi.
    cv2.imshow("Deteccion YOLO Optimizada", annotated_frame)
    
    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrando
cap.release()
cv2.destroyAllWindows()
print("Detección finalizada y recursos liberados.")
