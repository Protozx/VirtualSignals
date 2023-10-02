import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os


def escrbir_csv(nombre_archivo, encabezado_x, encabezado_y, eje_x, eje_y):
    # Crear y escribir los datos en el archivo CSV
    #ruta_completa = os.path.join("/home/rodrigo/Documentos/5toSemestre/Senales/prac3/zarate/static/data/", nombre_archivo)
    ruta_completa = os.path.join("static/data/", nombre_archivo)
    with open(ruta_completa, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        # Escribir encabezados (opcional)
        escritor_csv.writerow([encabezado_x, encabezado_y])
        
        # Escribir los datos de t y u_shifted en el archivo CSV
        for x, y in zip(eje_x, eje_y):
            escritor_csv.writerow([x, y])


def leer_csv(nombre_archivo, encabezado_x, encabezado_y):
    datos = pd.read_csv(nombre_archivo)

    return datos[encabezado_x].values, datos[encabezado_y].values


def definir_par_impar(y, nombre_arc, encabezado_x,encabezado_y, x):
    par = 0.5 * (y + np.flip(y))
    impar = 0.5 * (y - np.flip(y))
    ambas = par + impar
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x, par )
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x, impar)

def definir_par(y, nombre_arc, encabezado_x,encabezado_y, x):
    par = 0.5 * (y + np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,par)

def definir_impar(y, nombre_arc, encabezado_x,encabezado_y, x):
    impar = 0.5 * (y - np.flip(y))
    escrbir_csv(f"{nombre_arc}", encabezado_x, encabezado_y, x,impar)


def generar_grafica(amplitud, frecuencia, muestration, u_desplaz, periodo, sigma, omega, frec_angular, angulo_fase, par, continuidad, tipo, id):
    if(tipo == "1"):
        # >> Escalón unitario continua, simple y desplazada"""
        if(continuidad == "0" and periodo == 1):
            print("Escalon SC")
            x = u_desplaz
            t = np.linspace(-2*(2* (u_desplaz+1)), 2*(2* (u_desplaz+1)), muestration)
            t_shifted = t - x
            muestration = muestration
            u_shifted = np.where(t_shifted >= 0, amplitud, 0)
            if(par == "0"):
                escrbir_csv(id +".csv", "x", "y", t, u_shifted)
            elif(par == "1"):
                definir_par(u_shifted, id +".csv", "x", "y", t)
            elif(par == "2"):
                definir_impar(u_shifted, id +".csv", "x", "y", t)
            else:
                print("urias")
        
        elif continuidad == "0" and periodo > 1:
            print("Escalon PC")
            A = amplitud  # Amplitud
            n_periods = periodo  # Número de períodos (cambiar según lo desees)


            # Frecuencia en Hertz (Hz), calculada en base al número de períodos
            f = frecuencia

            # Período de la señal periódica
            T = 1 / f

            # Crear un arreglo de tiempo que cubra el rango que desees
            t = np.linspace(0, n_periods * T, muestration)

            # Crear la señal escalón unitario periódica
            u_periodic = np.where((t % T) < (0.5 * T), A, 0)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", t)

        elif(continuidad == "1" and periodo == 1):
            muestration = muestration / 10
            print("Escalon SD")
            n = np.arange(-5*(2*(u_desplaz+1)), 5*(2*(u_desplaz+1)))  # Valores discretos desde -5 hasta 5

            # Desplazar la señal en 2 unidades hacia la derecha
            n_shifted = n -u_desplaz  # Cambia el valor según la cantidad de unidades de desplazamiento

            # Crear la señal escalón unitario discreta desplazada
            u_shifted_discrete = np.where(n_shifted >= 0, amplitud, 0)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n_shifted, u_shifted_discrete)
            elif (par == "1"):
                definir_par(u_shifted_discrete, id + ".csv", "x", "y", n_shifted)
            elif (par == "2"):
                definir_impar(u_shifted_discrete, id + ".csv", "x", "y", n_shifted)

        elif(continuidad == "1"):    
            print("Escalon PD")
            A = amplitud  # Amplitud de los escalones
            n_periods = periodo  # Número de períodos (cambiar según lo desees)
            n_samples_in_high = muestration//3  # Número de muestras en alto seguidas de n muestras en bajo (cambiar según lo desees)

            # Frecuencia en Hertz (Hz), calculada en base al número de períodos
            f = frecuencia

            # Período de la señal periódica
            T = 1 / f

            # Crear un arreglo de tiempo discreto que cubra el rango que desees
            n = np.arange(0, n_periods * n_samples_in_high * 2)  # Valores discretos desde 0 hasta (n_periods * n_samples_in_high * 2 - 1)

            # Crear la señal escalón unitario discreta periódica con n muestras en alto seguidas de n muestras en bajo
            u_periodic = np.tile([A] * n_samples_in_high + [0] * n_samples_in_high, n_periods)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", n)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", n)          

    elif(tipo == "2"):
        
        if continuidad== "0" and periodo == 1:
            print("Tipo dos simple")
        
            desplazada = u_desplaz

            # Coordenadas del impulso unitario
            x = [i for i in range(-1*(desplazada+1)*100, (desplazada+2)*100)]

            # Ahora, ajustamos los valores dividiendo por 100 para obtener el paso de 0.01
            x = [valor / 100.0 for valor in x]
            y = [amplitud*100 if i == (desplazada)*100 else 0 for i in range(-(desplazada+1)*100, (desplazada+2)*100, 1)]
            y = [valor / 100.0 for valor in y]
            x = np.array(x)
            y = np.array(y)
            
            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", x, y)
            elif (par == "1"):
                definir_par(y, id + ".csv", "x", "y", x)
            elif (par == "2"):
                definir_impar(y, id + ".csv", "x", "y", x)    

        elif continuidad =="0":
            print("Tipo dos periodico")
            A = amplitud # Amplitud de los escalones
            n_periods = periodo//10  # Número de períodos (cambiar según lo desees)
            samples_per_step = muestration*100  # Número de muestras por cada paso (cambiar según lo desees)

            # Frecuencia en Hertz (Hz), calculada en base al número de períodos
            f = frecuencia

            # Período de la señal periódica
            T = 1 / f

            # Crear un arreglo de tiempo discreto que cubra el rango que desees
            n = np.arange(0, n_periods * (samples_per_step*muestration))  # Valores discretos desde 0 hasta (n_periods * samples_per_step - 1)

            # Crear la señal escalón unitario discreto periódica con más muestras en alto
            u_periodic = np.where((n % (samples_per_step * muestration)) == 0, A, 0)


            # Crear la gráfica
            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", n)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", n)   

        elif continuidad == "1" and periodo == 1:

            print("Tipo dos discreto y period")
            desplazada = u_desplaz

            # Coordenadas del impulso unitario
            x = [i for i in range(-(desplazada+1)*1, (desplazada+2)*1, 1)]

            # Ahora, ajustamos los valores dividiendo por 100 para obtener el paso de 0.01
            x = [valor / 1 for valor in x]
            y = [amplitud*1 if i == (desplazada)*1 else 0 for i in range(-(desplazada+1)*1, (desplazada+2)*1, 1)]
            y = [valor / 1 for valor in y]


            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", x, y)
            elif (par == "1"):
                definir_par(y, id + ".csv", "x", "y", x)
            elif (par == "2"):
                definir_impar(y, id + ".csv", "x", "y", x)  

        else:
            #Escalon unitario discreta simple y con desplazamiento"""
            #print(f"Sospechoso, periodos = {periodo}, continuidad = {continuidad}")
            

            # Parámetros para la señal periódica
            A = amplitud  # Amplitud de los escalones
            n_periods = periodo  # Número de períodos (cambiar según lo desees)
            samples_per_step = muestration//10  # Número de muestras por cada paso (cambiar según lo desees)

            # Frecuencia en Hertz (Hz), calculada en base al número de períodos
            f = frecuencia

            # Período de la señal periódica
            T = 1 / f

            # Crear un arreglo de tiempo discreto que cubra el rango que desees
            n = np.arange(0, n_periods * samples_per_step)  # Valores discretos desde 0 hasta (n_periods * samples_per_step - 1)

            # Crear la señal escalón unitario discreto periódica con más muestras en alto
            u_periodic = np.where((n % samples_per_step) == 0, A, 0)


            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", n)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", n)  


    elif(tipo == "3"):
        if continuidad == "0" and periodo == 1:

            # Crear un conjunto de valores de t
            # Desplazar la señal hacia la derecha en 1 unidad
            n = u_desplaz
            t = np.linspace(-2*(2* (n+1)), 2*(2*(n+1)), muestration)  # Desde -2 hasta 2 con 400 puntos
            t_desplazado_derecha = t - n


            

            # Ajustar la amplitud de la función rampa
            A = amplitud  # Cambia este valor a la amplitud deseada
            u_desplazado_amplitud = A * np.maximum(0, t_desplazado_derecha)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_desplazado_amplitud)
            elif (par == "1"):
                definir_par(u_desplazado_amplitud, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_desplazado_amplitud, id + ".csv", "x", "y", t)  

        elif continuidad == "0":
            n = periodo  # Número de periodos
            f = frecuencia  # Frecuencia (periodos por unidad de tiempo)
            a = amplitud  # Amplitu
            # Crear un conjunto de valores de tiempo
            t = np.linspace(0, n / f, muestration)  # De 0 a n/f, con 1000 puntos por período

            # Calcular la señal diente de sierra
            rampa = a * (t * f - np.floor(t * f))
            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, rampa)
            elif (par == "1"):
                    definir_par(rampa, id + ".csv", "x", "y", t)
            elif (par == "2"):
                    definir_impar(rampa, id + ".csv", "x", "y", t) 

        elif continuidad == "1" and periodo == 1:

            # Desplazar la señal hacia la derecha en 1 unidad
            n = u_desplaz
            # Crear un conjunto de valores de t
            t = np.linspace(-2*( 2*(n+1)), 2*(2*(n+1)), muestration)  # Desde -2 hasta 2 con 400 puntos
            t_desplazado_derecha = t - n

            # Ajustar la amplitud de la función rampa
            A = amplitud  # Cambia este valor a la amplitud deseada
            u_desplazado_amplitud = A * np.maximum(0, t_desplazado_derecha)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_desplazado_amplitud)
            elif (par == "1"):
                definir_par(u_desplazado_amplitud, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_desplazado_amplitud, id + ".csv", "x", "y", t)  


        elif continuidad == "1":
            n = periodo  # Número de periodos
            f = frecuencia  # Frecuencia (periodos por unidad de tiempo)
            a = amplitud  # Amplitud

            # Crear un conjunto de valores de tiempo
            t = np.linspace(0, n / f, (n*muestration))  # De 0 a n/f, con 1000 puntos por período

            # Calcular la señal diente de sierra
            rampa = a * (t * f - np.floor(t * f))

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, rampa)
            elif (par == "1"):
                definir_par(rampa, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(rampa, id + ".csv", "x", "y", t)  


    elif(tipo == "4"):
        if continuidad == "0":
            senal = lambda s,t: np.exp(s*t)
            #sigma = amplitud/100  # s = 0 +0j
            #omega = frecuencia/10

            a  = -5 # intervalo de tiempo [a,b)
            b  = 5
            #muestration = 0.1
            muestration = 1/muestration*10

            # PROCEDIMIENTO
            ti = np.arange(a, b, muestration)
            s_i = complex(sigma,omega)
            senal_i = senal(s_i,ti)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", ti, np.real(senal_i))
            elif (par == "1"):
                definir_par(np.real(senal_i), id + ".csv", "x", "y", ti)
            elif (par == "2"):
                definir_impar(np.real(senal_i), id + ".csv", "x", "y", ti)  
        #escrbir_csv("ExpoComplejalC.csv", "Tiempo", "Senoidal", ti, np.imag(senal_i))

            
            #definir_par_impar(np.imag(senal_i), "ExpolRealC.csv", "Tiempo", "Senoidal", ti)

        elif continuidad == "1":

            senal = lambda s,t: np.exp(s*t)
            #sigma = amplitud/100  # s = 0 +0j
            #omega = frecuencia/10

            a  = -5 # intervalo de tiempo [a,b)
            b  = 5
            muestration = 1/muestration*10

            # PROCEDIMIENTO
            ti = np.arange(a, b, muestration)
            s_i = complex(sigma,omega)
            senal_i = senal(s_i,ti)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", ti, np.real(senal_i))
            elif (par == "1"):
                definir_par(np.real(senal_i), id + ".csv", "x", "y", ti)
            elif (par == "2"):
                definir_impar(np.real(senal_i), id + ".csv", "x", "y", ti)  

 
    elif(tipo == "5"):
        if continuidad == "0":
            senal = lambda s,t: np.exp(s*t)
            #sigma = amplitud/100  # s = 0 +0j
            #omega = frecuencia/10

            a  = -5 # intervalo de tiempo [a,b)
            b  = 5
            muestration = 1/muestration*10

            # PROCEDIMIENTO
            ti = np.arange(a, b, muestration)
            s_i = complex(sigma,omega)
            senal_i = senal(s_i,ti)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", ti, np.imag(senal_i))
            elif (par == "1"):
                definir_par(np.imag(senal_i), id + ".csv", "x", "y", ti)
            elif (par == "2"):
                definir_impar(np.imag(senal_i), id + ".csv", "x", "y", ti)  
        #escrbir_csv("ExpoComplejalC.csv", "Tiempo", "Senoidal", ti, np.imag(senal_i))

            
            #definir_par_impar(np.imag(senal_i), "ExpolRealC.csv", "Tiempo", "Senoidal", ti)

        elif continuidad == "1":

            senal = lambda s,t: np.exp(s*t)
            #sigma = amplitud/100  # s = 0 +0j
            #omega = frecuencia/10

            a  = -5 # intervalo de tiempo [a,b)
            b  = 5
            muestration = 1/muestration*10

            # PROCEDIMIENTO
            ti = np.arange(a, b, muestration)
            s_i = complex(sigma,omega)
            senal_i = senal(s_i,ti)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", ti, np.imag(senal_i))
            elif (par == "1"):
                definir_par(np.imag(senal_i), id + ".csv", "x", "y", ti)
            elif (par == "2"):
                definir_impar(np.imag(senal_i), id + ".csv", "x", "y", ti)  

    elif(tipo == "6"):
        print("Senoidal")
        if continuidad == "0":
            A = amplitud            # Amplitud
            w0 = frec_angular      # Frecuencia angular (en radianes por segundo)
            theta = angulo_fase         # Fase inicial

            muestration = muestration

            # Crear un arreglo de tiempo
            t = np.linspace(0, 2 * np.pi, muestration)  # Genera 1000 puntos entre 0 y 2*pi

            # Calcular la señal senoidal
            x = A * np.cos(w0 * t + theta)
            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, x)
            elif (par == "1"):
                definir_par(x, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(x, id + ".csv", "x", "y", t)

        elif continuidad == "1":
            A = amplitud            # Amplitud$("#cc" + id).removeClass("d-none");
            w0 = frec_angular      # Frecuencia angular (en radianes por segundo)
            theta = angulo_fase          # Fase inicial

            muestration = muestration//2

            # Crear un arreglo de tiempo
            t = np.linspace(0, 2 * np.pi, muestration)  # Genera 1000 puntos entre 0 y 2*pi

            # Calcular la señal senoidal
            x = A * np.cos(w0 * t + theta)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, x)
            elif (par == "1"):
                definir_par(x, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(x, id + ".csv", "x", "y", t)
 

    return tipo