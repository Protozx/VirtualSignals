import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

# Función para procesar la imagen seleccionada
def procesar_imagen(imagen):
    # Aquí puedes conectar tu algoritmo de procesamiento de imágenes
    # y generar las imágenes y el texto procesados
    # Por ahora, solo imprimimos el nombre de la imagen seleccionada
    print("Imagen seleccionada:", imagen)

# Función para abrir el diálogo de selección de imágenes
def seleccionar_imagen():
    # Mostrar el diálogo de selección de archivo
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))

    # Verificar si se seleccionó una imagen
    if ruta_imagen:
        # Procesar la imagen seleccionada
        procesar_imagen(ruta_imagen)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Virtual Esperancita")

# Configurar el tamaño y posición de la ventana principal
ancho_ventana = 800
alto_ventana = 600
posicion_x = int(ventana.winfo_screenwidth() / 2 - ancho_ventana / 2)
posicion_y = int(ventana.winfo_screenheight() / 2 - alto_ventana / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

# Pantalla de presentación
pantalla_presentacion = tk.Frame(ventana)
pantalla_presentacion.pack(fill=tk.BOTH, expand=True)

# Logo de la empresa
logo_empresa = Image.open("img1.jpg")  # Reemplaza "ruta_del_logo.png" con la ruta de tu logo
logo_empresa = logo_empresa.resize((200, 200))  # Ajusta el tamaño del logo según tus necesidades
logo_empresa = ImageTk.PhotoImage(logo_empresa)
logo_label = tk.Label(pantalla_presentacion, image=logo_empresa)
logo_label.pack(pady=20)

# Título
titulo_label = tk.Label(pantalla_presentacion, text="Virtual Esperancita", font=("Arial", 24, "bold"))
titulo_label.pack(pady=10)

# Botón "Seleccionar imagen"
seleccionar_imagen_btn = tk.Button(pantalla_presentacion, text="Selecciona la imagen", command=seleccionar_imagen)
seleccionar_imagen_btn.pack(pady=20)

# Función para mostrar los resultados procesados
def mostrar_resultados(imagenes, texto):
    # Ocultar la pantalla de presentación
    pantalla_presentacion.pack_forget()

    # Pantalla de resultados
    pantalla_resultados = tk.Frame(ventana)
    pantalla_resultados.pack(fill=tk.BOTH, expand=True)

    # Mostrar las imágenes generadas
    for imagen in imagenes:
        imagen_label = tk.Label(pantalla_resultados, image=imagen)
        imagen_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Mostrar el texto generado
    texto_label = tk.Label(pantalla_resultados, text=texto, font=("Arial", 14))
    texto_label.pack(pady=10)

    # Botón "Volver al inicio"
    volver_btn = tk.Button(pantalla_resultados, text="Volver al inicio", command=ventana.destroy)
    volver_btn.pack(pady=20)

# Ejemplo de imágenes generadas y texto generado
ejemplo_imagenes = []  # Reemplaza esta lista con tus imágenes generadas
ejemplo_texto = "Texto generado"  # Reemplaza este texto con el texto generado

# Llamar a la función para mostrar los resultados (solo para prueba)
mostrar_resultados(ejemplo_imagenes, ejemplo_texto)

# Agregar un scrollbar al catálogo de imágenes
catalogo_frame = tk.Frame(pantalla_presentacion)
catalogo_frame.pack(pady=20)

scrollbar = tk.Scrollbar(catalogo_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

catalogo_canvas = tk.Canvas(catalogo_frame, yscrollcommand=scrollbar.set)
catalogo_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=catalogo_canvas.yview)

# Frame para contener las imágenes en el catálogo
imagenes_frame = tk.Frame(catalogo_canvas)
catalogo_canvas.create_window((0, 0), window=imagenes_frame, anchor=tk.NW)

# Agregar imágenes al catálogo
for i in range(10):
    # Ejemplo: Crear etiquetas de imágenes
    imagen = Image.open(f"img{i+1}.jpg")  # Reemplaza "ruta_imagen{i+1}.jpg" con la ruta de tus imágenes
    imagen = imagen.resize((100, 100))  # Ajusta el tamaño de la imagen según tus necesidades
    imagen = ImageTk.PhotoImage(imagen)

    imagen_label = tk.Label(imagenes_frame, image=imagen)
    imagen_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Agregar la imagen seleccionada al botón dinámico
    seleccionar_btn = tk.Button(imagenes_frame, text="Aceptar", command=lambda img=imagen: procesar_imagen(img))
    seleccionar_btn.pack(side=tk.LEFT, padx=10)

# Configurar el desplazamiento del canvas
imagenes_frame.update_idletasks()
catalogo_canvas.config(scrollregion=catalogo_canvas.bbox(tk.ALL))

# Ejecutar la aplicación
ventana.mainloop()
