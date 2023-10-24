import numpy as np
import matplotlib.pyplot as plt

def original(heart):
    Ts = 1/heart    
    x = np.linspace(0, 2, int(2/Ts))
    y = np.sin(4 * np.pi * x) + np.sin(8 * np.pi * x)
    return y, x

def obtener_interpolada(y_muestreada,hz):
    Ts = 1/hz
    x = np.linspace(0, 2, 1000)
    y = interpolar(x, y_muestreada, Ts)
    return y,x

def interpolar(t, x_muestreada, Ts):
    x_interp = np.zeros_like(t)
    for n, x_n in enumerate(x_muestreada):
        x_interp += x_n * funcion_g(t - n * Ts, Ts)
    return x_interp

def graficar_muestreo(y,x):

    # Graficar
    #plt.stem(t, x_muestreada, use_line_collection=True)
    plt.plot(x, y)
    plt.title('Muestreo de x(t) a 10Hz')
    plt.xlabel('Tiempo (t)')
    plt.ylabel('x(t)')
    plt.grid(True)
    plt.show()
    
def muestreo_sinusoidal(frecuencia, frecuencia_muestreo):
    # Duración de la señal en segundos
    T = 0.01  # Mostraremos la señal durante 2 segundos

    # Tiempo continuo y muestreado
    t_continuo = np.linspace(0, T, 1000)
    t_muestreado = np.linspace(0, T, int(T*frecuencia_muestreo))
    
    # Señal sinusoidal continuo y muestreado
    x_continuo = np.sin(2 * np.pi * frecuencia * t_continuo)
    x_muestreado = np.sin(2 * np.pi * frecuencia * t_muestreado)

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(t_continuo, x_continuo, label="Sinusoidal Continua")
    plt.stem(t_muestreado, x_muestreado, 'r', markerfmt='ro', basefmt=" ", linefmt='r', use_line_collection=True, label=f"Muestras a {frecuencia_muestreo}Hz")
    plt.title(f'Muestreo de una Onda Sinusoidal de {frecuencia}Hz a {frecuencia_muestreo}Hz')
    plt.legend()
    plt.show()


def señal_original(t):
    return np.sin(4 * np.pi * t) + np.sin(8 * np.pi * t)

def funcion_g(t, Ts):
    return np.sinc(t / Ts)

def interpolacion(t, t_muestreo, x_muestreada, Ts):
    x_interp = np.zeros_like(t)
    for n, x_n in enumerate(x_muestreada):
        x_interp += x_n * funcion_g(t - t_muestreo[n], Ts)
    return x_interp

def graficar_muestreo_y_interpolacion():
    # Periodo de muestreo
    Ts = 1/10  # 10Hz

    # Crear un array de valores de tiempo t para 2 segundos
    t_muestreo = np.linspace(0, 2, int(2/Ts))
    t_fino = np.linspace(0, 2, 1000)

    # Muestrear la señal
    x_muestreada = señal_original(t_muestreo)

    # Interpolación
    x_interp = interpolacion(t_fino, t_muestreo, x_muestreada, Ts)

    # Graficar
    plt.figure(figsize=(12, 6))
    
    plt.stem(t_muestreo, x_muestreada, 'r', markerfmt='ro', basefmt=" ", linefmt='r', use_line_collection=True, label="Muestras")
    plt.plot(t_fino, x_interp, 'b', label="Interpolada")
    plt.plot(t_fino, señal_original(t_fino), 'g--', label="Señal Original")
    plt.legend()
    plt.title('Muestreo de x(t) a 10Hz')

    plt.tight_layout()
    plt.show()

graficar_muestreo_y_interpolacion()

hz = 10
#y,x = original(hz)
#graficar_muestreo(y,x)
#y,x = obtener_interpolada(y,hz)
#graficar_muestreo(y,x)

muestreo_sinusoidal(300, 800)



