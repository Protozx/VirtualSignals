import numpy as np
import pandas as pd

def leer_datos(archivo):
    return pd.read_csv(archivo)

def correlacion_cruzada(df_factA, df_factB, max_lag):
    x = df_factA['amplitud'].values
    y = df_factB['amplitud'].values

    max_lag = min(max_lag, len(x), len(y))

    for l in range(-max_lag, max_lag + 1):
        r_xy = 0

        for n in range(len(x)):
            if 0 <= n - l < len(y):
                r_xy += x[n] * y[n - l]
        print(f"l = {l}: secuencia = {r_xy}")

archivo_A = "doctor.csv"
archivo_B = "uri.csv"
max_lag = 6

df_factA = leer_datos(archivo_A)
df_factB = leer_datos(archivo_B)

correlacion_cruzada(df_factA, df_factB, max_lag)
