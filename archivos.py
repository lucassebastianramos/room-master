# =============================================================================
# MÓDULO 5: PERSISTENCIA EN JSON (archivos.py)
# =============================================================================

import json

def cargar_datos_hotel(nombre_archivo="hotel_data.json"):
    """
    Carga el estado del hotel (dimensiones, huéspedes y tarifas) desde el archivo JSON.
    Si el archivo no existe, retorna una estructura por defecto con centinelas (-1).
    """
    try:
        with open(nombre_archivo, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)  # Convierte el archivo JSON a diccionario Python.
    except FileNotFoundError:
        # Si es la primera vez que se ejecuta y no existe el archivo
        datos = {
            "pisos": -1,
            "habitaciones": -1,
            "huespedes": [],
            "tarifas": []
        }
    except (OSError, json.JSONDecodeError) as error:
        # Captura de errores vista en clase
        print("ERROR. No fue posible leer los datos del hotel:", error)
        datos = None

    return datos


def guardar_datos_hotel(nombre_archivo, pisos, habitaciones, lista_huespedes, matriz_tarifas):
    """
    Guarda la configuración del hotel, lista de huéspedes y matriz de tarifas en un archivo JSON.
    Usa ensure_ascii=False e indent=4 según los estándares vistos en clase.
    """
    datos = {
        "pisos": pisos,
        "habitaciones": habitaciones,
        "huespedes": lista_huespedes,
        "tarifas": matriz_tarifas
    }

    guardado = False
    try:
        with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)  # Serializa a JSON
        guardado = True
    except OSError as error:
        print("ERROR. No fue posible guardar los datos del hotel:", error)

    return guardado