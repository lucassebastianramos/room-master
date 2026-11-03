# =============================================================================
# MÓDULO 5: PERSISTENCIA EN JSON (archivos.py)
# =============================================================================

import json

def cargar_datos_hotel(nombre_archivo="hotel_data.json"):
    datos = None
    try:
        with open(nombre_archivo, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)

    except FileNotFoundError:
        print("ERROR. El archivo no existe.")
        datos = {
            "pisos": -1,
            "habitaciones": -1,
            "huespedes": [],
            "tarifas": []
        }

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo.")

    except (ValueError, IndexError):
        print("ERROR. El archivo contiene registros incorrectos.")

    except OSError as error:
        print("ERROR al trabajar con el archivo:", error)

    else:
        print("\nLectura finalizada correctamente.")

    return datos


def guardar_datos_hotel(nombre_archivo, pisos, habitaciones, lista_huespedes, matriz_tarifas):
    """
    Guarda la configuración del hotel en el archivo JSON con manejo de excepciones.
    """
    archivo = None
    guardado = False

    datos = {
        "pisos": pisos,
        "habitaciones": habitaciones,
        "huespedes": lista_huespedes,
        "tarifas": matriz_tarifas
    }

    try:
        archivo = open(nombre_archivo, "w", encoding="UTF-8")
        json.dump(datos, archivo, ensure_ascii=False, indent=4)
        guardado = True

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo.")

    except (ValueError, TypeError):
        print("ERROR. El archivo contiene registros incorrectos.")

    except OSError as error:
        print("ERROR al trabajar con el archivo:", error)

    else:
        print("\nEscritura finalizada correctamente.")

    finally:
        if archivo != None:
            archivo.close()

    return guardado