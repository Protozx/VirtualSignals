import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mostar_menu():
    """Muestra la imágen principal del programa."""
    for widget in contenido_ventanita.winfo_children():
        widget.destroy()

    t = contenido_ventanita.winfo_width()
    x = contenido_ventanita.winfo_height()

    if (t+x) < 5:
        t = 1280
        x = 720

    image = Image.open("senales.jpg")
    image = image.resize((t, x), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)

    label = tk.Label(contenido_ventanita, image=img)
    label.image = img
    label.pack()


def plot_signal(t, original, t_sampled, sampled, reconstructed, title, ax):
    ax.plot(t, original, label="Original", alpha=0.7)
    ax.stem(t_sampled, sampled, 'r', markerfmt='ro', basefmt=" ", linefmt='r', label="Muestreada")
    ax.plot(t, reconstructed, 'g', label="Reconstruida con 'hold on'")
    ax.set_title(title)
    ax.set_xlabel("Tiempo (t)")
    ax.set_ylabel("Amplitud")
    ax.grid(True)
    ax.legend()



def muestreo_señal():
    global canvas
    # Borrar lo anterior en el marco
    for widget in contenido_ventanita.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(12, 7))
    f = 300
    fs = 800
    T = 1/fs
    t = np.linspace(0, 1, 1000)  # 1 segundo de señal
    t_sampled = np.arange(0, 1, T)
    x_original = np.sin(2 * np.pi * f * t)
    x_sampled = np.sin(2 * np.pi * f * t_sampled)

    # Interpolación con 'hold on' para 300Hz
    x_reconstructed_300 = []
    for i in range(len(t)):
        index = np.searchsorted(t_sampled, t[i])
        if index > 0:
            x_reconstructed_300.append(x_sampled[index - 1])
        else:
            x_reconstructed_300.append(x_sampled[0])

    plot_signal(t, x_original, x_sampled, x_reconstructed_300, "Señal 300Hz muestreada a 800Hz", ax)

    canvas = FigureCanvasTkAgg(fig, master=contenido_ventanita)
    canvas.draw()
    canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Señales")

    header = tk.Frame(root, bg="black")
    header.pack(side="top", fill="x")

    contenido_ventanita = tk.Frame(root, bg="black")
    contenido_ventanita.pack(side="bottom", fill="both", expand=True)

    botones = []
    nombres = ["Muestreo Señal 300Hz", "Menú"]

    for i, name in enumerate(nombres): 
        button = tk.Button(
            header,
            text=name, 
            command=muestreo_señal if name == "Muestreo Señal 300Hz" else mostar_menu,
            bg="purple",
            fg="white",
            font=("Arial", 24),
            relief="solid",
            bd=4,
            highlightthickness=2,
            highlightbackground="black"
        )
        button.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    mostar_menu()

    root.mainloop()
