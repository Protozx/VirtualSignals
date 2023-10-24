import csv
import networkx as nx
import matplotlib.pyplot as plt

def graficar_automata(filename):
    G = nx.DiGraph()
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        
        # Obtener la lista de estados a partir del encabezado
        estados = next(reader)
        # Eliminar la columna final que no representa un estado
        estados = estados[:-1]
        
        # Procesar las filas del CSV para añadir aristas al grafo
        for row in reader:
            estado_actual = row[0]
            
            for i, destino in enumerate(row[1:-1]):
                if destino != "0":
                    G.add_edge(estado_actual, destino, label=estados[i + 1])
    
    # Graficar el autómata
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=20, font_size=6)
    
    # Añadir las etiquetas de las transiciones
    edge_labels = {(u, v): G[u][v]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    
    plt.show()

# Usar la función para graficar el autómata
graficar_automata('celula.csv')
