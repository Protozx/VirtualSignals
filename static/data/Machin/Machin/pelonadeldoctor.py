import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer


def cargar_y_preprocesar_datos(nombre_archivo_csv):
    df = pd.read_csv(nombre_archivo_csv)

    X = df.iloc[:, :-1] 
    y = df.iloc[:, -1] 

    X = X.apply(pd.to_numeric, errors='coerce')

    imputador = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_imputado = imputador.fit_transform(X)

    escalador = StandardScaler()
    X_escalado = escalador.fit_transform(X_imputado)

    codificador_etiquetas = LabelEncoder()
    y_codificado = codificador_etiquetas.fit_transform(y.astype(str))

    return X_escalado, y_codificado

def realizar_validacion_cruzada(X, y, model, k=5, random_seed=1):
    np.random.seed(random_seed)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    
    tams_folds = np.full(k, len(X) // k, dtype=int)
    tams_folds[:len(X) % k] += 1
    aux = 0
    eficiencias = []

    for tams_fold in tams_folds:
        start, end = aux, aux + tams_fold
        val_indices = indices[start:end]
        train_indices = np.delete(indices, np.arange(start, end))
        
        X_train, X_val = X[train_indices], X[val_indices]
        y_train, y_val = y[train_indices], y[val_indices]
        
        model.fit(X_train, y_train)
        score = model.score(X_val, y_val)
        eficiencias.append(score)
        aux = end

    return eficiencias


def main(nombre_archivo_csv):
    X_escalado, y = cargar_y_preprocesar_datos(nombre_archivo_csv)

    knn = KNeighborsClassifier(n_neighbors=5)
    bayes_clasifier = GaussianNB()
    svm_gaussiano = SVC(kernel='rbf')
    regresion_logistica = LogisticRegression(max_iter=1000)

    modelos = [knn, bayes_clasifier, svm_gaussiano, regresion_logistica]
    nombres_modelos = ['k-NN', 'Clasificador Bayesiano', 'SVM Gaussiano', 'Regresión Logística']

    for modelo, nombre in zip(modelos, nombres_modelos):
        puntuaciones_cv = realizar_validacion_cruzada(X_escalado, y, modelo, k=5)
        print(f"{nombre} Precisión: {np.mean(puntuaciones_cv):.2f}")

if __name__ == "__main__":
    print("\t\t\t ***PRÁCTICA <<VALIDACIÓN CRUZADA>>***")
    nombre_archivo_csv = input("Ingrese el nombre del archivo CSV: ")
    main(nombre_archivo_csv)
