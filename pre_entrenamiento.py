from ultralytics import YOLO

model = YOLO('yolov8s.pt')

model.train(
    data='Tarea1/dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=8
)
