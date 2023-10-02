import cv2
import numpy as np
import json


def calcular_histograma(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    histograma_r = cv2.calcHist([imagen_rgb], [0], None, [256], [0, 256])
    histograma_g = cv2.calcHist([imagen_rgb], [1], None, [256], [0, 256])
    histograma_b = cv2.calcHist([imagen_rgb], [2], None, [256], [0, 256])
    return histograma_r, histograma_g, histograma_b


def cargar_diccionario(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        diccionario = json.load(archivo)
    return diccionario


def clasificar_imagen(ruta_imagen, dict_prom):
    histograma_imagen = calcular_histograma(ruta_imagen)
    distancia_playas = np.linalg.norm(histograma_imagen - np.array(dict_prom["playas"]))
    distancia_montanas = np.linalg.norm(histograma_imagen - np.array(dict_prom["montana"]))
    distancia_praderas = np.linalg.norm(histograma_imagen - np.array(dict_prom["praderas"]))
    if distancia_playas < distancia_montanas and distancia_playas < distancia_praderas:
        return "Playa",cargar_diccionario("playas.json")
    elif distancia_montanas < distancia_playas and distancia_montanas < distancia_praderas:
        return "Zona montañosa",cargar_diccionario("montanas.json")
    else:
        return "Pradera",cargar_diccionario("praderas.json")
    

def calcular_centroide(diccionario):
    centroides = {}
    for clase, valores in diccionario.items():
        total_puntos = len(valores)
        centroides[clase] = [0, 0, 0, 0, 0] 
        for pixel in valores:
            rgb = pixel[0]
            x, y = tuple(pixel[1])
            centroides[clase][0] += rgb[2]
            centroides[clase][1] += rgb[1]
            centroides[clase][2] += rgb[0]
            centroides[clase][3] += x
            centroides[clase][4] += y
        centroides[clase] = [valor / total_puntos for valor in centroides[clase]] 
        centroides[clase] = np.array(centroides[clase])
    return centroides


def clasificar_pixel(pixel, centroides):
    distancias = []
    for clase, centroide in centroides.items():
        distancia = np.linalg.norm(pixel - centroide)
        distancias.append((clase, distancia))
    distancias = sorted(distancias, key=lambda x: x[1])
    return distancias[0][0]


def pintar_imagen(ruta, centroides):
    img = cv2.imread(ruta)
    img = cv2.medianBlur(img, 3)
    aux = np.zeros_like(img)
    height, width, _ = img.shape
    for y in range(height):
        for x in range(width):
            rgb = img[y, x]
            coordenadas = [rgb[2], rgb[1], rgb[0], x, y]
            clase = clasificar_pixel(coordenadas, centroides)
            if clase == "cielo":
                aux[y, x] = (0, 255, 255)
            elif clase == "montana":
                aux[y, x] = (128, 0, 128)
            elif clase == "pasto":
                aux[y, x] = (45, 87, 44)
            elif clase == "arena":
                aux[y, x] = (255, 255, 0)
            elif clase == "mar":
                aux[y, x] = (0, 0, 0)
    return aux


def detectar_contornos(imagen, num_contornos):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Paso 3: Aplicar un umbral a la imagen para convertirla en una imagen binaria
    _, binaria = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

    # Paso 4: Encontrar los contornos en la imagen binaria
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Paso 5: Ordenar los contornos de acuerdo a su área en orden descendente
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)

    # Paso 6: Crear una imagen completamente negra del mismo tamaño que la imagen original
    imagen_negra = np.zeros_like(imagen)

    # Paso 7: Dibujar los n contornos más grandes en la imagen negra
    cv2.drawContours(imagen_negra, contornos[:num_contornos], -1, (255, 255, 255), 1)

    imagen_negra[0, :] = [0,0,0]
    imagen_negra[-1, :] = [0,0,0]
    imagen_negra[:, 0] = [0,0,0]
    imagen_negra[:, -1] = [0,0,0]
    return imagen_negra


def virtualnature(ruta_img):
    print(ruta_img)
    org = cv2.imread(ruta_img)
    print(org)
    prom_hist = cargar_diccionario("promedio_histogramas.json")
    clase,dictjson_paisaje = clasificar_imagen(ruta_img, prom_hist)
    centroides = calcular_centroide(dictjson_paisaje)
    imagen = pintar_imagen(ruta_img, centroides)
    imagen = cv2.medianBlur(imagen, 5)
    contornos = detectar_contornos(imagen, len(centroides)-1)
    imagen = cv2.resize(imagen, (350, 350))
    cv2.imwrite("static/img/clases.jpg", imagen)

    # Para especificar las dimensiones de la imagen2
    contornos = cv2.resize(contornos, (350, 350))  # Redimensiona la imagen a 1024x768 píxeles
    cv2.imwrite("static/img/contornos.jpg", contornos)
    cv2.imwrite("static/img/original.jpg", org)
    if clase == "Pradera":
        return ["La region mayormente de color verde es el pasto", "La region mayormente de color amarillo es el cielo", "Por lo tanto, es una pradera", ""]
    elif clase == "Playa":
        return ["La region mayormente de color cyan es el arena", "La region mayormente de color amarillo es el cielo", "La region mayormente de color negro es el mar", "Por lo tanto, es una playa"]
    else:
        return ["La region mayormente de color violeta es la montaña", "La region mayormente de color amarillo es el cielo", "Por lo tanto, es una region montañosa", ""]
    
    
    


if __name__ == "__main__":
    ruta_img = "img12.jpg"
    org = cv2.imread(ruta_img)
    prom_hist = cargar_diccionario("promedio_histogramas.json")
    dictjson_paisaje = clasificar_imagen(ruta_img, prom_hist)
    centroides = calcular_centroide(dictjson_paisaje)
    imagen = pintar_imagen(ruta_img, centroides)
    imagen = cv2.medianBlur(imagen, 5)
    contornos = detectar_contornos(imagen, len(centroides)-1)
    cv2.imshow('Original', org)
    cv2.imshow('Deteccion de clases', imagen)
    cv2.imshow('Contornos', contornos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()