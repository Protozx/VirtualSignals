
def generar_exponencial(muestration, inicio, fin, sigma, omega, es_discreta, id_senal):

    senal = lambda s,t: np.exp(s*t)

    # PROCEDIMIENTO
    ti = np.linspace(inicio, fin, muestration)

    if es_discreta:
        ti = ti.astype(int)
        ti = np.unique(ti)
        muestration = int(fin) - int(inicio)

    s_i = complex(sigma,omega)
    senal_i = senal(s_i,ti)

    if id_senal == "4":
        return ti, np.real(senal_i)
    else:
        return ti, np.imag(senal_i)
    

def generar_senoidal(amplitud, frec_angular, angulo_fase, muestration, inicio, fin, es_discreta):
    t = np.linspace(inicio, fin, muestration)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = int(fin) - int(inicio)
    seno = amplitud * np.cos(frec_angular * t + angulo_fase)

    return t, seno


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



def operar_senales(paquete_A, paquete_B, operacion, id_operacion):
    if operacion == "suma":
        x,y= sumar_senales(paquete_A, paquete_B)
    elif operacion == "resta":
        x,y= restar_senales(paquete_A, paquete_B)
    elif operacion == "multiplicacion":
        x,y= multiplicar_senales(paquete_A, paquete_B)
    elif operacion == "convolucion1":
        x,y= convolucionar_senales(paquete_A, paquete_B)
    elif operacion == "convolucion2":
        x,y= convolucionar_senales_manualmente(paquete_A, paquete_B)
    escrbir_csv(str(id_operacion) +".csv", "x", "y", x, y)



def convolucionar_senales_manualmente(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)

    y_A = df_factA['y'].values
    y_B = df_factB['y'].values

    len_A = len(y_A)
    len_B = len(y_B)
    len_conv = len_A + len_B - 1
    y_conv = np.zeros(len_conv)

    for i in range(len_conv):
        for j in range(len_B):
            if i - j >= 0 and i - j < len_A:
                y_conv[i] += y_A[i - j] * y_B[j]

    x_conv = np.linspace(0, len_conv - 1, len_conv)

    return x_conv, y_conv


def filtrar_menores_inicio(df, inicio):
    df.loc[df['x'] <= inicio, 'y'] = 0
    return df


def filtrar_mayores_fin(df, fin):
    df.loc[df['x'] >= fin, 'y'] = 0
    return df


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



import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
from scipy.integrate import cumtrapz
from scipy.signal import convolve


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