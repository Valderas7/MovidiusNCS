#!/usr/bin/env python
# coding: utf-8
# Se importan librerías:
import os # Listado archivos
import cv2 # OpenCV
import numpy as np # Manipular arrays
import time # Medir el tiempo de ejecución

# Se carga el modelo:
red = cv2.dnn.readNet('/home/pi/T-F-M/Valderas/modelos/modelo.xml', '/home/pi/T-F-M/Valderas/modelos/modelo.bin') 

# Se especifica el dispositivo objetivo (NCS):
red.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

# Se especifica el directorio principal y se crea un array para recopilar las imágenes:
directorio = "/home/pi/T-F-M/Valderas/test"
imagenes = []

# Se imprime la lista de imágenes, se leen cada una de ellas y se van añadiendo a la lista:
for dirPath, dirNames, fileNames in os.walk(directorio): # Genera los nombres de los archivos
    print('Lista de archivos:') 
    for f in fileNames:
        print(os.path.join(dirPath, f))        
        img = cv2.imread(os.path.join(dirPath, f)) # Se lee una imagen dentro del directorio establecido
        img = img.astype('float32') / 255 # Transformar imagen en formato float32 y se escalan los píxeles con valores entre (0-1)
        imagenes.append(img) # La imagen se añade al array           
print('[Info] Todas las imágenes han sido leídas\n')

# Para todas las imágenes del array:
for i in range(len(imagenes)):
    # Se prepara el objeto binario grande (la imagen) como entrada de la red neuronal: 
    blob = cv2.dnn.blobFromImage(imagenes[i], size=(180, 180), ddepth=cv2.CV_32F) # Se crea BLOB desde la imagen
    red.setInput(blob) # Se establece el BLOB creado como entrada de la red neuronal

    # Se obtiene la clasificación de salida y se mide el tiempo de ejecución:
    inicio = time.time() # Inicio del contador para cada BLOB
    out = red.forward() # Se calcula la salida de la red neuronal
    fin = time.time() # Final del contador para cada BLOB
    print("[Info] El tiempo de ejecución fue de {:.3} segundos".format(fin - inicio)) # 3 cifras significativas
    
    # Se imprime por pantalla salida y la probabilidad. La salida de la red da un valor dentro del intervalo (0-1).
    if out[0][np.argmax(out)]*100 > 50: # Cuanto más cerca del '1', más probable que la imagen sea de un perro.
      print('La imagen es de un: Perro (Probabilidad: {:.4}%)\n'.format(out[0][np.argmax(out)]*100))
    else: # Cuanto mas cerca del '0', más probable que la imagen sea de un gato. 
      print('La imagen es de un: Gato (Probabilidad: {:.4}%)\n'.format(100-out[0][np.argmax(out)]*100))