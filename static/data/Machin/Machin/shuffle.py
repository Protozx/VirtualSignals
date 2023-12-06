import csv
import random

def mezclar_filas_csv(archivo_entrada, archivo_salida):
    # Leer el archivo CSV de entrada
    with open(archivo_entrada, 'r', newline='') as entrada:
        filas = list(csv.reader(entrada))
    
    # Mezclar las filas
    random.shuffle(filas)
    
    # Escribir las filas mezcladas en el archivo de salida
    with open(archivo_salida, 'w', newline='') as salida:
        escritor = csv.writer(salida)
        escritor.writerows(filas)

# Ejemplo de uso
archivo_entrada = 'dataset.csv'  # Reemplaza con la dirección de tu archivo CSV de entrada
archivo_salida = 'dataset.csv'    # Reemplaza con la dirección del archivo CSV de salida
mezclar_filas_csv(archivo_entrada, archivo_salida)