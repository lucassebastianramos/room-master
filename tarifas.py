# =============================================================================
# MÓDULO DE TARIFAS Y SEGMENTACIÓN POR PISOS (tarifas.py)
# =============================================================================
# Responsabilidad: Configuración dinámica de la matriz de tarifas por piso,
# segmentación de suites/lujo con recargo y consulta de precios por noche.
# =============================================================================

from validaciones import (
    validar_generico,
    solicitar_dimension_valida,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)


def configurar_tarifas_hotel(total_pisos):
    """
    Permite configurar dinámicamente las tarifas del hotel por piso.
    Permite definir un precio base general y segmentar pisos superiores como lujosos/suites con recargo.
    Retorna una matriz de tarifas: [[piso, precio_base], ...] donde piso va de 1 a total_pisos.
    """
    print("\n" + "=" * 45)
    print("      CONFIGURACIÓN DE TARIFAS DEL HOTEL     ")
    print("=" * 45)

    # 1. Precio base general
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

    matriz_tarifas = []

    # 2. Si el hotel tiene más de un piso, permitir segmentación de pisos lujosos
    piso_lujo_desde = total_pisos + 1  # Por defecto, sin pisos de lujo
    recargo_porcentaje = 0.0

    if total_pisos > 1:
        tiene_lujo_valido = False
        tiene_lujo = ""

        while not tiene_lujo_valido:
            tiene_lujo = input("¿Desea segmentar pisos como lujosos/suites con tarifa diferenciada? (s/n): ").strip().lower()
            if tiene_lujo in ["s", "si", "sí", "n", "no"]:
                tiene_lujo_valido = True
            else:
                print("Opción inválida. Ingrese 's' o 'n'.")

        if tiene_lujo in ["s", "si", "sí"]:
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

    # 3. Construir la lista de tarifas para cada piso (de 1 a total_pisos)
    for p in range(1, total_pisos + 1):
        if p >= piso_lujo_desde:
            precio_piso = round(precio_base * (1 + recargo_porcentaje / 100.0), 2)
        else:
            precio_piso = round(precio_base, 2)
        matriz_tarifas.append([p, precio_piso])

    # 4. Mostrar resumen de tarifas
    print("\n--- ESQUEMA DE TARIFAS CONFIGURADO ---")
    for p, precio in matriz_tarifas:
        tipo = "Suite / Lujo" if p >= piso_lujo_desde else "Estándar"
        print(f"Piso {p} ({tipo}): ${precio:,.2f} por noche")
    print("=" * 45)
    input("\nPresione [Enter] para continuar...")

    return matriz_tarifas


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    matriz_tarifas tiene pares: [piso, precio_base] (piso 1-indexed: 1, 2, 3...)
    """
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            return matriz_tarifas[i][1]

    # Soporte por si se pasa piso en formato índice de matriz (0 para Piso 1)
    if piso == 0 and len(matriz_tarifas) > 0:
        return matriz_tarifas[0][1]

    # Fallback al último piso si excede el rango
    if len(matriz_tarifas) > 0:
        return matriz_tarifas[-1][1]

    return 0.0
