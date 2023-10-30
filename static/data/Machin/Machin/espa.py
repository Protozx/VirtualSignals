import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

class RegresionLogisticaCascada:
    def __init__(self):
        self.clasificador_dh = RegresionLogistica(tasa_aprendizaje=0.01, num_iteraciones=1000)
        self.clasificador_sl = RegresionLogistica(tasa_aprendizaje=0.01, num_iteraciones=1000)

    def entrenar(self, X, y):
        y_dh = np.where(y == 'DH', 1, 0)
        self.clasificador_dh.entrenar(X, y_dh)
        mascara = y != 'DH'
        X_sl = X[mascara]
        y_sl = np.where(y[mascara] == 'SL', 1, 0)
        self.clasificador_sl.entrenar(X_sl, y_sl)

    def predecir(self, X):
        predicciones = []

        predicciones_dh = self.clasificador_dh.predecir(X)
        predicciones_sl = self.clasificador_sl.predecir(X)

        for idx, (prediccion_dh, prediccion_sl) in enumerate(zip(predicciones_dh, predicciones_sl)):
            if prediccion_dh == 1:
                etiqueta = 'DH'
            elif prediccion_sl == 1:
                etiqueta = 'SL'
            else:
                etiqueta = 'NO'
            predicciones.append(etiqueta)
            print(f"Dato {idx+1}: {X.iloc[idx].values} -> Etiqueta predicha: {etiqueta}")

        return np.array(predicciones)

    def obtener_pesos(self):
        return {
            "pesos_clasificador_dh": self.clasificador_dh.pesos,
            "sesgo_clasificador_dh": self.clasificador_dh.sesgo,
            "pesos_clasificador_sl": self.clasificador_sl.pesos,
            "sesgo_clasificador_sl": self.clasificador_sl.sesgo
        }
        
    def graficar_modelo(self, X, y):
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        for etiqueta, color in [('DH', 'red'), ('SL', 'blue'), ('NO', 'green')]:
            mascara = y == etiqueta
            ax.scatter(X_pca[mascara][:, 0], X_pca[mascara][:, 1], X_pca[mascara][:, 2], c=color, label=etiqueta, depthshade=True)

        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_zlabel('Principal Component 3')
        ax.legend()
        ax.set_title('Modelo de Regresión Logística en Cascada (3D PCA)')
        plt.show()


class RegresionLogistica:
    def __init__(self, tasa_aprendizaje=0.001, num_iteraciones=1000):
        self.tasa_aprendizaje = tasa_aprendizaje
        self.num_iteraciones = num_iteraciones
        self.pesos = None
        self.sesgo = None

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def entrenar(self, X, y):
        num_muestras, num_caracteristicas = X.shape
        self.pesos = np.zeros(num_caracteristicas)
        self.sesgo = 0
        for _ in range(self.num_iteraciones):
            modelo = np.dot(X, self.pesos) + self.sesgo
            predicciones = self._sigmoid(modelo)
            dw = (1 / num_muestras) * np.dot(X.T, (predicciones - y))
            db = (1 / num_muestras) * np.sum(predicciones - y)
            self.pesos -= self.tasa_aprendizaje * dw
            self.sesgo -= self.tasa_aprendizaje * db

    def predecir(self, X):
        modelo = np.dot(X, self.pesos) + self.sesgo
        predicciones = self._sigmoid(modelo)
        y_pred = [1 if i > 0.5 else 0 for i in predicciones]
        return np.array(y_pred)

def dat_a_csv(nombre_archivo_dat, nombre_archivo_csv):
    with open(nombre_archivo_dat, 'r') as archivo_dat:
        lineas = archivo_dat.readlines()
        with open(nombre_archivo_csv, 'w', newline='') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=',')
            for linea in lineas:
                datos = linea.split()[:]
                escritor.writerow(datos)

def csv_a_datos(nombre_archivo):
    datos = []
    with open(nombre_archivo, newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=',')
        for fila in lector_csv:
            datos.append(','.join(fila))

    datos_csv = '\n'.join(datos)
    return datos_csv

def procesar_csv(datos: str):
    from io import StringIO
    datos_io = StringIO(datos)
    df = pd.read_csv(datos_io, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_entrenamiento, X_prueba, y_entrenamiento, y_prueba

nombre_archivo_dat = 'datata.dat'
nombre_archivo_csv = 'conjunto.csv'
dat_a_csv(nombre_archivo_dat, nombre_archivo_csv)
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = procesar_csv(csv_a_datos('conjunto.csv'))
clasificador_cascada = RegresionLogisticaCascada()
clasificador_cascada.entrenar(X_entrenamiento, y_entrenamiento)
info_pesos = clasificador_cascada.obtener_pesos()
print(info_pesos)

y_predicha = clasificador_cascada.predecir(X_prueba)
precision = np.mean(y_predicha == y_prueba)
print(f"Precisión: {precision * 100:.2f}%")
clasificador_cascada.graficar_modelo(X_entrenamiento, y_entrenamiento)
