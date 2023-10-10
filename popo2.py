import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
from scipy.integrate import cumtrapz


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


def normalizar_datos(paquete_A, paquete_B):
    id_senalA, amplitudA, periodoA, muestrationA, desplazamientoA, inicioA, finA, sigmaA, omegaA, frec_angularA, angulo_faseA, es_discretaA, paridadA = paquete_A
    id_senalB, amplitudB, periodoB, muestrationB, desplazamientoB, inicioB, finB, sigmaB, omegaB, frec_angularB, angulo_faseB, es_discretaB, paridadB = paquete_B

    inicio, fin = hallar_intervalos(inicioA, inicioB, finA, finB)

    x_A, y_A = generar_señal(id_senalA, amplitudA, periodoA, muestrationA, desplazamientoA, inicio, fin, sigmaA, omegaA, frec_angularA, angulo_faseA, es_discretaA, paridadA)
    x_B, y_B = generar_señal(id_senalB, amplitudB, periodoB, muestrationB, desplazamientoB, inicio, fin, sigmaB, omegaB, frec_angularB, angulo_faseB, es_discretaB, paridadB)

    df_A = pd.DataFrame({'XA': x_A, 'YA': y_A})
    df_B = pd.DataFrame({'XB': x_B, 'YB': y_B})
    df_A = filtrar_mayores_fin(df_A, finA)
    df_B = filtrar_mayores_fin(df_B, finB)
    df_A = filtrar_menores_inicio(df_A, finA)
    df_B = filtrar_menores_inicio(df_B, finB)
    return df_A, df_B


def sumar_senales(paquete_sumandoA, paquete_sumandoB):
    df_sA, df_sB = normalizar_datos(paquete_sumandoA, paquete_sumandoB)
    df_suma = df_sA[['x']].copy()
    df_suma['y'] = df_sA['y'] + df_sB['y']

    return df_suma["x"].values, df_suma["y"].values


def restar_senales(paquete_minuendo, paquete_sustraendo):
    df_minuendo, df_sustraendo = normalizar_datos(paquete_minuendo, paquete_sustraendo)
    df_resta = df_minuendo[['x']].copy()
    df_resta['y'] = df_minuendo['y'] - df_sustraendo['y']
    return df_resta["x"].values, df_resta["y"].values


def multiplicar_senales(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)
    df_producto = df_factA[['x']].copy()
    df_producto['y'] = df_factA['y'] * df_factB['y']
    return df_producto["x"].values, df_producto["y"].values


def derivar(x, y):
    dx = np.diff(x)
    dy = np.diff(y)

    derivada = dy / dx

    x_derivada = x[:-1] 
    return x_derivada, derivada


def integrar(x, y):
    integral = cumtrapz(y, x, initial=0)
    return x, integral


def escalamiento_amplitud(x, y, cte):
    y = cte*y
    return x, y


def escalamiento_tiempo(x, y, cte, es_discreto):
    cte_buena = 1/cte
    x = cte_buena*x

    if es_discreto:
        df = pd.DataFrame({'x': x, 'y': y})
        df = df[df['x'] % 1 == 0]
        x = df["x"].values
        y = df["y"].values
    return x, y


def reflejar(x, y):
    x = -1 * x
    return x, y


def desplazamiento(x, y, cte):
    x = x - cte
    return x, y

def suavizar_señal_con_filtro_del_1(x, y, alfa):
    señal_suavizada = np.zeros_like(y)
    señal_suavizada[0] = y[0]

    for i in range(1, len(y)):
        señal_suavizada[i] = alfa * y[i] + (1 - alfa) * señal_suavizada[i - 1]

    return x, y, señal_suavizada


def escrbir_csv(nombre_archivo, encabezado_x, encabezado_y, eje_x, eje_y):

    ruta_completa = os.path.join("static/data/", nombre_archivo)
    with open(ruta_completa, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        escritor_csv.writerow([encabezado_x, encabezado_y])

        for x, y in zip(eje_x, eje_y):
            escritor_csv.writerow([x, y])


def leer_csv(nombre_archivo, encabezado_x, encabezado_y):
    datos = pd.read_csv(nombre_archivo)
    return datos[encabezado_x].values, datos[encabezado_y].values


def escribir_par(x, y, nombre_arc, encabezado_x,encabezado_y, ):
    par = 0.5 * (y + np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,par)


def escribir_impar(y, nombre_arc, encabezado_x,encabezado_y, x):
    impar = 0.5 * (y - np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,impar)


def escribir_señal(id, paridad, x, y):
    if paridad == "0":
        escrbir_csv(id +".csv", "x", "y", x, y)
    elif paridad == "1":
        escribir_par(y, id +".csv", "x", "y", x)
    elif paridad == "2":
        escribir_impar(y, id +".csv", "x", "y", x)


def generar_cuadrada(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):
    
    t = np.linspace(inicio, fin, muestration, endpoint=False)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = fin - inicio

    cuadrada = np.zeros(muestration)

    for i in range(muestration):
        t_actual = t[i]
        posicion_rel = (t_actual - desplazamiento) % periodo
        if posicion_rel < periodo / 2:
            cuadrada[i] = amplitud
        else:
            cuadrada[i] = 0.0
    
    return t, cuadrada


def generar_tren_impulsos(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):
    tiempo = np.linspace(inicio, fin, muestration)

    if es_discreta:
        tiempo = tiempo.astype(int)
        tiempo = np.unique(tiempo)
        muestration = fin - inicio

    señal = np.zeros_like(tiempo)

    intervalo = (fin - inicio) / muestration

    valor_impulso = amplitud

    for i in range(muestration):
        t = tiempo[i]
        if (t - desplazamiento) % periodo < intervalo:
            señal[i] = valor_impulso
    
    return tiempo, señal



def generar_dientes_sierra(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin, muestration, endpoint=False)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = fin - inicio

    dientes_sierra = np.zeros(muestration)

    for i in range(muestration):
        t_actual = t[i]
        posicion_rel = (t_actual - desplazamiento) % periodo
        dientes_sierra[i] = (2 * amplitud / periodo) * (posicion_rel - periodo / 2)
    
    return t, dientes_sierra


def generar_triangular(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):


    t = np.linspace(inicio, fin, muestration, endpoint=False)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = fin - inicio

    triangular = np.zeros(muestration)

    for i in range(muestration):
        t_actual = t[i]
        posicion_rel = (t_actual - desplazamiento) % periodo

        if posicion_rel < periodo / 2:
            triangular[i] = (4 * amplitud / periodo) * posicion_rel - amplitud
        else:
            triangular[i] = (-4 * amplitud / periodo) * posicion_rel + 3 * amplitud
    
    return t, triangular


def generar_botar_pelota(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):
    
    t = np.linspace(inicio, fin, muestration, endpoint=False)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = fin - inicio

    pelota = np.zeros(muestration)

    for i in range(muestration):
        t_actual = t[i]
        posicion_rel = (t_actual - desplazamiento) % periodo
        pelota[i] = amplitud * abs(np.sin((2 * np.pi / periodo) * posicion_rel))
        
    return t, pelota


def generar_escalon_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin, muestration)
    
    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)

    escalon = np.zeros(len(t))

    for i in range(len(t)):
        t_actual = t[i]
 
        if t_actual >= desplazamiento:
            escalon[i] = amplitud
    
    return t, escalon


def generar_impulso_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin , muestration)
    
    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = fin - inicio


    impulso = np.zeros(len(t))
    
    impulso[int((desplazamiento-inicio)*muestration/(fin-inicio))] = amplitud
    
    return t, impulso


def generar_impulso_triangular(amplitud, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin, muestration)
    
    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)

    impulso_triang = np.zeros(len(t))

    for i in range(len(t)):
        t_actual = t[i]
        posicion_rel = t_actual - desplazamiento

        if abs(posicion_rel) <= amplitud / 2:
            impulso_triang[i] = 1 - 2 * abs(posicion_rel) / amplitud
        else:
            impulso_triang[i] = 0
    
    return t, impulso_triang


def generar_rampa(amplitud, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin, muestration)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
    
    signal = np.zeros(len(t))
    
    for i in range(len(t)):
        t_actual = t[i]
        posicion_rel = t_actual - desplazamiento

        if posicion_rel >= 0:
            signal[i] = amplitud * posicion_rel
    
    return t, signal

def generar_exponencial(muestration, inicio, fin, sigma, omega, es_discreta, id_senal):

    senal = lambda s,t: np.exp(s*t)
    inicio  = -20 
    fin  = 20

    # PROCEDIMIENTO
    ti = np.linspace(inicio, fin, muestration)

    if es_discreta:
        ti = ti.astype(int)
        ti = np.unique(ti)

    s_i = complex(sigma,omega)
    senal_i = senal(s_i,ti)

    if id_senal == "10":
        return ti, np.real(senal_i)
    else:
        return ti, np.imag(senal_i)
    

def generar_senoidal(amplitud, frec_angular, angulo_fase, muestration, inicio, fin, es_discreta):
    t = np.linspace(inicio, fin, muestration)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
    seno = amplitud * np.cos(frec_angular * t + angulo_fase)

    return t, seno


def generar_señal(id_señal, tipo, amplitud, periodo, muestration, desplazamiento, inicio, fin, sigma, omega, frec_angular, angulo_fase, es_discreta, paridad):

    if tipo == "1":
        x, y = generar_cuadrada(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(id_señal, paridad, x, y)

    elif tipo == "2":
        x,y = generar_tren_impulsos(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "3":
        x,y = generar_dientes_sierra(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "4":
        x,y = generar_triangular(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "5":
        x,y = generar_botar_pelota(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "6":
        x, y = generar_escalon_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "7":
        x, y = generar_impulso_unitario(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "8":
        x, y = generar_impulso_triangular(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "9":
        x, y = generar_rampa(amplitud, muestration, desplazamiento, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)

    elif tipo == "10" or "11":
        x, y = generar_exponencial(muestration, inicio, fin, sigma, omega, es_discreta, tipo)
        escribir_señal(tipo, paridad, x, y)
    
    elif tipo == "12":
        x, y = generar_senoidal(amplitud, frec_angular, angulo_fase, muestration, inicio, fin, es_discreta)
        escribir_señal(tipo, paridad, x, y)
    return x, y