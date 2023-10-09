import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os


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
            A = amplitud
            n_periods = periodo 

            f = frecuencia

            T = 1000 / f

            t = np.linspace(0, n_periods * T, muestration)

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
            n = np.arange(-5*(2*(u_desplaz+1)), 5*(2*(u_desplaz+1)))

            n = n.astype(int)
            n = np.unique(n)


            n_shifted = n -u_desplaz  

            u_shifted_discrete = np.where(n_shifted >= 0, amplitud, 0)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n_shifted, u_shifted_discrete)
            elif (par == "1"):
                definir_par(u_shifted_discrete, id + ".csv", "x", "y", n_shifted)
            elif (par == "2"):
                definir_impar(u_shifted_discrete, id + ".csv", "x", "y", n_shifted)

        elif(continuidad == "1"):    
            """A = amplitud 
            n_periods = periodo  
            n_samples_in_high = muestration//3 

            f = frecuencia

            T = 1 / f

            n = np.arange(0, n_periods * n_samples_in_high * 2) 

            u_periodic = np.tile([A] * n_samples_in_high + [0] * n_samples_in_high, n_periods)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", n, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", n)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", n) """  

            A = amplitud
            n_periods = periodo 

            f = frecuencia

            T = 1000 / f

            t = np.linspace(0, n_periods * T, muestration)

            t = t.astype(int)
            t = np.unique(t)

            u_periodic = np.where((t % T) < (0.5 * T), A, 0)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_periodic)
            elif (par == "1"):
                definir_par(u_periodic, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_periodic, id + ".csv", "x", "y", t)       

    elif(tipo == "2"):
        
        if continuidad== "0" and periodo == 1:
            print("Tipo dos simple")
        
            desplazada = u_desplaz

            x = [i for i in range(-1*(desplazada+1)*100, (desplazada+2)*100)]

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
            """A = amplitud 
            n_periods = periodo
            samples_per_step = muestration 

            f = frecuencia

            T = 1 / f

            n = np.arange(0, n_periods * (samples_per_step)//2) 

            samples_per_impulse = int(samples_per_step / f)

            u_periodic = np.where((n % T) == 0, A, 0)"""

            periodo_s = 1/frecuencia  # Periodo del tren de impulsos
            duración = periodo_s * periodo  # Duración total de la señal
            n_impulsos = periodo  # Número de impulsos en el tren (puedes modificar esto)
            print(n_impulsos)

            # Crear un vector de tiempo
            t = np.linspace(0, duración, muestration)

            # Crear el tren de impulsos
            impulsos = np.zeros(len(t))
            for i in range(0, len(t), muestration // n_impulsos):
                impulsos[i] = amplitud



            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, impulsos)
            elif (par == "1"):
                definir_par(impulsos, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(impulsos, id + ".csv", "x", "y", t)   

        elif continuidad == "1" and periodo == 1:

            print("Tipo dos discreto y period")
            desplazada = u_desplaz

            x = [i for i in range(-(desplazada+1)*1, (desplazada+2)*1, 1)]

            x = [valor / 1 for valor in x]
            y = [amplitud*1 if i == (desplazada)*1 else 0 for i in range(-(desplazada+1)*1, (desplazada+2)*1, 1)]
            y = [valor / 1 for valor in y]

            x = x.astype(int)
            x = np.unique(x)


            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", x, y)
            elif (par == "1"):
                definir_par(y, id + ".csv", "x", "y", x)
            elif (par == "2"):
                definir_impar(y, id + ".csv", "x", "y", x)  

        else:
            #Escalon unitario discreta simple y con desplazamiento"""

            periodo_s = 1/frecuencia  # Periodo del tren de impulsos
            duración = periodo_s * periodo  # Duración total de la señal
            n_impulsos = periodo  # Número de impulsos en el tren (puedes modificar esto)
            print(n_impulsos)

            # Crear un vector de tiempo
            t = np.linspace(0, duración, muestration)

            # Crear el tren de impulsos
            impulsos = np.zeros(len(t))
            for i in range(0, len(t), muestration // n_impulsos):
                impulsos[i] = amplitud

            t = t.astype(int)
            t = np.unique(t)



            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, impulsos)
            elif (par == "1"):
                definir_par(impulsos, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(impulsos, id + ".csv", "x", "y", t)    


    elif(tipo == "3"):
        if continuidad == "0" and periodo == 1:

            n = u_desplaz
            t = np.linspace(-2*(2* (n+1)), 2*(2*(n+1)), muestration)
            t_desplazado_derecha = t - n

            A = amplitud
            u_desplazado_amplitud = A * np.maximum(0, t_desplazado_derecha)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_desplazado_amplitud)
            elif (par == "1"):
                definir_par(u_desplazado_amplitud, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_desplazado_amplitud, id + ".csv", "x", "y", t)  


        elif continuidad == "0":
            n = periodo 
            f = (1/frecuencia) * 200
            a = amplitud 

            t = np.linspace(0, n * f, muestration * n)

            rampa = amplitud * ((2 * np.pi / f * t) % (2 * np.pi) - np.pi) / np.pi


            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, rampa)
            elif (par == "1"):
                    definir_par(rampa, id + ".csv", "x", "y", t)
            elif (par == "2"):
                    definir_impar(rampa, id + ".csv", "x", "y", t) 

        elif continuidad == "1" and periodo == 1:


            n = u_desplaz

            t = np.linspace(-2*( 2*(n+1)), 2*(2*(n+1)), muestration)  
            t_desplazado_derecha = t - n

            A = amplitud 
            u_desplazado_amplitud = A * np.maximum(0, t_desplazado_derecha)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, u_desplazado_amplitud)
            elif (par == "1"):
                definir_par(u_desplazado_amplitud, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(u_desplazado_amplitud, id + ".csv", "x", "y", t)  


        elif continuidad == "1":
            n = periodo 
            f = (1/frecuencia) * 200
            a = amplitud 

            t = np.linspace(0, n * f, muestration * n)

            t = t.astype(int)
            t = np.unique(t)

            rampa = amplitud * ((2 * np.pi / f * t) % (2 * np.pi) - np.pi) / np.pi

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, rampa)
            elif (par == "1"):
                definir_par(rampa, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(rampa, id + ".csv", "x", "y", t)  


    elif(tipo == "4"):
        if continuidad == "0":
            senal = lambda s,t: np.exp(s*t)

            a  = -20 
            b  = 20
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


        elif continuidad == "1":

            senal = lambda s,t: np.exp(s*t)

            a  = -20 
            b  = 20
            muestration = 1/muestration*10

            # PROCEDIMIENTO
            ti = np.arange(a, b, muestration)

            ti = ti.astype(int)
            ti = np.unique(ti)
            
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
            a  = -20 
            b  = 20
            muestration = 1/muestration*10


            ti = np.arange(a, b, muestration)
            s_i = complex(sigma,omega)
            senal_i = senal(s_i,ti)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", ti, np.imag(senal_i))
            elif (par == "1"):
                definir_par(np.imag(senal_i), id + ".csv", "x", "y", ti)
            elif (par == "2"):
                definir_impar(np.imag(senal_i), id + ".csv", "x", "y", ti)  


        elif continuidad == "1":

            senal = lambda s,t: np.exp(s*t)


            a  = -20 
            b  = 20
            muestration = 1/muestration*10

            ti = np.arange(a, b, muestration)

            ti = ti.astype(int)
            ti = np.unique(ti)

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
            A = amplitud       
            w0 = frec_angular    
            theta = angulo_fase     

            muestration = muestration

            t = np.linspace(0, 2 * np.pi, muestration)

            x = A * np.cos(w0 * t + theta)
            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, x)
            elif (par == "1"):
                definir_par(x, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(x, id + ".csv", "x", "y", t)

        elif continuidad == "1":
            A = amplitud        
            w0 = frec_angular    
            theta = angulo_fase 

            muestration = muestration//2

            t = np.linspace(0, 2 * np.pi, muestration) 

            t = t.astype(int)
            t = np.unique(t)

            x = A * np.cos(w0 * t + theta)

            if (par == "0"):
                escrbir_csv(id + ".csv", "x", "y", t, x)
            elif (par == "1"):
                definir_par(x, id + ".csv", "x", "y", t)
            elif (par == "2"):
                definir_impar(x, id + ".csv", "x", "y", t)
 
    return tipo