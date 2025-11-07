import cv2

# Abrir el video original
video = cv2.VideoCapture("4.mp4")

# Revisar si se abrió correctamente
if not video.isOpened():
    print("Error al abrir el video")
    exit()

# Obtener propiedades del video original
fps_original = int(video.get(cv2.CAP_PROP_FPS))   # FPS original
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir FPS deseado
fps_nuevo = 5
salida = cv2.VideoWriter("4fps5.mp4",
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         fps_nuevo,
                         (width, height))

# Calcular cuántos frames saltar
step = int(fps_original / fps_nuevo)

print(f"FPS original: {fps_original}, Frames: {frame_count}, Step: {step}")

i = 0
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Guardar solo cada "step" frame
    if i % step == 0:
        salida.write(frame)
    i += 1

video.release()
salida.release()
cv2.destroyAllWindows()

