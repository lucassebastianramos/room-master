# =============================================================================
# MÓDULO DE REPORTES Y PROGRAMACIÓN FUNCIONAL (reportes.py)
# =============================================================================
# Responsabilidad: Métricas del hotel, porcentaje de ocupación, facturación
# proyectada y recaudación total aplicando el paradigma de programación funcional:
# map, filter, functools.reduce y funciones anónimas lambda.
# =============================================================================

import functools
from tarifas import obtener_tarifa_habitacion


def generar_reporte_ocupacion(matriz_hotel):
    """
    Genera un reporte analítico que muestra el total de habitaciones,
    las que se encuentran ocupadas ('O') y el porcentaje de ocupación del hotel.
    Utiliza functools.reduce y map con lambdas.
    """
    # 1. Total de habitaciones acumulando el largo de cada fila mediante reduce
    total_habitaciones = functools.reduce(
        lambda acumulado, fila: acumulado + len(fila),
        matriz_hotel,
        0
    )

    # 2. Cuenta las habitaciones ocupadas en cada fila usando reduce mapeado
    ocupadas_por_fila = map(
        lambda fila: functools.reduce(
            lambda acum, hab: acum + (1 if hab == "O" else 0),
            fila,
            0
        ),
        matriz_hotel
    )

    # 3. Acumula los subtotales de cada fila para obtener el gran total ocupado
    habitaciones_ocupadas = functools.reduce(
        lambda acumulado, cant: acumulado + cant,
        ocupadas_por_fila,
        0
    )

    # 4. Cálculo porcentual seguro contra división por cero
    if total_habitaciones > 0:
        porcentaje_ocupacion = (habitaciones_ocupadas * 100.0) / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = round(porcentaje_ocupacion, 2)

    print("\n" + "=" * 40)
    print("        REPORTE DE OCUPACIÓN DEL HOTEL    ")
    print("=" * 40)
    print(f"Total de habitaciones:    {total_habitaciones}")
    print(f"Habitaciones ocupadas:    {habitaciones_ocupadas}")
    print(f"Porcentaje de ocupación:  {porcentaje_ocupacion}%")
    print("=" * 40)


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a facturar por un huésped específico.
    Aplica una función anónima (lambda) con 10% de bonificación para estadías mayores a 7 noches.
    Retorna el subtotal calculado en punto flotante.
    """
    dias = int(huesped[2])
    piso = int(huesped[3])
    piso_comercial = piso + 1

    precio_noche = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
    subtotal_bruto = precio_noche * dias

    # Descuento del 10% para estadías prolongadas (> 7 noches)
    aplicar_descuento = lambda d, monto: monto * 0.9 if d > 7 else monto
    subtotal_neto = aplicar_descuento(dias, subtotal_bruto)

    return subtotal_neto


def calcular_recaudacion_total(lista_huespedes, matriz_tarifas):
    """
    Calcula y muestra la recaudación total proyectada del hotel.
    Utiliza:
    - map para transformar la lista de huéspedes a lista de montos individuales.
    - reduce para consolidar la suma total de los importes.
    """
    if len(lista_huespedes) == 0:
        print("\n=== RECAUDACIÓN TOTAL ===")
        print("Recaudación total: $0.00 (sin huéspedes registrados)")
        return 0.0

    # Transformación con map: convierte cada registro de huésped en su monto subtotal
    subtotales = list(map(
        lambda huesped: calcular_subtotal(huesped, matriz_tarifas),
        lista_huespedes
    ))

    # Acumulación con reduce: suma los subtotales generados
    recaudacion_total = functools.reduce(
        lambda acumulado, subtotal: acumulado + subtotal,
        subtotales,
        0.0
    )

    print("\n" + "=" * 40)
    print("         RECAUDACIÓN TOTAL PROYECTADA     ")
    print("=" * 40)
    print(f"Huéspedes facturados:     {len(lista_huespedes)}")
    print(f"Recaudación total:        ${recaudacion_total:,.2f}")
    print("=" * 40)

    return recaudacion_total
