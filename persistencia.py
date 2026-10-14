# =============================================================================
# MÓDULO DE PERSISTENCIA EN JSON (persistencia.py)
# =============================================================================
# Responsabilidad: Guardar y cargar el estado del hotel en archivos JSON.
# Manejo robusto de excepciones (FileNotFoundError, JSONDecodeError, OSError).
# =============================================================================

import os
import json

RUTA_DATOS_JSON = os.path.join("datos", "hotel_data.json")


def asegurar_directorio(ruta_archivo):
    """
    Crea el directorio contenedor del archivo si no existe.
    """
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio, exist_ok=True)
        except OSError as error:
            print(f"[Error] No se pudo crear el directorio {directorio}: {error}")


def existe_datos_json(ruta=RUTA_DATOS_JSON):
    """
    Retorna True si el archivo de persistencia JSON existe en disco.
    """
    return os.path.isfile(ruta)


def guardar_datos_json(hotel, huespedes, tarifas, ruta=RUTA_DATOS_JSON):
    """
    Serializa el estado completo del hotel a un archivo JSON.
    Convierte tuplas a listas automáticamente para compatibilidad con JSON.
    Retorna True si fue exitoso, False en caso contrario.
    """
    try:
        asegurar_directorio(ruta)
        datos = {
            "hotel": hotel,
            "huespedes": huespedes,
            "tarifas": tarifas
        }
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except (TypeError, OSError, IOError) as error:
        print(f"[Error de Persistencia] No se pudo guardar el archivo JSON: {error}")
        return False


def cargar_datos_json(ruta=RUTA_DATOS_JSON):
    """
    Carga y deserializa el estado del hotel desde un archivo JSON.
    Restaura las tuplas inmutables de los registros de huéspedes.
    Retorna un diccionario con 'hotel', 'huespedes' y 'tarifas', o None ante error.
    """
    try:
        if not os.path.exists(ruta):
            return None

        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Restauración de tuplas inmutables en huéspedes
        # Estructura: [ (dni, nombre), (piso, hab, num_comercial), dias, extras ]
        huespedes_restaurados = []
        for h in datos.get("huespedes", []):
            if len(h) >= 4 and isinstance(h[0], (list, tuple)) and isinstance(h[1], (list, tuple)):
                identidad = (str(h[0][0]), str(h[0][1]))
                config_hab = (int(h[1][0]), int(h[1][1]), int(h[1][2]))
                dias = int(h[2])
                extras = float(h[3])
                huespedes_restaurados.append([identidad, config_hab, dias, extras])
            elif len(h) >= 7:
                # Compatibilidad con formato plano anterior
                identidad = (str(h[1]), str(h[0]))
                piso = int(h[3])
                hab = int(h[4])
                num_comercial = int(h[5])
                config_hab = (piso, hab, num_comercial)
                dias = int(h[2])
                extras = float(h[6]) if len(h) > 6 else 0.0
                huespedes_restaurados.append([identidad, config_hab, dias, extras])

        datos["huespedes"] = huespedes_restaurados
        return datos

    except FileNotFoundError:
        return None
    except json.JSONDecodeError as error:
        print(f"[Error de Persistencia] Formato JSON inválido en {ruta}: {error}")
        return None
    except (OSError, IOError) as error:
        print(f"[Error de Persistencia] No se pudo leer {ruta}: {error}")
        return None
