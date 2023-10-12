import csv

def leer_transiciones(archivo_csv):
    transiciones = {}

    with open(archivo_csv, 'r') as f:
        lector = csv.reader(f)
        headers = next(lector)  # Obtenemos los encabezados
        
        for fila in lector:
            estado_inicial = fila[0]
            for index, estado_destino in enumerate(fila[1:-1], start=1):  # Ignoramos la última columna "final"
                entrada = headers[index]
                transiciones[(estado_inicial, entrada)] = estado_destino

    return transiciones

archivo_csv = "vaBien.csv"  # Reemplaza "tu_archivo.csv" por el nombre/path de tu archivo
transiciones = leer_transiciones(archivo_csv)
print(transiciones)
