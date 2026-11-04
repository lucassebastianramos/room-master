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
    Carga el estado del hotel desde el archivo JSON.
    Las tarifas se almacenan como diccionario {piso: precio}.
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
            "tarifas": {}
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
# 2. HELPER DE LECTURA TXT (FUNCIÓN MODULARIZADA)
# -----------------------------------------------------------------------------

def leer_registros_txt(nombre_archivo="facturacion.txt"):
    """
    Lee un archivo delimitado por ';' y retorna una lista de sublistas con sus datos.
    Centraliza el manejo de apertura, lectura y captura de excepciones.
    """
    archivo = None
    registros = []

    try:
        archivo = open(nombre_archivo, "r", encoding="UTF-8")
        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia != "":
                datos = linea_limpia.split(";")
                registros.append(datos)

    except FileNotFoundError:
        print("ERROR. El archivo TXT no existe.")

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo.")

    except (ValueError, IndexError):
        print("ERROR. El archivo contiene registros incorrectos.")

    except OSError as error:
        print("ERROR al trabajar con el archivo:", error)

    finally:
        if archivo is not None:
            archivo.close()

    return registros


# -----------------------------------------------------------------------------
# 3. AUDITORÍA EN ARCHIVO DE TEXTO (.TXT)
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


def registrar_factura_txt(dni, nombre, habitacion, piso, dias, monto, nombre_archivo="facturacion.txt"):
    """
    Registra en modo agregado ('a') cada Check-out cobrado en el archivo TXT.
    Formato: dni;nombre;habitacion;piso;dias;monto
    """
    archivo = None
    try:
        archivo = open(nombre_archivo, "a", encoding="UTF-8")
        registro = f"{dni};{nombre};{habitacion};{piso};{dias};{monto:.2f}\n"
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
    Procesa las facturas registradas usando la función modularizada de lectura.
    """
    registros = leer_registros_txt(nombre_archivo)
    if len(registros) == 0:
        return

    print("\n=== HISTORIAL DE FACTURACIÓN (DESDE ARCHIVO TXT) ===")
    print(f"{'DNI':<12} {'Huésped':<20} {'Hab':>5} {'Piso':>5} {'Días':>5} {'Monto':>14}")
    print("-" * 65)

    total_recaudado = 0.0

    for datos in registros:
        dni = datos[0]
        nombre = datos[1]
        habitacion = datos[2]
        piso = datos[3]
        dias = datos[4]
        monto = float(datos[5])

        print(f"{dni:<12} {nombre:<20} {habitacion:>5} {piso:>5} {dias:>5} ${monto:>13,.2f}")
        total_recaudado += monto

    print("=" * 65)
    print(f"Total comprobantes procesados: {len(registros)}")
    print(f"Recaudación histórica total acumulada: ${total_recaudado:,.2f}")


def historial_huesped(dni_buscado, nombre_archivo="facturacion.txt"):
    """
    Busca y muestra las estadías de un DNI usando la función modularizada de lectura.
    """
    registros = leer_registros_txt(nombre_archivo)
    if len(registros) == 0:
        return

    print(f"\n=== HISTORIAL DE HUÉSPED (DNI: {dni_buscado}) ===")
    encontrado = False
    total = 0.0

    for datos in registros:
        if datos[0] == dni_buscado:
            encontrado = True
            nombre = datos[1]
            habitacion = datos[2]
            piso = datos[3]
            dias = datos[4]
            monto = float(datos[5])

            print(f"  {nombre} - Hab {habitacion} (Piso {piso}) - {dias} días - ${monto:,.2f}")
            total += monto

    if not encontrado:
        print("No se encontraron estadías registradas para ese DNI.")
    else:
        print(f"  Total histórico: ${total:,.2f}")


# -----------------------------------------------------------------------------
# 4. EXPORTACIÓN A EXCEL / CSV (.CSV)
# -----------------------------------------------------------------------------
def exportar_facturacion_a_csv(nombre_archivo_txt="facturacion.txt", nombre_archivo_csv="facturacion.csv"):
    """
    Lee los datos mediante la función modularizada y genera la planilla CSV.
    Formatea el monto con coma decimal para compatibilidad con Excel regional.
    """
    registros = leer_registros_txt(nombre_archivo_txt)
    if len(registros) == 0:
        print("No hay registros para exportar a CSV.")
        return

    archivo_csv = None
    try:
        archivo_csv = open(nombre_archivo_csv, "w", encoding="UTF-8", newline="")
        escritor = csv.writer(archivo_csv)
        escritor.writerow(["DNI", "Huesped", "Habitacion", "Piso", "Dias", "Monto_Cobrado"])

        for datos in registros:
            # Se formatea a 2 decimales y se reemplaza el punto por coma para Excel
            monto_excel = f"{float(datos[5]):.2f}".replace(".", ",")
            escritor.writerow([datos[0], datos[1], datos[2], datos[3], datos[4], monto_excel])

        print(f"\n[Éxito] Se exportaron {len(registros)} registros correctamente a '{nombre_archivo_csv}'.")

    except PermissionError:
        print("ERROR. No tiene permisos para acceder al archivo CSV.")

    except OSError as error:
        print("ERROR al trabajar con el archivo CSV:", error)

    else:
        print("\nExportación CSV finalizada correctamente.")

    finally:
        if archivo_csv is not None:
            archivo_csv.close()