# =============================================================================
# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (reportes.py)
# =============================================================================

import functools
from tarifas import obtener_tarifa_habitacion


def generar_reporte_ocupacion(matriz_hotel, lista_huespedes=None):
    """
    Genera un reporte mostrando el total de habitaciones, ocupadas, libres
    y el porcentaje global de ocupación del hotel.
    Integra la información de habitaciones libres (sin repetir el total).
    """
    if lista_huespedes is None:
        lista_huespedes = []

    # Acumula el total de habitaciones sumando la longitud de cada fila
    total_habitaciones = functools.reduce(
        lambda acumulado, fila: acumulado + len(fila),
        matriz_hotel,
        0
    )

    # Cuenta las habitaciones ocupadas ("O") por fila
    ocupadas_por_fila = map(
        lambda fila: functools.reduce(
            lambda acumulado_ocupadas, habitacion: acumulado_ocupadas + (1 if habitacion == "O" else 0),
            fila,
            0
        ),
        matriz_hotel
    )

    # Suma las ocupadas de cada fila para el total general
    habitaciones_ocupadas = functools.reduce(
        lambda acumulado, cantidad: acumulado + cantidad,
        ocupadas_por_fila,
        0
    )

    # Conjuntos: todas las habitaciones y las ocupadas
    todas = set()
    for piso in range(len(matriz_hotel)):
        for hab in range(len(matriz_hotel[piso])):
            num = (piso + 1) * 100 + (hab + 1)
            todas.add(num)

    ocupadas_set = set()
    for huesped in lista_huespedes:
        ocupadas_set.add(huesped["ubicacion"][2])

    libres = todas.difference(ocupadas_set)

    # Cálculo del porcentaje
    if total_habitaciones > 0:
        porcentaje_ocupacion = (habitaciones_ocupadas * 100) / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = int(porcentaje_ocupacion * 100 + 0.5) / 100

    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones: ", total_habitaciones)
    if habitaciones_ocupadas == 0:
        print("Habitaciones ocupadas: ninguna (hotel vacío)")
    else:
        print("Habitaciones ocupadas: ", habitaciones_ocupadas)
    if len(libres) == 0:
        print("Habitaciones libres: ninguna (hotel completo)")
    else:
        print("Habitaciones libres: ", len(libres), sorted(libres))
    print("Porcentaje de ocupación:", porcentaje_ocupacion, "%")


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a cobrar por un huésped accediendo a las claves de su diccionario.
    Aplica una bonificación del 10% si la estadía es mayor a 7 noches.
    """
    dias = int(huesped["dias"])
    piso = int(huesped["ubicacion"][0])
    piso_comercial = piso + 1

    precio_noche = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
    subtotal = precio_noche * dias

    # Expresión lambda para descuento por estadía larga
    aplicar_descuento = lambda dias_estadia, subtotal_actual: subtotal_actual * 0.9 if dias_estadia > 7 else subtotal_actual
    subtotal = aplicar_descuento(dias, subtotal)

    return subtotal


def calcular_recaudacion_total(lista_huespedes, matriz_tarifas):
    """
    Calcula la recaudación total proyectada del hotel sumando los subtotales de todos
    los huéspedes mediante map y reduce sobre la lista de diccionarios.
    """
    # map transforma la lista de diccionarios en una lista de montos (subtotales)
    subtotales = list(map(lambda huesped_actual: calcular_subtotal(huesped_actual, matriz_tarifas), lista_huespedes))

    # reduce acumula la suma de todos los subtotales
    recaudacion_total = functools.reduce(lambda acumulado, subtotal: acumulado + subtotal, subtotales, 0.0)

    print("\n=== RECAUDACIÓN TOTAL ===")
    print(f"Recaudación total proyectada: ${recaudacion_total:,.2f}")
    return recaudacion_total


