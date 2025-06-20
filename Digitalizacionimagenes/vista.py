import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
import sqlite3

class Vista:
    """
    Clase Vista - Encargada de construir la interfaz gráfica del sistema
    Componentes principales:
    - Panel de controles con selección de resolución, profundidad y botones de acción
    - Panel para mostrar imagen digitalizada (parte superior derecha)
    - Panel para mostrar imagen original (parte inferior izquierda)
    - Panel de información con comparación de tamaños
    - Funciones para mostrar imágenes, mostrar info, historial y borrar historial
    """
    def __init__(self, root, controlador):
        """Inicializa la vista con una referencia al root de Tkinter y al controlador"""
        self.root = root
        self.controlador = controlador
        self.image_original = None
        self.image_digital = None

    def setup_ui(self):
        """Construye toda la interfaz gráfica de la aplicación"""
        self.root.title('Digitalización de Imágenes - MVC')
        self.root.geometry("1100x800")
        self.root.configure(bg="#f8f9fa")

        # Frame principal dividido en izquierdo y derecho
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True)

        frame_izquierdo = tk.Frame(main_frame, width=250, bg="#f8f9fa")
        frame_izquierdo.pack(side="left", fill="y", padx=10, pady=10)

        frame_derecho = tk.Frame(main_frame, bg="#f8f9fa")
        frame_derecho.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Panel de controles con opciones de resolución, profundidad y acciones
        self.frame_controles = tk.LabelFrame(frame_izquierdo, text="Controles", padx=10, pady=10, bg="#f8f9fa", font=("Arial", 10, "bold"))
        self.frame_controles.pack(fill="x")

        tk.Label(self.frame_controles, text="Resolución:", bg="#f8f9fa", font=("Arial", 10)).pack(anchor="w")
        self.res_var = tk.StringVar(value="100x100")
        self.res_menu = tk.OptionMenu(self.frame_controles, self.res_var, "100x100", "500x500", "1000x1000")
        self.res_menu.config(width=15)
        self.res_menu.pack(anchor="w", pady=5)

        tk.Label(self.frame_controles, text="Profundidad:", bg="#f8f9fa", font=("Arial", 10)).pack(anchor="w")
        self.depth_var = tk.StringVar(value="8 bits")
        self.depth_menu = tk.OptionMenu(self.frame_controles, self.depth_var, "1 bit", "8 bits", "24 bits")
        self.depth_menu.config(width=15)
        self.depth_menu.pack(anchor="w", pady=5)

        self.btn_cargar = tk.Button(self.frame_controles, text="📁 Cargar Imagen", width=20, bg="#dee2e6")
        self.btn_cargar.pack(pady=10)

        self.btn_digitalizar = tk.Button(self.frame_controles, text="⚙️ Digitalizar", width=20, bg="#dee2e6")
        self.btn_digitalizar.pack(pady=10)

        self.btn_guardar = tk.Button(self.frame_controles, text="💾 Guardar Imagen", width=20, bg="#dee2e6")
        self.btn_guardar.pack(pady=10)

        self.btn_historial = tk.Button(self.frame_controles, text="📋 Ver Historial", width=20, bg="#dee2e6", command=self.mostrar_historial)
        self.btn_historial.pack(pady=10)

        self.btn_borrar_historial = tk.Button(self.frame_controles, text="🗑️ Borrar Historial", width=20, bg="#ffc9c9", command=self.borrar_historial)
        self.btn_borrar_historial.pack(pady=10)

        # Imagen digitalizada (parte superior centro)
        self.panel_digital = tk.LabelFrame(frame_derecho, text="Imagen Digitalizada", font=("Arial", 10, "bold"), bg="#f8f9fa")
        self.panel_digital.pack(pady=20)
        self.panel_digital_label = tk.Label(self.panel_digital)
        self.panel_digital_label.pack()

        # Imagen original (debajo del panel de controles)
        self.panel_original = tk.LabelFrame(frame_izquierdo, text="Imagen Original", font=("Arial", 10, "bold"), bg="#f8f9fa")
        self.panel_original.pack(pady=20)
        self.panel_original_label = tk.Label(self.panel_original)
        self.panel_original_label.pack()

        # Info de tamaño (debajo de la imagen original)
        self.info_label = tk.Label(frame_izquierdo, text="", justify="left", font=("Arial", 10), bg="#f8f9fa")
        self.info_label.pack(pady=10)

    def mostrar_imagen(self, imagen_pil, panel):
        """Muestra una imagen redimensionada en el panel correspondiente"""
        if panel == self.panel_original_label:
            imagen_pil = imagen_pil.copy()
            imagen_pil.thumbnail((200, 200))

        img_tk = ImageTk.PhotoImage(imagen_pil)
        panel.config(image=img_tk)
        panel.image = img_tk

    def mostrar_info(self, texto):
        """Actualiza la etiqueta de información con texto nuevo"""
        self.info_label.config(text=texto)

    def obtener_resolucion(self):
        """Devuelve la resolución seleccionada en forma de tupla"""
        return {
            "100x100": (100, 100),
            "500x500": (500, 500),
            "1000x1000": (1000, 1000)
        }[self.res_var.get()]

    def obtener_profundidad(self):
        """Devuelve la profundidad de color seleccionada"""
        return {
            "1 bit": 1,
            "8 bits": 8,
            "24 bits": 24
        }[self.depth_var.get()]

    def mostrar_historial(self):
        """Muestra una ventana con los últimos 10 registros del historial de procesamiento"""
        conn = sqlite3.connect("imagenes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historico ORDER BY id DESC LIMIT 10")
        datos = cursor.fetchall()
        conn.close()

        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Procesamientos")
        ventana.geometry("600x300")
        text = tk.Text(ventana, wrap="none")
        text.pack(fill="both", expand=True)

        for fila in datos:
            text.insert("end", f"ID: {fila[0]} | Ruta: {fila[1]} | Resolución: {fila[2]} | Profundidad: {fila[3]} | Fecha: {fila[4]}\n")

    def borrar_historial(self):
        """Pregunta confirmación y borra todos los registros del historial"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que querés borrar todo el historial?"):
            conn = sqlite3.connect("imagenes.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico")
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Historial borrado correctamente.")
