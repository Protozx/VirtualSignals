import numpy as np
import matplotlib.pyplot as plt
import csv
import os



def paso1(secs,mz,num):
    
    def señal_original(t):
        return np.sin(4 * np.pi * t) + np.sin(8 * np.pi * t)
    
    def interpolacion(t, t_muestreo, x_muestreada):
        x_interp = np.zeros_like(t)
        for n, x_n in enumerate(x_muestreada):
            g = np.sin(np.pi * mz * (t - t_muestreo[n])) / (np.pi * mz * (t - t_muestreo[n]))
            x_interp += x_n * g
        return x_interp
    
    
    Ts = 1/mz  # 10Hz

    # Crear un array de valores de tiempo t para 2 segundos
    t_muestreo = np.linspace(0, secs, int(secs/Ts))
    t_fino = np.linspace(0, secs, int(500*int(secs)))

    # Muestrear la señal
    x_muestreada = señal_original(t_muestreo)

    # Interpolación
    x_interp = interpolacion(t_fino, t_muestreo, x_muestreada)

    # Graficar
    #plt.figure(figsize=(12, 6))
    
    #plt.stem(t_muestreo, x_muestreada, 'r', markerfmt='ro', basefmt=" ", linefmt='r', use_line_collection=True, label="Muestras")
    escrbir_csv(str(num) +"a.csv", "x", "y", t_muestreo, x_muestreada)
    
    #plt.plot(t_fino, x_interp, 'b', label="Interpolada")
    escrbir_csv(str(num) +"b.csv", "x", "y", t_fino, x_interp)
    
    #plt.plot(t_fino, señal_original(t_fino), 'g--', label="Señal Original")
    escrbir_csv(str(num) +"c.csv", "x", "y", t_fino, señal_original(t_fino))
    
    #plt.legend()
    #plt.title('Muestreo de x(t) a 10Hz')

    #plt.tight_layout()
    #plt.show()

def paso2(secs,og_mz,mue_mz,num):
    
    def señal_original(t):
        return np.sin(2 * np.pi * og_mz * t)

    def interpolacion(t, t_muestreo, x_muestreada):
        x_interp = np.zeros_like(t)
        for n, x_n in enumerate(x_muestreada):
            g = np.sin(np.pi * mue_mz * (t - t_muestreo[n])) / (np.pi * mue_mz * (t - t_muestreo[n]))
            x_interp += x_n * g
        return x_interp
    
    
    Ts = 1/mue_mz  # 10Hz

    # Crear un array de valores de tiempo t para 2 segundos
    t_muestreo = np.linspace(0, secs, int(secs*mue_mz))
    t_fino = np.linspace(0, secs, int(1000*(int(secs)+1)))

    # Muestrear la señal
    x_muestreada = señal_original(t_muestreo)

    # Interpolación
    x_interp = interpolacion(t_fino, t_muestreo, x_muestreada)

    # Graficar
    #plt.figure(figsize=(12, 6))
    
    #plt.stem(t_muestreo, x_muestreada, 'r', markerfmt='ro', basefmt=" ", linefmt='r', use_line_collection=True, label="Muestras")
    escrbir_csv(str(num) +"a.csv", "x", "y", t_muestreo, x_muestreada)
    
    #plt.plot(t_fino, x_interp, 'b', label="Interpolada")
    escrbir_csv(str(num) +"b.csv", "x", "y", t_fino, x_interp)
    
    #plt.plot(t_fino, señal_original(t_fino), 'g--', label="Señal Original")
    escrbir_csv(str(num) +"c.csv", "x", "y", t_fino, señal_original(t_fino))
    
    #plt.legend()
    #plt.title('Muestreo de x(t) a 10Hz')

    #plt.tight_layout()
    #plt.show()

def escrbir_csv(nombre_archivo, encabezado_x, encabezado_y, eje_x, eje_y):

    ruta_completa = os.path.join("static/data/", nombre_archivo)
    with open(ruta_completa, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([encabezado_x, encabezado_y])
        for x, y in zip(eje_x, eje_y):
            escritor_csv.writerow([x, y])

#paso1(2,10,1)
#paso2(2,4,8,1)



