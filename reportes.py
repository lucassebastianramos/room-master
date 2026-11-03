# =============================================================================
# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (reportes.py)
# =============================================================================

import functools
from tarifas import obtener_tarifa_habitacion


def generar_reporte_ocupacion(matriz_hotel):
    """
    Genera un reporte mostrando el total de habitaciones, ocupadas y
    el porcentaje global de ocupación del hotel.

    >>> matriz = [["O", "L"], ["L", "L"]]
    >>> generar_reporte_ocupacion(matriz)
    <BLANKLINE>
    === REPORTE DE OCUPACIÓN ===
    Total de habitaciones:  4
    Habitaciones ocupadas:  1
    Porcentaje de ocupación: 25.0 %
    """
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

    # Cálculo del porcentaje
    if total_habitaciones > 0:
        porcentaje_ocupacion = (habitaciones_ocupadas * 100) / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = int(porcentaje_ocupacion * 100 + 0.5) / 100

    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones: ", total_habitaciones)
    print("Habitaciones ocupadas: ", habitaciones_ocupadas)
    print("Porcentaje de ocupación:", porcentaje_ocupacion, "%")


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a cobrar por un huésped accediendo a las claves de su diccionario.
    Aplica una bonificación del 10% si la estadía es mayor a 7 noches.

    >>> tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    >>> huesped_estandar = {"identidad": ("12345678", "Juan"), "dias": 5, "ubicacion": [0, 0, 101]}
    >>> calcular_subtotal(huesped_estandar, tarifas)
    50000.0
    >>> huesped_larga_estadia = {"identidad": ("12345678", "Juan"), "dias": 10, "ubicacion": [0, 0, 101]}
    >>> calcular_subtotal(huesped_larga_estadia, tarifas)
    90000.0
    >>> huesped_limite_7 = {"identidad": ("12345678", "Juan"), "dias": 7, "ubicacion": [0, 0, 101]}
    >>> calcular_subtotal(huesped_limite_7, tarifas)
    70000.0
    >>> huesped_cero = {"identidad": ("12345678", "Juan"), "dias": 0, "ubicacion": [0, 0, 101]}
    >>> calcular_subtotal(huesped_cero, tarifas)
    0.0
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

    >>> tarifas = [[1, 10000.0], [2, 12000.0]]
    >>> h1 = {"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}
    >>> h2 = {"identidad": ("222", "Bob"), "dias": 3, "ubicacion": [1, 0, 201]}
    >>> total = calcular_recaudacion_total([h1, h2], tarifas)
    <BLANKLINE>
    === RECAUDACIÓN TOTAL ===
    Recaudación total proyectada: $56,000.00
    >>> total
    56000.0
    """
    # map transforma la lista de diccionarios en una lista de montos (subtotales)
    subtotales = list(map(lambda huesped_actual: calcular_subtotal(huesped_actual, matriz_tarifas), lista_huespedes))

    # reduce acumula la suma de todos los subtotales
    recaudacion_total = functools.reduce(lambda acumulado, subtotal: acumulado + subtotal, subtotales, 0.0)

    print("\n=== RECAUDACIÓN TOTAL ===")
    print(f"Recaudación total proyectada: ${recaudacion_total:,.2f}")
    return recaudacion_total


def reporte_habitaciones_libres(matriz_hotel, lista_huespedes):
    """
    Reporte de habitaciones libres usando operaciones de conjuntos.
    - todas: set con todos los numeros de habitacion del hotel.
    - ocupadas: set con los numeros de habitacion ocupadas.
    - libres = todas - ocupadas   (diferencia)
    - comunes = todas & ocupadas   (interseccion)

    >>> matriz = [["O", "L"]]
    >>> lista = [{"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    >>> res = reporte_habitaciones_libres(matriz, lista)
    <BLANKLINE>
    === REPORTE DE HABITACIONES LIBRES ===
    Total de habitaciones: 2
    Habitaciones ocupadas: {101}
    Habitaciones libres: {102}
    >>> res == {102}
    True
    """
    # Todas las habitaciones del hotel
    todas = set()
    for piso in range(len(matriz_hotel)):
        for hab in range(len(matriz_hotel[piso])):
            num = (piso + 1) * 100 + (hab + 1)
            todas.add(num)

    # Habitaciones ocupadas
    ocupadas = set()
    for huesped in lista_huespedes:
        ocupadas.add(huesped["ubicacion"][2])

    # Diferencia: libres = todas - ocupadas
    libres = todas - ocupadas

    # Interseccion: ocupadas que existen en el hotel
    comunes = todas & ocupadas

    print("\n=== REPORTE DE HABITACIONES LIBRES ===")
    print("Total de habitaciones:", len(todas))
    print("Habitaciones ocupadas:", comunes)
    if len(libres) == 0:
        print("Habitaciones libres: ninguna (hotel completo)")
    else:
        print("Habitaciones libres:", libres)
    return libres


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
