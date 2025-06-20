import tkinter as tk
from vista import Vista
from controlador import Controlador
from db import crear_tabla


# entrada principal del sistema de digitalización de imágenes.
#se encarga de:

#- Crear la base de datos (si no existe)
#- Inicializar la interfaz gráfica 

#- Crear la instancia de Vista y Controlador
#- Asignar los eventos de los botones a métodos del controlador


if __name__ == '__main__':
    crear_tabla()  # Se asegura de que la tabla de historial exista

    root = tk.Tk()                            # Ventana principal de la aplicación
    vista = Vista(root, None)                # Se crea la vista sin controlador aún
    controlador = Controlador(vista)         # Se crea el controlador con la vista
    vista.controlador = controlador          # Se asigna el controlador a la vista
    vista.setup_ui()                         # Se arma la interfaz

    # Asignación de funciones a los botones
    vista.btn_cargar.config(command=controlador.cargar_imagen)
    vista.btn_digitalizar.config(command=controlador.digitalizar)
    vista.btn_guardar.config(command=controlador.guardar)

    root.mainloop()                          # Inicia el loop de eventos
