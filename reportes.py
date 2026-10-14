# =============================================================================
# MÓDULO DE REPORTES Y PROGRAMACIÓN FUNCIONAL (reportes.py)
# =============================================================================
# Responsabilidad: Métricas del hotel, porcentaje de ocupación, desglose de estados
# (Libre, Ocupada, Limpieza, Mantenimiento), facturación proyectada y recaudación total
# aplicando el paradigma de programación funcional:
# map, filter, functools.reduce y funciones anónimas lambda.
# =============================================================================

import functools
from tarifas import obtener_tarifa_habitacion


def generar_reporte_ocupacion(matriz_hotel):
    """
    Genera un reporte analítico integral que muestra el total de habitaciones,
    el desglose por estado (Ocupadas, Libres, En Limpieza, En Mantenimiento)
    y el porcentaje exacto de ocupación del hotel.
    Utiliza functools.reduce y map con lambdas.
    """
    # 1. Total de habitaciones acumulando el largo de cada fila mediante reduce
    total_habitaciones = functools.reduce(
        lambda acumulado, fila: acumulado + len(fila),
        matriz_hotel,
        0
    )

    # 2. Conteo funcional por estados usando map y reduce
    contar_estado = lambda estado: functools.reduce(
        lambda acum, fila: acum + functools.reduce(
            lambda sub, hab: sub + (1 if hab == estado else 0),
            fila,
            0
        ),
        matriz_hotel,
        0
    )

    habitaciones_ocupadas = contar_estado("O")
    habitaciones_libres = contar_estado("L")
    habitaciones_limpieza = contar_estado("S")
    habitaciones_mantenimiento = contar_estado("M")

    # 3. Cálculo porcentual seguro contra división por cero
    if total_habitaciones > 0:
        porcentaje_ocupacion = (habitaciones_ocupadas * 100.0) / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = round(porcentaje_ocupacion, 2)

    print("\n" + "=" * 52)
    print("          REPORTE ANALÍTICO DE OCUPACIÓN Y ESTADOS       ")
    print("=" * 52)
    print(f"Total de habitaciones:       {total_habitaciones}")
    print(f"- Habitaciones Ocupadas [O]: {habitaciones_ocupadas}")
    print(f"- Habitaciones Libres   [L]: {habitaciones_libres}")
    print(f"- En Limpieza           [S]: {habitaciones_limpieza}")
    print(f"- En Mantenimiento      [M]: {habitaciones_mantenimiento}")
    print("-" * 52)
    print(f"Porcentaje de ocupación:     {porcentaje_ocupacion}%")
    print("=" * 52)


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a facturar por un huésped específico.
    Soporta la estructura moderna con tuplas inmutables:
    huesped = [(dni, nombre), (piso, habitacion, num_comercial), dias, consumos_extras]
    así como estructuras planas anteriores por compatibilidad.
    Aplica una función anónima (lambda) con 10% de bonificación para estadías mayores a 7 noches
    e incorpora los consumos extras acumulados (Minibar, servicios).
    Retorna el subtotal neto calculado en punto flotante.
    """
    if isinstance(huesped[0], (tuple, list)):
        # Tuplas inmutables: huesped[1] es (piso, habitacion, num_comercial)
        piso = int(huesped[1][0])
        dias = int(huesped[2])
        consumos_extras = float(huesped[3]) if len(huesped) > 3 else 0.0
    else:
        # Formato plano histórico
        dias = int(huesped[2])
        piso = int(huesped[3])
        consumos_extras = float(huesped[6]) if len(huesped) > 6 else 0.0

    piso_comercial = piso + 1

    precio_noche = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
    subtotal_estadia = precio_noche * dias

    # Descuento del 10% para estadías prolongadas (> 7 noches)
    aplicar_descuento = lambda d, monto: monto * 0.9 if d > 7 else monto
    estadia_neta = aplicar_descuento(dias, subtotal_estadia)

    subtotal_total = estadia_neta + consumos_extras
    return subtotal_total


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

    print("\n" + "=" * 52)
    print("            RECAUDACIÓN TOTAL PROYECTADA         ")
    print("=" * 52)
    print(f"Huéspedes facturados:        {len(lista_huespedes)}")
    print(f"Recaudación total:           ${recaudacion_total:,.2f}")
    print("=" * 52)

    return recaudacion_total
