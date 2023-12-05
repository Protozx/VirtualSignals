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


def convolucionar_senales(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)
    y_conv = convolve(df_factA['y'], df_factB['y'], mode='full')
    n = len(y_conv)

    x_inicio = df_factA['x'].iloc[0] + df_factB['x'].iloc[0]
    x_final = df_factA['x'].iloc[-1] + df_factB['x'].iloc[-1]

    x_conv = np.linspace(x_inicio, x_final, n)

    return x_conv, y_conv


def convoluciona_senales_manualmente(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)

    y_A = df_factA['y'].values
    y_B = df_factB['y'].values

    len_A = len(y_A)
    len_B = len(y_B)
    len_conv = len_A + len_B - 1
    y_conv = np.zeros(len_conv)

    for i in range(len_conv-1):
        for j in range(len_B-1):
            if i + j >= 0 and i + j < len_conv:
                y_conv[i+j] += y_A[i] * y_B[j]

    x_inicio = df_factA['x'].iloc[0] + df_factB['x'].iloc[0]
    x_final = df_factA['x'].iloc[-1] + df_factB['x'].iloc[-1]
    x_conv = np.linspace(x_inicio, x_final, len_conv)

    return x_conv, y_conv


def correlacionar_senales_manualmente(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)

    y_A = df_factA['y'].values
    y_B = df_factB['y'].values

    len_A = len(y_A)
    len_B = len(y_B)
    len_corr = len_A + len_B - 1
    y_corr = np.zeros(len_corr)

    for i in range(len_corr):
        for j in range(len_B):
            if (i - j) >= 0 and (i - j) < len_A:
                y_corr[i] += y_A[i - j] * y_B[j]

    x_inicio = df_factA['x'].iloc[0] + df_factB['x'].iloc[0]
    x_final = df_factA['x'].iloc[-1] + df_factB['x'].iloc[-1]

    x_corr = np.linspace(x_inicio, x_final, len_corr)

    return x_corr, y_corr



def correlacionar_senales(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)

    y_A = df_factA['y'].values
    y_B = df_factB['y'].values

    # Realiza la correlación usando numpy
    y_corr = np.correlate(y_A, y_B, mode='full')

    # Calcula el rango de x
    x_inicio = df_factA['x'].iloc[0] + df_factB['x'].iloc[0]
    x_final = df_factA['x'].iloc[-1] + df_factB['x'].iloc[-1]
    len_corr = len(y_corr)
    x_corr = np.linspace(x_inicio, x_final, len_corr)

    return x_corr, y_corr




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
    elif operacion == "correlacion1":
        x,y= correlacionar_senales(paquete_A, paquete_B)
    elif operacion == "correlacion2":
        x,y= correlacionar_senales_manualmente(paquete_A, paquete_B)
    escrbir_csv(str(id_operacion) +".csv", "x", "y", x, y)


def sumar_senales(paquete_sumandoA, paquete_sumandoB):
    df_sA, df_sB = normalizar_datos(paquete_sumandoA, paquete_sumandoB)
    df_suma = df_sA[['x']].copy()
    df_suma['y'] = df_sA['y'] + df_sB['y']
    print(df_sA)
    print("-----------------------")
    print("Sumando")
    print(df_sB)

    return df_suma["x"].values, df_suma["y"].values


def restar_senales(paquete_minuendo, paquete_sustraendo):
    df_minuendo, df_sustraendo = normalizar_datos(paquete_minuendo, paquete_sustraendo)
    df_resta = df_minuendo[['x']].copy()
    df_resta['y'] = df_minuendo['y'] - df_sustraendo['y']
    print("-----------------------")
    print("Resta")
    print(df_resta)
    return df_resta["x"].values, df_resta["y"].values


def multiplicar_senales(paquete_factA, paquete_factB):
    df_factA, df_factB = normalizar_datos(paquete_factA, paquete_factB)
    df_producto = df_factA[['x']].copy()
    df_producto['y'] = df_factA['y'] * df_factB['y']
    return df_producto["x"].values, df_producto["y"].values


def derivar_fx(x, y):
    dx = np.diff(x)
    dy = np.diff(y)

    derivada = dy / dx

    x_derivada = x[:-1] 
    return x_derivada, derivada


def integrar_fx(x, y):
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

def filtro_del_1(x, y, alfa):
    print(alfa)
    señal_suavizada = np.zeros_like(y)
    señal_suavizada[0] = float(y[0])

    for i in range(1, len(y)):
        señal_suavizada[i] = alfa * float(y[i]) + (1 - alfa) * float(señal_suavizada[i - 1])

    return x, señal_suavizada


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
    print(y)
    par = 0.5 * (y + np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,par)


def escribir_impar(y, nombre_arc, encabezado_x,encabezado_y, x):
    impar = 0.5 * (y - np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,impar)


def escribir_señal(id, paridad, x, y):
    if paridad == "0":
        escrbir_csv(str(id) +".csv", "x", "y", x, y)
    elif paridad == "1":
        escribir_par(x, y, str(id) +".csv", "x", "y")
    elif paridad == "2":
        escribir_impar(y, str(id) +".csv", "x", "y", x)


def generar_cuadrada(amplitud, periodo, muestration, desplazamiento, inicio, fin, es_discreta):
    
    t = np.linspace(inicio, fin, muestration, endpoint=False)

    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = int(fin) - int(inicio)

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
        t = t.astype(int)
        t = np.unique(t)
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)


    impulso = np.zeros(len(t))
    
    impulso[int((desplazamiento-inicio)*muestration/(fin-inicio))] = amplitud
    
    return t, impulso


def generar_impulso_triangular(amplitud, muestration, desplazamiento, inicio, fin, es_discreta):

    t = np.linspace(inicio, fin, muestration)
    
    if es_discreta:
        t = t.astype(int)
        t = np.unique(t)
        muestration = int(fin) - int(inicio)

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
        muestration = int(fin) - int(inicio)
    
    signal = np.zeros(len(t))
    
    for i in range(len(t)):
        t_actual = t[i]
        posicion_rel = t_actual - desplazamiento

        if posicion_rel >= 0:
            signal[i] = amplitud * posicion_rel
    
    return t, signal

def generar_exponencial(muestration, inicio, fin, sigma, omega, es_discreta, id_senal):

    senal = lambda s,t: np.exp(s*t)

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

    x_inicio = df_factA['x'].iloc[0] + df_factB['x'].iloc[0]
    x_final = df_factA['x'].iloc[-1] + df_factB['x'].iloc[-1]

    x_conv = np.linspace(x_inicio, x_final, len_conv)

    return x_conv, y_conv
