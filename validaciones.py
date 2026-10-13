# =============================================================================
# MÓDULO DE VALIDACIONES GENÉRICAS (validaciones.py)
# =============================================================================
# Responsabilidad: Capa de validación de entradas de usuario basada en
# Expresiones Regulares (re). Garantiza datos limpios y tipados antes de operar.
# =============================================================================

import re

# Patrones Regex obligatorios para la integridad de datos
PATRON_NUMERO_VALIDO = r"^\d+$"
PATRON_DNI_VALIDO = r"^\d{7,8}$"
PATRON_TEXTO_VALIDO = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
PATRON_DIAS_VALIDO = r"^[1-9]\d*$"

# Mensajes de error estandarizados
ERROR_NUMERO = "Error: Debe ingresar un número entero válido."
ERROR_DNI = "DNI INVÁLIDO. Debe contener entre 7 y 8 dígitos numéricos."
ERROR_TEXTO = "Error. El texto solo debe contener letras y no debe estar vacío."
ERROR_DIAS = "Error: La cantidad de días debe ser mayor a 0."


def validar_generico(mensaje, patron, mensaje_error):
    """
    Solicita una entrada al usuario y la valida iterativamente contra una
    expresión regular (patron) hasta que sea correcta.
    Retorna la cadena de texto validada.
    """
    dato_ingresado = input(mensaje).strip()
    while not re.match(patron, dato_ingresado):
        print(mensaje_error)
        dato_ingresado = input(mensaje).strip()
    return dato_ingresado


def validar_generico_con_cancelacion(mensaje, patron, mensaje_error):
    """
    Solicita una entrada al usuario con opción de cancelar ingresando '0'.
    Si el usuario ingresa '0' o 'cancelar', retorna None.
    Si el formato es inválido, muestra el mensaje de error y advierte sobre la cancelación.
    """
    while True:
        dato_ingresado = input(mensaje).strip()
        if dato_ingresado in ["0", "cancelar", "CANCELAR"]:
            print("[Operación cancelada] Regresando...")
            return None

        if re.match(patron, dato_ingresado):
            return dato_ingresado

        print(mensaje_error)
        print("(Tip: Ingrese '0' si desea cancelar la operación y volver al menú)")


def confirmar_accion(mensaje="¿Confirma la operación? (s/n): "):
    """
    Solicita confirmación explícita al usuario para operaciones críticas
    (Check-in, Check-out, Swap, etc.).
    Retorna True si confirma ('s' o 'si'), False en caso contrario.
    """
    respuesta = input(mensaje).strip().lower()
    return respuesta in ["s", "si", "sí"]


def solicitar_dimension_valida(mensaje, min_val, max_val):
    """
    Solicita un número entero dentro de un rango numérico [min_val, max_val].
    Reutiliza validar_generico para asegurar el tipo entero.
    Retorna el número validado.
    """
    es_valido = False
    valor_num = 0

    while not es_valido:
        valor_num = int(validar_generico(mensaje, PATRON_NUMERO_VALIDO, ERROR_NUMERO))
        if min_val <= valor_num <= max_val:
            es_valido = True
        else:
            print(f"Error: El valor debe estar entre {min_val} y {max_val}.")

    return valor_num
