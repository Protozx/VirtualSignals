import pandas as pd
from hmmlearn import hmm
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import LabelEncoder

def cargar_datos_markov(filename):
    columns = ['Time', 'X', 'Y', 'Z', 'R', 'Theta', 'label']
    data = pd.read_csv(filename, header=None, names=columns)
    label_encoder = LabelEncoder()
    data['label'] = label_encoder.fit_transform(data['label'])
    return data, label_encoder

def separar_datos_markov(data):
    X = data[['Time', 'X', 'Y', 'Z', 'R', 'Theta']]
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

if __name__ == "__main__":
    print(f'Precisión promedio con validación cruzada K-Fold: {puntaje_markov("dataset.csv")}')