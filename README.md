
# PredictorDepurador

Sistema que preprocesa un video, ejecuta la prediccion, y otorga la posibilidad de postprocesamiento.

## Instalacion

Las Liberias necesarias para ejecutar el proyecto son:

**-Ultralytics**

**-Opencv**

**-Pillow**

## Organización
El sistema está dividido en tres fases principales: Preprocesamiento (preparación de datos), Procesamiento (ejecución del modelo) y Postprocesamiento (renderizado y filtrado).

### Prepocesamiento
Esta fase prepara los videos de entrada para el entrenamiento del modelo.

**Primero** con `pre_ReductorDeFps.py` se reducen los fps de un video a la cantidad indicada en el codigo, en este caso 5.

**Segundo** `pre_SelecitorDeFrames.py` toma el video total y toma la cantidad de frames indicada en el codigo, ademas a cada frame le asigna el nombre con un contador, este contador inicia en el valor que se le indique en el codigo.

**Tercero** `pre_Aleatorizador.py` Toma una carpeta con imagenes, aleatoriza el orden cambiandoles el nombre.

**Cuarto** `pre_entrenamiento.py` toma la infrmacion en data.yaml (Ubicacion del dataset, train y val) y de sus etiquetas y hace el entrenamiento con el modelo de YOLO indicado. Y guarda el modelo entrenado en un archivo llamado `best.pt` 

### Pocesamiento
Esta fase utiliza el modelo `best.pt` entrenado para realizar detecciones en nuevos videos, se tienen dos opciones de procesamiento.

**El primer archivo** `pro_PrediccionVisualizacion.py`, hace las predicciones frame por frame mostrandolo en una ventana.

**El segundo archivo** `pro_PrediccionBack.py` que hace el procesamiento video intermente, cuando termina, exporta un video con sus predicciones y etiquetas en un archivo .avi. y para terminar exporta un archivo JSON, con la etiquetas de cada frame

### Postpocesamiento
Esta fase permite trabajar con los resultados de la predicción de forma separada al video.

**Con el archivo** `post_renderizar.py` Toma un archivo JSON con etiquetas(Ya filtradas o no) y las renderiza en el video original con cv2.


