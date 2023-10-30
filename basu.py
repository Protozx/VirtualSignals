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


def p33(josue, tipo, bits,idd):
    def generar_senal(f0, t): # Genera 'n' puntos equidistantes
        return 10 * np.sin(2 * np.pi * f0 * t)

    def cuantificar(senal, bits):
        """Cuantifica una señal en base a la cantidad de bits especificada."""
        niveles = 2**bits
        maximo = np.max(senal)
        minimo = np.min(senal)
        paso = (maximo - minimo) / niveles
        senal_cuantificada = np.floor((senal - minimo) / paso) * paso + minimo
        return senal_cuantificada
    
    def cuantificar2(senal, bits):
        """Cuantifica una señal en base a la cantidad de bits especificada."""
        niveles = 2**bits
        maximo = np.max(senal)
        minimo = np.min(senal)
        paso = (maximo - minimo) / niveles
        senal_cuantificada = np.round((senal - minimo) / paso) * paso + minimo
        return senal_cuantificada

    def interpolacion(t, t_muestreo, x_muestreada):
        x_interp = np.zeros_like(t)
        for n, x_n in enumerate(x_muestreada):
            g = np.sin(np.pi * 200 * (t - t_muestreo[n])) / (np.pi * 200 * (t - t_muestreo[n]))
            x_interp += x_n * g
        return x_interp
    
    # Ejemplo de uso:
    t = np.linspace(0, 2, 1000)
    tm = np.linspace(0, 2, josue*70)
    senal = generar_senal(50, t)
    senal_muestreada = generar_senal(50, tm)  # Muestreo a los puntos especificados
    if (tipo == '1'):
        senal_cuantificada = cuantificar2(senal_muestreada, bits)
    else:
        senal_cuantificada = cuantificar(senal_muestreada, bits)
    error = senal_muestreada - senal_cuantificada
    recuperada = interpolacion(t, tm, senal_cuantificada)  # Usar tm en la interpolación
    
    
    plt.figure(figsize=(12, 10), facecolor='black')  # fondo negro para la figura

    # Señal muestreada
    plt.subplot(2, 2, 1, facecolor='black')  # fondo negro para el subplot
    plt.plot(tm, senal_muestreada, label='x(n)', color='purple')
    plt.xlabel('Tiempo (s)', color='white')
    plt.ylabel('Amplitud', color='white')
    plt.title('Señal Muestreada', color='white')
    plt.legend()
    plt.grid(True, color='gray')
    plt.tick_params(axis='both', colors='white')

    # Error
    plt.subplot(2, 2, 2, facecolor='black')
    plt.plot(tm, error, label='e(n)', color='green')
    plt.xlabel('Tiempo (s)', color='white')
    plt.ylabel('Amplitud', color='white')
    plt.title('Error', color='white')
    plt.legend()
    plt.grid(True, color='gray')
    plt.tick_params(axis='both', colors='white')

    # Señal recuperada
    plt.subplot(2, 2, 3, facecolor='black')
    plt.plot(t, recuperada, label='Recuperada', color='red')
    plt.xlabel('Tiempo (s)', color='white')
    plt.ylabel('Amplitud', color='white')
    plt.title('Señal Recuperada', color='white')
    plt.legend()
    plt.grid(True, color='gray')
    plt.tick_params(axis='both', colors='white')

    # Señal cuantificada
    plt.subplot(2, 2, 4, facecolor='black')
    plt.stem(tm, senal_cuantificada, label='xQ(n)', linefmt='cyan', markerfmt='o', basefmt="gray")  # Cambiamos colores para el stem
    plt.xlabel('Tiempo (s)', color='white')
    plt.ylabel('Amplitud', color='white')
    plt.title('Señal Cuantificada', color='white')
    plt.legend()
    plt.grid(True, color='gray')
    plt.tick_params(axis='both', colors='white')

    # Ajusta el layout para que no haya superposición
    plt.tight_layout()
    
    plt.savefig("static/data/" + (str(idd) + '.png'), dpi=300, bbox_inches='tight', facecolor='black')



#p33('0',2,1)
#p33('1',2,2)



 





