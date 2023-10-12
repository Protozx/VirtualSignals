import csv

def divide_palabras(palabra1, palabra2):
    segmentos = []
    i = 0
    while i < len(palabra1):
        seg = palabra1[i:]
        if palabra2.startswith(seg):
            segmentos.append(seg)
        i += 1
    return segmentos

def generar_automata(palabras):
    automata = {}
    estado_inicial = 'q0'
    automata[estado_inicial] = {}
    estado_contador = 1

    for palabra in palabras:
        estado_actual = estado_inicial
        i = 0
        while i < len(palabra):
            simbolo = palabra[i]
            if simbolo not in automata[estado_actual]:
                nuevo_estado = 'q' + str(estado_contador)
                automata[estado_actual][simbolo] = nuevo_estado
                if nuevo_estado not in automata:
                    automata[nuevo_estado] = {}
                estado_actual = nuevo_estado
                estado_contador += 1
                i += 1
            else:
                estado_actual = automata[estado_actual][simbolo]
                i += 1

        if 'final' not in automata[estado_actual]:
            automata[estado_actual]['final'] = True

    # Añadiendo las transiciones para detectar inicios repentinos de otras palabras
    for estado in automata:
        for simbolo in set(''.join(palabras)):
            if simbolo not in automata[estado]:
                # ¿Es el símbolo el inicio de alguna palabra?
                for palabra in palabras:
                    if palabra.startswith(simbolo):
                        automata[estado][simbolo] = automata[estado_inicial][simbolo]
                        break
                else:
                    automata[estado][simbolo] = estado_inicial

    simbolos = set(''.join(palabras))
    return automata, simbolos



def generar_csv(automata, simbolos):
    with open('vaBien.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Escribir la fila de los símbolos de entrada
        writer.writerow([''] + list(simbolos) + ['final'])

        # Escribir las filas de estados y transiciones
        for estado, transiciones in automata.items():
            row = [estado]
            for simbolo in simbolos:
                row.append(transiciones.get(simbolo, ''))
            if 'final' in transiciones:
                row.append('1')
            else:
                row.append('0')
            writer.writerow(row)

if __name__ == "__main__":
    palabras = ["auto","break","case","char","const","continue","default","do","double","else","enum","extern","float","for","goto","if","int","long","register","return","short","signed","sizeof","static","struct","switch","typedef","union","unsigned","void","volatile","while"]

    automata, simbolos = generar_automata(palabras)
    generar_csv(automata, simbolos)

    print("Tabla de estados y transiciones generada en 'automata.csv'")