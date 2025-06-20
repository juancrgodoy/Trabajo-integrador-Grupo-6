import cv2
import numpy as np
from PIL import Image

# carga una imagen desde un archivo en formato compatible con PIL
def cargar_imagen(filepath):
    return Image.open(filepath)

# procesa la imagen recibida en formato PIL con opciones de resolución y profundidad
def procesar_imagen(imagen_pil, resolucion, profundidad):
    # convierte la imagen de PIL a un array de numpy
    image_np = np.array(imagen_pil)
    # redimensiona la imagen al tamaño especificado en resolucion usando un escalado básico
    resized = cv2.resize(image_np, resolucion, interpolation=cv2.INTER_NEAREST)

    if profundidad == 1:
        # convierte la imagen a escala de grises
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        # aplica un umbral para crear una imagen en blanco y negro
        _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # convierte la imagen binaria de nuevo a un formato RGB para mantener la consistencia
        final = cv2.cvtColor(bw, cv2.COLOR_GRAY2RGB)
    elif profundidad == 8:
        # convierte la imagen a escala de grises
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        # convierte la imagen de grises a formato RGB para mantener la consistencia
        final = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    else:
        # si la profundidad no es 1 ni 8, simplemente usa la imagen redimensionada
        final = resized

    # convierte el array de numpy de vuelta a una imagen PIL y la devuelve
    return Image.fromarray(final)

# guarda una imagen en formato jpg con una calidad especificada
def comprimir_a_jpg(imagen_pil, calidad=80):
    import io  # se usa para manejar la compresión en memoria
    buffer = io.BytesIO()  # crea un buffer en memoria para almacenar el archivo comprimido
    # guarda la imagen en el buffer con el formato jpg y la calidad especificada
    imagen_pil.save(buffer, format="JPEG", quality=calidad)
    # devuelve el contenido comprimido y el tamaño en KB
    return buffer.getvalue(), len(buffer.getvalue()) / 1024  # bytes, tamaño en KB
