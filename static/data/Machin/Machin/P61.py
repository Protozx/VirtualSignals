import pandas as pd
from hmmlearn import hmm
from sklearn.model_selection import train_test_split
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

def main():
    data, label_encoder = cargar_datos_markov('dataset.csv')
    X_train, X_test, y_train, y_test = separar_datos_markov(data)
    hmms = entrenar_markov(X_train, y_train)
    predictions = clasificar_markov(X_test, hmms)
    accuracy = evaluar_markov(predictions, y_test)
    print(f'Precisión: {accuracy}')

if __name__ == "__main__":
    main()
