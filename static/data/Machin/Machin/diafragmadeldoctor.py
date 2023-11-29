# Importamos las bibliotecas necesarias
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Definimos una función para cargar y preprocesar los datos
def cargar_y_preprocesar_datos(nombre_archivo_csv):
    # Leemos el archivo CSV
    df = pd.read_csv(nombre_archivo_csv)
    
    # Separamos las características (X) y la etiqueta (y)
    X = df.iloc[:, :-1]  # Todas las columnas excepto la última
    y = df.iloc[:, -1]   # Última columna

    # Convertimos los valores no numéricos a NaN y luego los imputamos
    X = X.apply(pd.to_numeric, errors='coerce')

    # Imputamos los valores faltantes con la media
    imputador = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_imputado = imputador.fit_transform(X)

    # Escalamos las características para que tengan media 0 y desviación estándar 1
    escalador = StandardScaler()
    X_escalado = escalador.fit_transform(X_imputado)

    # Codificamos las etiquetas a valores numéricos
    codificador_etiquetas = LabelEncoder()
    y_codificado = codificador_etiquetas.fit_transform(y.astype(str))

    return X_escalado, y_codificado

# Definimos la función principal del script
def main(nombre_archivo_csv):
    # Preprocesamos los datos
    X_escalado, y = cargar_y_preprocesar_datos(nombre_archivo_csv)

    # Inicializamos los modelos
    knn = KNeighborsClassifier(n_neighbors=5)
    bayes_ingenuo = GaussianNB()
    svm_gaussiano = SVC(kernel='rbf')
    regresion_logistica = LogisticRegression(max_iter=1000)

    # Configuramos la validación cruzada
    kf = KFold(n_splits=5, shuffle=True, random_state=1)

    # Creamos una lista con los modelos y otra con los nombres de los modelos
    modelos = [knn, bayes_ingenuo, svm_gaussiano, regresion_logistica]
    nombres_modelos = ['k-NN', 'Bayes Ingenuo', 'SVM Gaussiano', 'Regresión Logística']

    # Evaluamos cada modelo utilizando validación cruzada
    for modelo, nombre in zip(modelos, nombres_modelos):
        puntuaciones_cv = cross_val_score(modelo, X_escalado, y, cv=kf)
        print(f"{nombre} Precisión: {puntuaciones_cv.mean():.2f} (+/- {puntuaciones_cv.std() * 2:.2f})")

# Verificamos si el script es el punto de entrada principal
if __name__ == "__main__":
    # Solicitamos al usuario el nombre del archivo CSV
    nombre_archivo_csv = input("Ingrese el nombre del archivo CSV: ")
    main(nombre_archivo_csv)
