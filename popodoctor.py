import csv

def divide_palabras(palabras):
    segmentos = {}
    for palabra1 in palabras:
        for palabra2 in palabras:
            if palabra1 != palabra2:
                i = 0
                while i < len(palabra1):
                    seg = palabra1[i:]
                    if palabra2.startswith(seg):
                        if seg not in segmentos:
                            segmentos[seg] = []
                        segmentos[seg].append(palabra2)
                    i += 1
    return segmentos

def generar_automata(palabras):
    segmentos = divide_palabras(palabras)
    automata = {}
    estado_inicial = 'q0'
    automata[estado_inicial] = {}
    estado_contador = 1

    for palabra in palabras:
        estado_actual = estado_inicial
        for i, simbolo in enumerate(palabra):
            if simbolo not in automata[estado_actual]:
                nuevo_estado = 'q' + str(estado_contador)
                automata[estado_actual][simbolo] = nuevo_estado
                if nuevo_estado not in automata:
                    automata[nuevo_estado] = {}
                estado_actual = nuevo_estado
                estado_contador += 1
            else:
                estado_actual = automata[estado_actual][simbolo]
            # Verificar si hay palabras que comienzan con los caracteres restantes
            restante = palabra[i+1:]
            for seg, p_list in segmentos.items():
                if restante.startswith(seg):
                    for p in p_list:
                        if p[0] not in automata[estado_actual]:
                            automata[estado_actual][p[0]] = automata[estado_inicial][p[0]]

        automata[estado_actual]['final'] = True

    simbolos = set(''.join(palabras))
    return automata, simbolos

def generar_csv(automata, simbolos):
    with open('vamal.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + list(simbolos) + ['final'])
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
    palabras = ["break", "else"]
    automata, simbolos = generar_automata(palabras)
    generar_csv(automata, simbolos)
    print("Tabla de estados y transiciones generada en 'automata.csv'")
