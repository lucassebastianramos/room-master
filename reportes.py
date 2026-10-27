# =============================================================================
# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (reportes.py)
# =============================================================================

import functools
from tarifas import obtener_tarifa_habitacion


def generar_reporte_ocupacion(matriz_hotel):
    """ Genera un reporte que muestra el total de habitaciones,
    las que se encuentran ocupadas y el porcentaje de ocupación del hotel.
    """
    # Total de habitaciones acumulando el largo de cada fila mediante reduce
    total_habitaciones = functools.reduce(
        lambda acumulado, fila: acumulado + len(fila),
        matriz_hotel,
        0
    )

    # Cuenta las habitaciones ocupadas en cada fila usando reduce
    ocupadas_por_fila = map(
        lambda fila: functools.reduce(
            lambda acum, hab: acum + (1 if hab == "O" else 0),
            fila,
            0
        ),
        matriz_hotel
    )

    # Acumula los subtotales de cada fila para obtener el total ocupado
    habitaciones_ocupadas = functools.reduce(
        lambda acumulado, cant: acumulado + cant,
        ocupadas_por_fila,
        0
    )

    if total_habitaciones > 0:
        porcentaje_ocupacion = habitaciones_ocupadas * 100 / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = int(porcentaje_ocupacion * 100 + 0.5) / 100

    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones: ", total_habitaciones)
    print("Habitaciones ocupadas: ", habitaciones_ocupadas)
    print("Porcentaje de ocupación: ", porcentaje_ocupacion, "%")


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a cobrar por un huésped específico y aplica un descuento del 10% si su estadía es mayor a 7 noches.
    Devuelve el subtotal para calcular la recaudación total del hotel.
    """
    dias = int(huesped[2])
    piso = int(huesped[3])
    piso_comercial = piso + 1

    precio_noche = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
    subtotal = precio_noche * dias

    aplicar_descuento = lambda d, s: s * 0.9 if d > 7 else s
    subtotal = aplicar_descuento(dias, subtotal)

    return subtotal


def calcular_recaudacion_total(lista_huespedes, matriz_tarifas):
    """
    Calcula la recaudación total del hotel sumando los subtotales de todos los huéspedes. 
    """
    # Transformación con map para convertir cada huésped en su monto subtotal
    subtotales = list(map(lambda huesped: calcular_subtotal(huesped, matriz_tarifas), lista_huespedes))

    # Acumulación con reduce de los subtotales generados
    recaudacion_total = functools.reduce(lambda acumulado, subtotal: acumulado + subtotal, subtotales, 0.0)

    print("\n=== RECAUDACIÓN TOTAL ===")
    print("Recaudación total: $", recaudacion_total)
    return recaudacion_total

