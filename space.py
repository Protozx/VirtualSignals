import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
from scipy.integrate import cumtrapz


def generar_grafica(id,tipo, amplitud, periodo, muestration, desplazamiento, inicio, fin, sigma, omega, frec_angular, angulo_fase, paridad, es_discreta):
    print("--------------------------")
    print(f"tipo={tipo}, type(tipo)={type(tipo)}")
    if tipo == "8":
        print("8")
        x, y = generar_cuadrada(amplitud, periodo, muestration, desplazamiento, inicio, fin, int(es_discreta))
        escribir_señal(id, paridad, x, y)

    elif tipo == "9":
        print("9")
        x,y = generar_tren_impulsos(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "10":
        print("10")
        x,y = generar_dientes_sierra(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "11":
        print("11")
        x,y = generar_triangular(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "12":
        print("12")
        x,y = generar_botar_pelota(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "1":
        print("1")
        print("Cayó escalón")
        x, y = generar_escalon_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "2":
        print("2")
        x, y = generar_impulso_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "13":
        print("13")
        x, y = generar_impulso_triangular(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "3":
        print("3")
        x, y = generar_rampa(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)

    elif tipo == "4" or tipo ==  "5":
        print("4o5")
        x, y = generar_exponencial(muestration, inicio, fin, sigma, omega, es_discreta, tipo)
        escribir_señal(id, paridad, x, y)
    
    elif tipo == "6":
        print("6")
        x, y = generar_senoidal(amplitud, frec_angular, angulo_fase, muestration, inicio, fin, es_discreta)
        escribir_señal(id, paridad, x, y)
    
    else:
        print("Cayo caso 1000")
        x, y = leer_csv(f"static/data/{id}.csv", "x", "y")

    return x, y



def normalizar_datos(paquete_A, paquete_B):
    id_senalA, tipoA, amplitudA, periodoA, muestrationA, desplazamientoA, inicioA, finA, sigmaA, omegaA, frec_angularA, angulo_faseA, es_discretaA, paridadA = paquete_A
    id_senalB, tipoB,  amplitudB, periodoB, muestrationB, desplazamientoB, inicioB, finB, sigmaB, omegaB, frec_angularB, angulo_faseB, es_discretaB, paridadB = paquete_B

    print(f"tipos normA = {tipoA}")
    print(f"tipos normB = {tipoB}")

    inicio, fin = hallar_intervalos(inicioA, inicioB, finA, finB)



    x_A, y_A = generar_grafica(id_senalA, tipoA, amplitudA, periodoA, muestrationA, desplazamientoA, inicio, fin, sigmaA, omegaA, frec_angularA, angulo_faseA, es_discretaA, paridadA)
    x_B, y_B = generar_grafica(id_senalB, tipoB, amplitudB, periodoB, muestrationA, desplazamientoB, inicio, fin, sigmaB, omegaB, frec_angularB, angulo_faseB, es_discretaB, paridadB)

    df_A = pd.DataFrame({'x': x_A, 'y': y_A})
    df_B = pd.DataFrame({'x': x_B, 'y': y_B})

    print("-----------------")
    print("Data A")
    print(df_A)
    print("-----------------")
    print("Data B")
    print(df_B)

    df_A = filtrar_mayores_fin(df_A, finA)
    df_B = filtrar_mayores_fin(df_B, finB)
    df_A = filtrar_menores_inicio(df_A, inicioA)
    df_B = filtrar_menores_inicio(df_B, inicioB)
    return df_A, df_B


def multiplicar_senales(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)
    df_producto = df_factA[['x']].copy()
    df_producto['y'] = df_factA['y'] * df_factB['y']
    return df_producto["x"].values, df_producto["y"].values


def hallar_intervalos(inicio_A, inicio_B, fin_A, fin_B):
    if inicio_A < inicio_B:
        minimo = inicio_A
    else:
        minimo = inicio_B

    if fin_A > fin_B:
        maximo = fin_A
    else:
        maximo = fin_B
    return minimo, maximo


def filtrar_menores_inicio(df, inicio):
    df.loc[df['x'] <= inicio, 'y'] = 0
    return df


def filtrar_mayores_fin(df, fin):
    df.loc[df['x'] >= fin, 'y'] = 0
    return df
