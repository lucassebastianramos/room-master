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
    Devuelve -1 si el usuario cancela.
    """
    precio_base_valido = False
    precio_base = 0.0

    while precio_base_valido == False:
        dato = validar_generico(
            "Ingrese el precio base por noche del hotel ($) (-1 para cancelar): ",
            PATRON_NUMERO_VALIDO,
            ERROR_NUMERO
        )
        if dato == "-1":
            return -1

        precio_base = float(dato)
        if precio_base > 0:
            precio_base_valido = True
        else:
            print("Error: El precio base debe ser mayor a 0.")

    return precio_base


def solicitar_configuracion_lujo(total_pisos):
    """
    Solicita la segmentación de pisos lujosos.
    Devuelve (piso_lujo_desde, recargo_porcentaje) o (-1, -1) si se cancela.
    """
    piso_lujo_desde = total_pisos + 1
    recargo_porcentaje = 0.0

    if total_pisos > 1:
        quiere_lujo = solicitar_confirmacion(
            "¿Desea segmentar pisos como lujosos/suites con tarifa diferenciada? (s/n) (-1 para cancelar): "
        )
        if quiere_lujo == "-1":
            return -1, -1

        if quiere_lujo == True:
            piso_lujo_desde = solicitar_dimension_valida(
                f"¿A partir de qué piso se consideran de lujo? (2 a {total_pisos}) (-1 para cancelar): ",
                2,
                total_pisos
            )
            if piso_lujo_desde == -1:
                return -1, -1

            recargo = validar_generico(
                "¿Qué porcentaje más caras serán las habitaciones de lujo? (ej: 30 o 50) (-1 para cancelar): ",
                PATRON_NUMERO_VALIDO,
                ERROR_NUMERO
            )
            if recargo == "-1":
                return -1, -1

            recargo_porcentaje = float(recargo)

    return piso_lujo_desde, recargo_porcentaje


def capturar_parametros_tarifas(total_pisos):
    """
    Reúne el precio base y la configuración de pisos lujosos.
    Devuelve (-1, -1, -1) si el usuario cancela.
    """
    precio_base = solicitar_precio_base()
    if precio_base == -1:
        return -1, -1, -1

    configuracion = solicitar_configuracion_lujo(total_pisos)
    if configuracion == (-1, -1):
        return -1, -1, -1

    piso_lujo_desde, recargo_porcentaje = configuracion
    return precio_base, piso_lujo_desde, recargo_porcentaje


def generar_dict_tarifas(total_pisos, precio_base, piso_lujo_desde, recargo_porcentaje):
    """
    Genera y retorna las tarifas por piso como diccionario {piso: precio}.
    """
    matriz_tarifas = {}
    for p in range(1, total_pisos + 1):
        if p >= piso_lujo_desde:
            precio_calculado = precio_base * (1 + recargo_porcentaje / 100.0)
            precio_piso = int(precio_calculado * 100 + 0.5) / 100.0
        else:
            precio_piso = int(precio_base * 100 + 0.5) / 100.0
        matriz_tarifas[p] = precio_piso

    return matriz_tarifas


def configurar_tarifas_hotel(total_pisos):
    """
    Función principal del módulo para configurar las tarifas.
    Devuelve -1 si el usuario cancela.
    """
    print("\n" + "=" * 45)
    print("      CONFIGURACIÓN DE TARIFAS DEL HOTEL     ")
    print("=" * 45)

    parametros = capturar_parametros_tarifas(total_pisos)
    if parametros == (-1, -1, -1):
        return -1

    precio_base, piso_lujo_desde, recargo_porcentaje = parametros
    matriz_tarifas = generar_dict_tarifas(
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
        for piso in matriz_tarifas:
            precio = matriz_tarifas[piso]
            if piso_lujo_desde > 0 and piso >= piso_lujo_desde:
                tipo = " (Suite / Lujo)"
            else:
                tipo = " (Estándar)"
            print(f"Piso {piso}{tipo}: ${precio:,.2f} por noche")
    print("=" * 45)


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    Trabaja exclusivamente con diccionario {piso: precio}.
    """
    # Buscar el piso exacto
    if piso in matriz_tarifas:
        return matriz_tarifas[piso]

    # Fallback: si no existe, usar el primer valor (piso 0) o el último
    if len(matriz_tarifas) == 0:
        return 0.0

    valores = []
    for precio in matriz_tarifas.values():
        valores.append(precio)

    if piso == 0:
        return valores[0]
    return valores[-1]