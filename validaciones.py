# =============================================================================
# MÓDULO DE VALIDACIONES GENÉRICAS (validaciones.py)
# =============================================================================

import re

# Patrones Regex para la validación de datos
PATRON_NUMERO_VALIDO = r"^\d+$"
PATRON_DNI_VALIDO = r"^\d{7,8}$"
PATRON_TEXTO_VALIDO = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
PATRON_DIAS_VALIDO = r"^[1-9]\d*$"

# Mensajes de error estandarizados
ERROR_NUMERO = "Error: Debe ingresar un número entero válido."
ERROR_DNI = "DNI INVÁLIDO."
ERROR_TEXTO = "Error. El texto solo debe contener letras y no debe estar vacío."
ERROR_DIAS = "Error: La cantidad de días debe ser mayor a 0."


def validar_generico(mensaje, patron, mensaje_error):
    """Pide un dato, lo valida contra 'patron' hasta que sea correcto y lo devuelve como texto."""
    dato_ingresado = input(mensaje).strip()
    while not re.match(patron, dato_ingresado):
        print(mensaje_error)
        dato_ingresado = input(mensaje).strip()
    return dato_ingresado


def solicitar_dimension_valida(mensaje, min_val, max_val):
    """
    Solicita una entrada al usuario y valida únicamente que se encuentre
    dentro del rango (min_val, max_val).
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


def solicitar_confirmacion(mensaje):
    """
    Solicita una respuesta afirmativa o negativa (s/n) al usuario.
    Retorna True si la respuesta es afirmativa (s/si/sí) y False si es negativa (n/no).
    """
    opcion = input(mensaje).strip().lower()
    while opcion not in ["s", "si", "sí", "n", "no"]:
        print("Opción inválida. Ingrese 's' o 'n'.")
        opcion = input(mensaje).strip().lower()

    if opcion in ["s", "si", "sí"]:
        confirmado = True
    else:
        confirmado = False

    return confirmado