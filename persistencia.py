# =============================================================================
# MÓDULO DE PERSISTENCIA Y AUDITORÍA (persistencia.py)
# =============================================================================
# Responsabilidad: Almacenamiento y recuperación del estado del hotel en JSON
# y registro cronológico de bitácora transaccional en archivo de texto plano (TXT).
# Manejo robusto de excepciones (FileNotFoundError, PermissionError, JSONDecodeError).
# =============================================================================

import os
import json
import datetime

RUTA_DATOS_JSON = os.path.join("datos", "hotel_data.json")
RUTA_AUDITORIA_TXT = os.path.join("datos", "auditoria.txt")


def asegurar_directorio_datos(ruta_archivo):
    """
    Verifica y crea el directorio contenedor del archivo si no existe.
    Previene errores de FileNotFoundError al intentar escribir en carpetas inexistentes.
    """
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio, exist_ok=True)
        except OSError as error:
            print(f"[Error de Sistema] No se pudo crear el directorio {directorio}: {error}")


def registrar_evento_auditoria(operador, accion, detalle, ruta=RUTA_AUDITORIA_TXT):
    """
    Registra una transacción crítica en la bitácora cronológica de auditoría (TXT).
    Formato: [YYYY-MM-DD HH:MM:SS] [OPERADOR: user] ACCION | Detalle
    Utiliza manejo de excepciones con try/except para proteger la ejecución del sistema.
    """
    try:
        asegurar_directorio_datos(ruta)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [OPERADOR: {operador}] ACCION: {accion:<18} | {detalle}\n"

        with open(ruta, "a", encoding="utf-8") as archivo_log:
            archivo_log.write(linea_log)
        return True
    except (OSError, IOError) as error:
        print(f"[Advertencia de Auditoría] No se pudo escribir en la bitácora TXT: {error}")
        return False


def guardar_estado_json(hotel, huespedes, tarifas, usuarios, reglas_negocio, ruta=RUTA_DATOS_JSON):
    """
    Serializa y persiste la totalidad del estado del hotel en un archivo JSON.
    Estructura jerárquica limpia con sangría legible (indent=4).
    Retorna True si la persistencia fue exitosa, o False ante fallo.
    """
    try:
        asegurar_directorio_datos(ruta)
        payload = {
            "version": "2.0",
            "fecha_guardado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hotel": hotel,
            "huespedes": huespedes,
            "tarifas": tarifas,
            "usuarios": usuarios,
            "reglas_negocio": reglas_negocio
        }

        with open(ruta, "w", encoding="utf-8") as archivo_json:
            json.dump(payload, archivo_json, indent=4, ensure_ascii=False)

        return True
    except (TypeError, OSError, IOError) as error:
        print(f"[Error de Persistencia] No se pudo guardar el archivo JSON: {error}")
        return False


def cargar_estado_json(ruta=RUTA_DATOS_JSON):
    """
    Recupera el estado persistido previamente desde el archivo JSON.
    Controla exhaustivamente FileNotFoundError y JSONDecodeError con try/except.
    Retorna el diccionario deserializado o None si el archivo no existe o está corrupto.
    """
    try:
        if not os.path.exists(ruta):
            return None

        with open(ruta, "r", encoding="utf-8") as archivo_json:
            datos_cargados = json.load(archivo_json)
        return datos_cargados
    except FileNotFoundError:
        print(f"[Aviso] No se encontró el archivo de datos previo en {ruta}.")
        return None
    except json.JSONDecodeError as error:
        print(f"[Error de Persistencia] El archivo {ruta} contiene formato JSON inválido: {error}")
        return None
    except (OSError, IOError) as error:
        print(f"[Error de Persistencia] Error al leer archivo {ruta}: {error}")
        return None
