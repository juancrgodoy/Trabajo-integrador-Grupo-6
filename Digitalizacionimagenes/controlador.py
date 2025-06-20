from tkinter import filedialog, messagebox
from modelo import cargar_imagen, procesar_imagen
from db import guardar_proceso
from datetime import datetime
import os
import io

# clase que controla la interacción entre la vista y la lógica del programa
class Controlador:
    def __init__(self, vista):
        self.vista = vista  # referencia a la vista de la interfaz gráfica
        self.imagen_original = None  # almacenará la imagen cargada
        self.imagen_digital = None  # almacenará la imagen procesada
        self.ruta_original = None  # almacenará la ruta de la imagen original

    # método para cargar una imagen desde un archivo
    def cargar_imagen(self):
        # abre un cuadro de diálogo para seleccionar un archivo
        ruta = filedialog.askopenfilename()
        if ruta:
            self.ruta_original = ruta  # guarda la ruta del archivo seleccionado
            self.imagen_original = cargar_imagen(ruta)  # carga la imagen usando la función del modelo
            # muestra la imagen cargada en el panel correspondiente de la vista
            self.vista.mostrar_imagen(self.imagen_original, self.vista.panel_original_label)

    # método para procesar (digitalizar) la imagen cargada
    def digitalizar(self):
        if not self.imagen_original:  # verifica si hay una imagen cargada
            return

        # obtiene los parámetros de resolución y profundidad desde la vista
        resolucion = self.vista.obtener_resolucion()
        profundidad = self.vista.obtener_profundidad()
        # procesa la imagen utilizando la función del modelo
        self.imagen_digital = procesar_imagen(self.imagen_original, resolucion, profundidad)
        # muestra la imagen procesada en el panel correspondiente de la vista
        self.vista.mostrar_imagen(self.imagen_digital, self.vista.panel_digital_label)

        # calcula los tamaños de la imagen original y la digitalizada
        original_kb = os.path.getsize(self.ruta_original) / 1024 if self.ruta_original else 0
        buffer = io.BytesIO()  # crea un buffer para almacenar temporalmente la imagen digitalizada
        self.imagen_digital.save(buffer, format='PNG')  # guarda la imagen en formato png en el buffer
        digital_kb = len(buffer.getvalue()) / 1024  # calcula el tamaño en kilobytes del buffer

        # genera un texto con los tamaños y lo muestra en la vista
        texto = f"Tamaño original: {original_kb:.2f} KB\nTamaño digitalizado: {digital_kb:.2f} KB"
        self.vista.mostrar_info(texto)

        # guarda información del proceso en la base de datos
        guardar_proceso(
            self.ruta_original,  # ruta de la imagen original
            f"{resolucion[0]}x{resolucion[1]}",  # resolución como cadena
            f"{profundidad} bits",  # profundidad como cadena
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # marca de tiempo actual
        )

    # método para guardar la imagen digitalizada en un archivo
    def guardar(self):
        if not self.imagen_digital:  # verifica si hay una imagen procesada
            # muestra un mensaje de advertencia si no hay imagen para guardar
            messagebox.showwarning("Error", "No hay imagen digitalizada para guardar.")
            return

        # abre un cuadro de diálogo para seleccionar dónde guardar la imagen
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if ruta:
            # guarda la imagen procesada en la ubicación seleccionada
            self.imagen_digital.save(ruta)
            # muestra un mensaje de confirmación del guardado
            messagebox.showinfo("Guardado", f"Imagen guardada en:\n{ruta}")
