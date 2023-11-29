import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.decomposition import PCA

def cargar_datos(ruta_csv):
    data = pd.read_csv(ruta_csv, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y

def k_fold_cross_validation(X, y, k, modelo):
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scores = []

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        modelo_clonado = clone(modelo)
        modelo_clonado.fit(X_train, y_train)

        y_pred = modelo_clonado.predict(X_test)
        score = accuracy_score(y_test, y_pred)
        scores.append(score)

    return scores

def generar_poblacion_inicial(num_caracteristicas, tam_poblacion=10):
    return np.random.randint(2, size=(tam_poblacion, num_caracteristicas))

def reproducir(individuos):
    nuevos_individuos = []
    for _ in range(10): 
        padres = np.random.choice(len(individuos), 2, replace=False)
        punto_cruce = np.random.randint(1, len(individuos[0]))
        hijo1 = np.concatenate([individuos[padres[0]][:punto_cruce], individuos[padres[1]][punto_cruce:]])
        hijo2 = np.concatenate([individuos[padres[1]][:punto_cruce], individuos[padres[0]][punto_cruce:]])
        nuevos_individuos.extend([hijo1, hijo2])
    return nuevos_individuos

def mutar(individuos, prob_mutacion=0.1):
    for individuo in individuos:
        for i in range(len(individuo)):
            if np.random.rand() < prob_mutacion:
                individuo[i] = 1 - individuo[i]
    return individuos

def evaluar_individuos(X, y, individuos, k=5, modelo=LogisticRegression()):
    puntuaciones = []
    for individuo in individuos:
        if np.sum(individuo) == 0:
            puntuaciones.append(0)
            continue

        caracteristicas_seleccionadas = X[:, individuo.astype(bool)]
        pipeline = Pipeline([('scaler', StandardScaler()), ('classifier', modelo)])
        scores = k_fold_cross_validation(caracteristicas_seleccionadas, y, k, pipeline)
        puntuaciones.append(np.mean(scores))
    return puntuaciones

def seleccionar_mejores(individuos, puntuaciones, num_seleccionados=10):
    indices = np.argsort(puntuaciones)[-num_seleccionados:]
    return [individuos[i] for i in indices]


def comparar_modelos(X, y, caracteristicas_importantes, modelo=LogisticRegression()):
    pipeline_completo = Pipeline([('scaler', StandardScaler()), ('classifier', modelo)])
    scores_completo = k_fold_cross_validation(X, y, 5, pipeline_completo)

    X_reducido = X[:, caracteristicas_importantes]
    pipeline_reducido = Pipeline([('scaler', StandardScaler()), ('classifier', modelo)])
    scores_reducido = k_fold_cross_validation(X_reducido, y, 5, pipeline_reducido)

    print(f"Efectividad promedio usando todas las características: {np.mean(scores_completo):.2f}")
    print(f"Efectividad promedio usando características seleccionadas: {np.mean(scores_reducido):.2f}")

def aplicar_pca_y_comparar(X, y, num_componentes, modelo=LogisticRegression()):
    pca = PCA(n_components=num_componentes)
    X_pca = pca.fit_transform(X)

    pipeline_pca = Pipeline([('scaler', StandardScaler()), ('classifier', modelo)])
    scores_pca = k_fold_cross_validation(X_pca, y, 5, pipeline_pca)

    print(f"Efectividad promedio usando PCA con {num_componentes} componentes: {np.mean(scores_pca):.2f}")

    return scores_pca

def main(ruta_csv, num_generaciones=10, num_componentes_pca=4):
    X, y = cargar_datos(ruta_csv)
    num_caracteristicas = X.shape[1]
    poblacion = generar_poblacion_inicial(num_caracteristicas)

    for _ in range(num_generaciones):
        descendientes = reproducir(poblacion)
        descendientes_mutados = mutar(descendientes)
        copia_poblacion = mutar(poblacion.copy())
        poblacion_total = np.vstack((poblacion, copia_poblacion, descendientes_mutados))
        puntuaciones = evaluar_individuos(X, y, poblacion_total)
        poblacion = seleccionar_mejores(poblacion_total, puntuaciones)

    mejor_individuo = poblacion[0]
    caracteristicas_importantes = np.where(mejor_individuo == 1)[0]
    print("Características importantes:", caracteristicas_importantes)

    comparar_modelos(X, y, caracteristicas_importantes)
    scores_pca = aplicar_pca_y_comparar(X, y, num_componentes_pca)

if __name__ == "__main__":
    main("dataset.csv")
