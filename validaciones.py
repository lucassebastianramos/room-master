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


def validar_generico(mensaje, patron, mensaje_error, permitir_cancelar=True):
    dato = input(mensaje).strip()

    # Si permite cancelar y el usuario ingresa -1, cortamos enseguida
    if permitir_cancelar and dato == "-1":
        return "-1"

    # Mientras no cumpla el patrón...
    while not re.match(patron, dato):
        print(mensaje_error)
        dato = input(mensaje).strip()
        
        # Volvemos a darle la oportunidad de cancelar si se equivoca y quiere salir
        if permitir_cancelar and dato == "-1":
            return "-1"

    return dato


def solicitar_dimension_valida(mensaje, min_val, max_val, permitir_cancelar=True):
    es_valido = False
    valor_num = 0

    while not es_valido:
        dato = validar_generico(mensaje, PATRON_NUMERO_VALIDO, ERROR_NUMERO, permitir_cancelar)
        
        if permitir_cancelar and dato == "-1":
            return -1

        valor_num = int(dato)
        if min_val <= valor_num <= max_val:
            es_valido = True
        else:
            print(f"Error: El valor debe estar entre {min_val} y {max_val}.")

    return valor_num

def solicitar_confirmacion(mensaje, permitir_cancelar=True):
    opcion = input(mensaje).strip().lower()

    while opcion not in ["s", "si", "sí", "n", "no"]:
        if permitir_cancelar and opcion == "-1":
            return "-1"
            
        print("Opción inválida. Ingrese 's' o 'n'.")
        opcion = input(mensaje).strip().lower()

    if opcion in ["s", "si", "sí"]:
        return True
    return False