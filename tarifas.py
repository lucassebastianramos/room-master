# =============================================================================
# MÓDULO DE TARIFAS Y PRECIOS (tarifas.py)
# =============================================================================

from validaciones import (
    validar_generico,
    solicitar_dimension_valida,
    solicitar_confirmacion,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)


def solicitar_precio_base():
    """
    Solicita y valida el precio base por noche del hotel.
    """
    precio_base_valido = False
    precio_base = 0.0

    while not precio_base_valido:
        precio_base = float(validar_generico(
            "Ingrese el precio base por noche del hotel ($): ",
            PATRON_NUMERO_VALIDO,
            ERROR_NUMERO
        ))
        if precio_base > 0:
            precio_base_valido = True
        else:
            print("Error: El precio base debe ser mayor a 0.")

    return precio_base


def solicitar_configuracion_lujo(total_pisos):
    """
    Solicita al usuario el tipo de segmentación que desea tener en los pisos lujosos.
    Retorna una tupla: (piso_lujo_desde, recargo_porcentaje)
    """
    piso_lujo_desde = total_pisos + 1
    recargo_porcentaje = 0.0

    if total_pisos > 1:
        quiere_lujo = solicitar_confirmacion(
            "¿Desea segmentar pisos como lujosos/suites con tarifa diferenciada? (s/n): "
        )
        if quiere_lujo:
            piso_lujo_desde = solicitar_dimension_valida(
                f"¿A partir de qué piso se consideran de lujo? (2 a {total_pisos}): ",
                2,
                total_pisos
            )
            recargo_porcentaje = float(validar_generico(
                "¿Qué porcentaje más caras serán las habitaciones de lujo? (ej: 30 o 50): ",
                PATRON_NUMERO_VALIDO,
                ERROR_NUMERO
            ))

    return piso_lujo_desde, recargo_porcentaje


def capturar_parametros_tarifas(total_pisos):
    """
    Invoca las funciones especificas del precio base, y el recargo de los pisos lujosos
    """
    precio_base = solicitar_precio_base()
    piso_lujo_desde, recargo_porcentaje = solicitar_configuracion_lujo(total_pisos)
    return precio_base, piso_lujo_desde, recargo_porcentaje


def generar_matriz_tarifas(total_pisos, precio_base, piso_lujo_desde, recargo_porcentaje):
    """
    Genera y retorna la matriz de tarifas por piso.
    """
    matriz_tarifas = []
    for p in range(1, total_pisos + 1):
        if p >= piso_lujo_desde:
            precio_calculado = precio_base * (1 + recargo_porcentaje / 100.0)
            precio_piso = int(precio_calculado * 100 + 0.5) / 100.0
        else:
            precio_piso = int(precio_base * 100 + 0.5) / 100.0
        matriz_tarifas.append([p, precio_piso])

    return matriz_tarifas


def configurar_tarifas_hotel(total_pisos):
    """
    Función principal del módulo para configurar las tarifas
    """
    print("\n" + "=" * 45)
    print("      CONFIGURACIÓN DE TARIFAS DEL HOTEL     ")
    print("=" * 45)

    precio_base, piso_lujo_desde, recargo_porcentaje = capturar_parametros_tarifas(total_pisos)
    matriz_tarifas = generar_matriz_tarifas(
        total_pisos, precio_base, piso_lujo_desde, recargo_porcentaje
    )

    mostrar_resumen_tarifas(matriz_tarifas, piso_lujo_desde)
    input("\nPresione [Enter] para continuar...")

    return matriz_tarifas


def mostrar_resumen_tarifas(matriz_tarifas, piso_lujo_desde=0):
    """
    Imprime en consola el esquema de precios vigente por piso.
    """
    print("\n--- ESQUEMA DE TARIFAS VIGENTES ---")
    if len(matriz_tarifas) == 0:
        print("No hay tarifas configuradas.")
    else:
        for p, precio in matriz_tarifas:
            if piso_lujo_desde > 0 and p >= piso_lujo_desde:
                tipo = " (Suite / Lujo)"
            else:
                tipo = " (Estándar)"
            print(f"Piso {p}{tipo}: ${precio:,.2f} por noche")
    print("=" * 45)


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    """
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            return matriz_tarifas[i][1]

    if piso == 0 and len(matriz_tarifas) > 0:
        return matriz_tarifas[0][1]

    if len(matriz_tarifas) > 0:
        return matriz_tarifas[-1][1]

    return 0.0