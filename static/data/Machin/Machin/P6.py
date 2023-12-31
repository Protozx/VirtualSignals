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
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, KFold

def cargar_datos(ruta_csv):
    data = pd.read_csv(ruta_csv, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y

def cargar_datos_markov(filename):
    columns = ['', '', '', '', '', '', '']
    data = pd.read_csv(filename, header=None, names=columns)
    label_encoder = LabelEncoder()
    data['label'] = label_encoder.fit_transform(data['label'])
    return data, label_encoder


def separar_datos_markov(data):
    X = data[['', '', '', '', '', '']]
    y = data['label']
    return train_test_split(X, y, test_size=0.3, random_state=42)

def entrenar_markov(X_train, y_train):
    hmms = {}
    for label in y_train.unique():
        model = hmm.GaussianHMM(n_components=4, covariance_type="diag", n_iter=100)
        model.fit(X_train[y_train == label])
        hmms[label] = model
    return hmms

def clasificar_markov(X_test, hmms) -> list:
    predictions = []
    for index, row in X_test.iterrows():
        max_score = float('-inf')
        best_label = None
        for label, model in hmms.items():
            score = model.score(row.to_frame().T)
            if score > max_score:
                max_score = score
                best_label = label
        predictions.append(best_label)
    return predictions

def evaluar_markov(predictions, y_test):
    return sum(predictions == y_test) / len(y_test)

def validacion_cruzada_kfold(data, k):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    scores = []

    for train_index, test_index in kf.split(data):
        X_train, X_test = data.iloc[train_index], data.iloc[test_index]
        y_train, y_test = X_train['label'], X_test['label']
        X_train = X_train.drop('label', axis=1)
        X_test = X_test.drop('label', axis=1)

        hmms = entrenar_markov(X_train, y_train)
        predictions = clasificar_markov(X_test, hmms)
        score = evaluar_markov(predictions, y_test)
        scores.append(score)

    return sum(scores) / len(scores)

def puntaje_markov(archivo):
    data, label_encoder = cargar_datos_markov(archivo)
    accuracy_promedio = validacion_cruzada_kfold(data, 5)
    return accuracy_promedio

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
        'Maquina de soporte vectorial': Pipeline([('scaler', StandardScaler()), ('classifier', SVC(kernel='linear', random_state=42))]),
        'Clasificador Bayesiano': Pipeline([('scaler', StandardScaler()), ('classifier', GaussianNB())])
    }

    resultados = dict()
    resultados['Cadenas ocultas de markov'] =  puntaje_markov('dataset.csv')
    print(f"\n\nCadenas ocultas de markov: {resultados['Cadenas ocultas de markov']}")
    
    for nombre, modelo in modelos.items():
        scores = k_fold_cross_validation(X, y, k, modelo)
        resultados[nombre] = scores
        print(f"{nombre}: {np.mean(scores)}")
    mejor_modelo = max(resultados, key=lambda nombre: np.mean(resultados[nombre]))
    
    print(f"\nEl mejor modelo es {mejor_modelo} con una precisión de {np.mean(resultados[mejor_modelo])}.")




def main(ruta_csv):
    X, y = cargar_datos(ruta_csv)
    evaluar_con_kfold_manual(X, y)

if __name__ == "__main__":
    main("dataset.csv")
