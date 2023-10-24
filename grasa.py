import csv

def fila(direccion_csv):
    primera_fila = []  # Usamos una lista para mantener el orden de los elementos

    with open(direccion_csv, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            if fila:  # Verificamos si la fila no está vacía
                elementos = [elemento.strip() for elemento in fila]
                for elemento in elementos:
                    primera_fila.append(elemento)  # Agregamos cada elemento a la lista
                break  # Terminamos después de procesar la primera fila

    return primera_fila

def columna(direccion_csv):
    primera_columna = set()  # Usamos un conjunto para evitar duplicados

    with open(direccion_csv, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            if fila:  # Verificamos si la fila no está vacía
                # Dividimos la fila en elementos separados por comas y eliminamos espacios en blanco
                elementos = [elemento.strip() for elemento in fila[0].split(',')]
                for elemento in elementos:
                    primera_columna.add(elemento)  # Agregamos cada elemento al conjunto

    return primera_columna


def leer_transiciones(archivo_csv):
    transiciones = {}

    with open(archivo_csv, 'r') as f:
        lector = csv.reader(f)
        headers = next(lector)  # Obtenemos los encabezados
        
        for fila in lector:
            estado_inicial = fila[0]
            for index, estado_destino in enumerate(fila[1:], start=1):  # Ignoramos la última columna "final"
                entrada = headers[index]
                transiciones[(estado_inicial, entrada)] = estado_destino

    return transiciones

archivo_csv = "celula.csv"  # Reemplaza "tu_archivo.csv" por el nombre/path de tu archivo
transiciones = leer_transiciones(archivo_csv)
print(transiciones)
#transiciones = fila(archivo_csv)

#estados = {'q5-q27-q0':'if','q38-q0':'do','q47-q0-q6':'int','q56-q0-q7':'for','q67-q0':'enum','q14-q69-q0':'else','q70-q0':'goto','q73-q0':'auto','q13-q85-q0':'long','q13-q85-q0':'void','q88-q14-q0':'case','q91-q0-q7':'char','q0-q96':'union','q97-q0':'break','q0-q102-q6':'short','q105-q0-q6':'float','q14-q0-q106':'while','q108-q0-q23-q6':'const','q112-q0':'extern','q138-q0-q133':'signed','q5-q0-q115':'sizeof','q1-q0-q116':'static','q0-q117-q6':'struct','q37-q0-q118':'switch','q0-q120':'return','q125-q14-q0':'double','q65-q5-q0-q129':'typedef','q132-q0-q6':'default','q138-q0-q133-q134':'unsigned','q0-q7-q135':'register','q14-q0-q136':'volatile','q137-q14-q0':'continue'}        
        
#print(estados.keys())
