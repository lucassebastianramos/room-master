# =============================================================================
# MÓDULO 5: PERSISTENCIA Y MANEJO DE ARCHIVOS (archivos.py)
# =============================================================================

import json
import csv


# -----------------------------------------------------------------------------
# 1. PERSISTENCIA EN JSON (Estructura general del hotel)
# -----------------------------------------------------------------------------

def cargar_datos_hotel(nombre_archivo="hotel_data.json"):
    """
    Carga el estado del hotel desde el archivo JSON aplicando la estructura
    de excepciones con try - except - else - finally.
    """
    archivo = None
    datos = None

    try:
        archivo = open(nombre_archivo, "r", encoding="UTF-8")
        datos = json.load(archivo)

    except FileNotFoundError:
        print("ERROR. El archivo JSON no existe. Creando estructura inicial...")
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
        print("\nLectura de datos JSON finalizada correctamente.")

    finally:
        if archivo is not None:
            archivo.close()

    return datos


def guardar_datos_hotel(nombre_archivo, pisos, habitaciones, lista_huespedes, matriz_tarifas):
    """
    Guarda la configuración del hotel, huéspedes y tarifas en el archivo JSON.
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
        print("\nEscritura JSON finalizada correctamente.")

    finally:
        if archivo is not None:
            archivo.close()

    return guardado


# -----------------------------------------------------------------------------
# 2. AUDITORÍA EN ARCHIVO DE TEXTO (.TXT)
# -----------------------------------------------------------------------------

def inicializar_archivo_txt(nombre_archivo="facturacion.txt"):
    """
    Garantiza que el archivo facturacion.txt exista desde la inicialización del sistema.
    """
    archivo = None
    try:
        archivo = open(nombre_archivo, "a", encoding="UTF-8")
    except PermissionError:
        print("ERROR. No tiene permisos para crear el archivo TXT.")
    except OSError as error:
        print("ERROR al inicializar el archivo TXT:", error)
    finally:
        if archivo is not None:
            archivo.close()


def registrar_factura_txt(dni, nombre, monto, nombre_archivo="facturacion.txt"):
    """
    Registra en modo agregado ('a') cada Check-out cobrado en el archivo TXT.
    """
    archivo = None
    try:
        archivo = open(nombre_archivo, "a", encoding="UTF-8")
        registro = f"{dni};{nombre};{monto:.2f}\n"
        archivo.write(registro)

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo.")

    except OSError as error:
        print("ERROR al trabajar con el archivo:", error)

    finally:
        if archivo is not None:
            archivo.close()


def leer_y_procesar_facturacion_txt(nombre_archivo="facturacion.txt"):
    """
    Lee el archivo TXT de facturas, procesa los registros y calcula el total histórico.
    """
    archivo = None
    try:
        archivo = open(nombre_archivo, "r", encoding="UTF-8")

        print("\n=== HISTORIAL DE FACTURACIÓN (DESDE ARCHIVO TXT) ===")
        print(f"{'DNI':<12} {'Huésped':<25} {'Monto Cobrado':>15}")
        print("-" * 55)

        total_recaudado = 0.0
        cantidad = 0

        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia != "":
                datos = linea_limpia.split(";")
                dni = datos[0]
                nombre = datos[1]
                monto = float(datos[2])

                total_recaudado += monto
                cantidad += 1
                print(f"{dni:<12} {nombre:<25} ${monto:>14,.2f}")

        print("=" * 55)
        print(f"Total comprobantes procesados: {cantidad}")
        print(f"Recaudación histórica total acumulada: ${total_recaudado:,.2f}")

    except FileNotFoundError:
        print("ERROR. El archivo TXT no existe.")

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo.")

    except (ValueError, IndexError):
        print("ERROR. El archivo contiene registros incorrectos.")

    except OSError as error:
        print("ERROR al trabajar con el archivo:", error)

    else:
        print("\nLectura TXT finalizada correctamente.")

    finally:
        if archivo is not None:
            archivo.close()


# -----------------------------------------------------------------------------
# 3. EXPORTACIÓN A EXCEL / CSV (.CSV)
# -----------------------------------------------------------------------------

def exportar_facturacion_a_csv(nombre_archivo_txt="facturacion.txt", nombre_archivo_csv="facturacion.csv"):
    """
    Lee el archivo TXT y genera un reporte estructurado en CSV usando la librería csv.
    """
    archivo_txt = None
    archivo_csv = None

    try:
        archivo_txt = open(nombre_archivo_txt, "r", encoding="UTF-8")
        archivo_csv = open(nombre_archivo_csv, "w", encoding="UTF-8", newline="")

        escritor = csv.writer(archivo_csv)
        escritor.writerow(["DNI", "Huesped", "Monto_Cobrado"])

        cantidad_exportados = 0
        for linea in archivo_txt:
            linea_limpia = linea.strip()
            if linea_limpia != "":
                datos = linea_limpia.split(";")
                escritor.writerow([datos[0], datos[1], f"{float(datos[2]):.2f}"])
                cantidad_exportados += 1

        print(f"\n[Éxito] Se exportaron {cantidad_exportados} registros correctamente a '{nombre_archivo_csv}'.")

    except FileNotFoundError:
        print("ERROR. El archivo TXT no existe para realizar la exportación.")

    except PermissionError:
        print("ERROR. No tiene permisos para acceder a los archivos.")

    except (ValueError, IndexError):
        print("ERROR. El archivo contiene registros incorrectos.")

    except OSError as error:
        print("ERROR al trabajar con los archivos:", error)

    else:
        print("\nExportación CSV finalizada correctamente.")

    finally:
        if archivo_txt is not None:
            archivo_txt.close()
        if archivo_csv is not None:
            archivo_csv.close()