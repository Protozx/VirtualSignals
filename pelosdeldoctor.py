import csv
from graphics import *
import numpy as np

def graficar_automata_graphics(filename):
    win = GraphWin('Automata', 600, 600)
    win.setBackground('white')
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        
        # Obtener la lista de estados a partir del encabezado
        estados = next(reader)
        estados = estados[:-1]
        
        # Calcular posiciones para los nodos
        num_estados = len(estados)
        radio_circulo = 250
        centro = Point(300, 300)
        posiciones = {}
        for i, estado in enumerate(estados):
            angulo = 2 * 3.14159 * i / num_estados
            x = centro.getX() + radio_circulo * np.cos(angulo)
            y = centro.getY() + radio_circulo * np.sin(angulo)
            posiciones[estado] = Point(x, y)
            print(f"Agregando estado {estado} con posición {x, y}")  # Agregar print de diagnóstico
            
            # Dibujar el nodo
            circulo = Circle(posiciones[estado], 20)
            circulo.setFill('lightblue')
            circulo.draw(win)
            label = Text(posiciones[estado], estado)
            label.draw(win)
        
        # Procesar las filas del CSV para dibujar aristas
        for row in reader:
            estado_actual = row[0]
            for i, destino in enumerate(row[1:-1]):
                if destino != "0":
                    try:
                        linea = Line(posiciones[estado_actual], posiciones[destino])
                    except KeyError as e:
                        print(f"Error al tratar de acceder al estado {e} en el diccionario de posiciones.")
                        print("Asegúrate de que este estado esté presente en el encabezado del CSV.")
                        return  # Salir de la función
                    linea.setArrow("last")
                    linea.draw(win)
                    # Dibujar etiqueta en medio de la línea
                    mid_x = (posiciones[estado_actual].getX() + posiciones[destino].getX()) / 2
                    mid_y = (posiciones[estado_actual].getY() + posiciones[destino].getY()) / 2
                    label = Text(Point(mid_x, mid_y), estados[i + 1])
                    label.draw(win)
                    
    win.getMouse()  # Esperar hasta que se haga click para cerrar
    win.close()

# Usar la función para graficar el autómata
graficar_automata_graphics('vaBien.csv')
