import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.base import clone
from sklearn.pipeline import Pipeline

def cargar_datos(ruta_csv):
    data = pd.read_csv(ruta_csv, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y

def k_fold_cross_validation(X, y, k, modelo):
    fold_size = len(X) // k
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    scores = []

    for fold in range(k):
        test_indices = indices[fold * fold_size : (fold + 1) * fold_size]
        train_indices = np.setdiff1d(indices, test_indices)


        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]


        modelo_clonado = clone(modelo)
        modelo_clonado.fit(X_train, y_train)
        
        
        y_pred = modelo_clonado.predict(X_test)
        score = accuracy_score(y_test, y_pred)
        scores.append(score)

    return scores

def evaluar_con_kfold_manual(X, y, k=5):
    modelos = {
        'KNN': Pipeline([('scaler', StandardScaler()), ('classifier', KNeighborsClassifier(n_neighbors=5))]),
        'Regresión Logística': Pipeline([('scaler', StandardScaler()), ('classifier', LogisticRegression(random_state=42))]),
        'SVM': Pipeline([('scaler', StandardScaler()), ('classifier', SVC(kernel='linear', random_state=42))]),
        'Bayesiano': Pipeline([('scaler', StandardScaler()), ('classifier', GaussianNB())])
    }

    resultados = dict()

    for nombre, modelo in modelos.items():
        scores = k_fold_cross_validation(X, y, k, modelo)
        resultados[nombre] = scores
        print(f"{nombre}: {np.mean(scores)} (+/- {np.std(scores)})")
    mejor_modelo = max(resultados, key=lambda nombre: np.mean(resultados[nombre]))
    print(f"\nEl mejor modelo es {mejor_modelo} con una precisión de {np.mean(resultados[mejor_modelo])}.")

def main(ruta_csv):
    X, y = cargar_datos(ruta_csv)
    evaluar_con_kfold_manual(X, y)

if __name__ == "__main__":
    main("dataset.csv")
