import csv
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

class CascadeLogisticRegression:
    def __init__(self):
        self.clf_dh = LogisticRegression(learning_rate=0.01, n_iterations=1000)
        self.clf_sl = LogisticRegression(learning_rate=0.01, n_iterations=1000)

    def fit(self, X, y):
        y_dh = np.where(y == 'DH', 1, 0)
        self.clf_dh.fit(X, y_dh)
        mask = y != 'DH'
        X_sl = X[mask]
        y_sl = np.where(y[mask] == 'SL', 1, 0)
        self.clf_sl.fit(X_sl, y_sl)

    def predict(self, X):
        preds = []

        dh_predictions = self.clf_dh.predict(X)
        sl_predictions = self.clf_sl.predict(X)

        for idx, (dh_pred, sl_pred) in enumerate(zip(dh_predictions, sl_predictions)):
            if dh_pred == 1:
                label = 'DH'
            elif sl_pred == 1:
                label = 'SL'
            else:
                label = 'NO'
            preds.append(label)
            print(f"Data {idx+1}: {X.iloc[idx].values} -> Predicted label: {label}")


        return np.array(preds)

    def get_weights(self):
        return {
            "clf_dh_weights": self.clf_dh.weights,
            "clf_dh_bias": self.clf_dh.bias,
            "clf_sl_weights": self.clf_sl.weights,
            "clf_sl_bias": self.clf_sl.bias
        }

class LogisticRegression:
    def __init__(self, learning_rate=0.001, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        for _ in range(self.n_iterations):
            model = np.dot(X, self.weights) + self.bias
            predictions = self._sigmoid(model)
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        model = np.dot(X, self.weights) + self.bias
        predictions = self._sigmoid(model)
        y_pred = [1 if i > 0.5 else 0 for i in predictions]
        return np.array(y_pred)

def dat_to_csv(dat_filename, csv_filename):
    with open(dat_filename, 'r') as dat_file:
        lines = dat_file.readlines()
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in lines:
                data = line.split()[:]
                writer.writerow(data)
                
def csv_datos(nombre_archivo):
    datos = []
    with open(nombre_archivo, newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=',')
        for fila in lector_csv:
            datos.append(','.join(fila))
    
    csv_data = '\n'.join(datos)
    return csv_data

def process_csv(data: str):
    from io import StringIO
    data_io = StringIO(data)
    df = pd.read_csv(data_io, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test
dat_filename = 'datata.dat'
csv_filename = 'dataset.csv'
dat_to_csv(dat_filename, csv_filename)
X_train, X_test, y_train, y_test = process_csv(csv_datos('dataset.csv'))
clf_cascade = CascadeLogisticRegression()
clf_cascade.fit(X_train, y_train)
weights_info = clf_cascade.get_weights()
print(weights_info)

y_pred = clf_cascade.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")
