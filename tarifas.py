# =============================================================================
# MÓDULO DE TARIFAS Y REGLAS DE NEGOCIO (tarifas.py)
# =============================================================================
# Responsabilidad: Esquema de precios por piso, segmentación dinámica de suites/lujo,
# precios dinámicos por oferta/demanda y políticas de negocio configurables por el Admin.
# =============================================================================

from validaciones import (
    validar_generico,
    solicitar_dimension_valida,
    confirmar_accion,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)

# Diccionario integral de reglas de negocio configurables
REGLAS_NEGOCIO_DEFAULT = {
    "permitir_autoregistro": True,         # Si es False, el hotel opera solo por mostrador/recepción
    "permitir_reserva_terceros": True,     # Si los huéspedes pueden reservar para terceros
    "oferta_demanda_activa": False,        # Precios dinámicos por alta demanda
    "umbral_ocupacion_demanda": 70.0,      # % de ocupación a partir del cual rige alta demanda
    "recargo_oferta_demanda": 20.0,        # % de recargo aplicado sobre la tarifa por alta demanda
    "max_dias_estadia": 30,                # Límite máximo de estadía permitido por reserva
    "descuento_cliente_frecuente": 5.0     # % de descuento por fidelidad a usuarios registrados
}


def configurar_tarifas_hotel(total_pisos):
    """
    Permite configurar dinámicamente las tarifas del hotel por piso.
    Permite definir un precio base general y segmentar pisos superiores como lujosos/suites con recargo.
    Retorna una matriz de tarifas: [[piso, precio_base], ...] donde piso va de 1 a total_pisos.
    """
    print("\n" + "=" * 45)
    print("      CONFIGURACIÓN DE TARIFAS DEL HOTEL     ")
    print("=" * 45)

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
    piso_lujo_desde = total_pisos + 1
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

    for p in range(1, total_pisos + 1):
        if p >= piso_lujo_desde:
            precio_piso = round(precio_base * (1 + recargo_porcentaje / 100.0), 2)
        else:
            precio_piso = round(precio_base, 2)
        matriz_tarifas.append([p, precio_piso])

    mostrar_resumen_tarifas(matriz_tarifas, piso_lujo_desde)
    input("\nPresione [Enter] para continuar...")

    return matriz_tarifas


def mostrar_resumen_tarifas(matriz_tarifas, piso_lujo_desde=None):
    """
    Imprime en consola el esquema de precios vigente por piso.
    """
    print("\n--- ESQUEMA DE TARIFAS VIGENTES ---")
    for p, precio in matriz_tarifas:
        tipo = ""
        if piso_lujo_desde is not None and p >= piso_lujo_desde:
            tipo = " (Suite / Lujo)"
        elif piso_lujo_desde is not None:
            tipo = " (Estándar)"
        print(f"Piso {p}{tipo}: ${precio:,.2f} por noche")
    print("=" * 45)


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel (1-indexed).
    """
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            return matriz_tarifas[i][1]

    if piso == 0 and len(matriz_tarifas) > 0:
        return matriz_tarifas[0][1]

    if len(matriz_tarifas) > 0:
        return matriz_tarifas[-1][1]

    return 0.0


def calcular_tarifa_dinamica(piso, matriz_tarifas, ocupacion_pct=0.0, reglas_negocio=None):
    """
    Calcula la tarifa aplicable a una habitación teniendo en cuenta las reglas
    de negocio activas (por ejemplo: aumento de tarifa por oferta/demanda).
    Retorna una tupla: (tarifa_final, aplico_demanda).
    """
    tarifa_base = float(obtener_tarifa_habitacion(piso, matriz_tarifas))

    if reglas_negocio is None:
        return tarifa_base, False

    oferta_activa = reglas_negocio.get("oferta_demanda_activa", False)
    umbral = reglas_negocio.get("umbral_ocupacion_demanda", 70.0)
    recargo_pct = reglas_negocio.get("recargo_oferta_demanda", 20.0)

    if oferta_activa and ocupacion_pct >= umbral:
        tarifa_con_recargo = round(tarifa_base * (1 + recargo_pct / 100.0), 2)
        return tarifa_con_recargo, True

    return tarifa_base, False


def menu_configuracion_reglas_negocio(matriz_tarifas, reglas_negocio, total_pisos):
    """
    Panel interactivo donde el Administrador puede ajustar todas las políticas del hotel:
    1. Reconfigurar tarifas por piso o eliminar/activar segmentación de lujo.
    2. Activar/Desactivar aumentos por oferta y demanda (y calibrar % de recargo).
    3. Habilitar/Deshabilitar reservas para terceros por huéspedes.
    4. Conmutar modo de operación del hotel (Permitir/Bloquear autorregistro online).
    5. Configurar límite máximo de estadía permitida.
    """
    ejecutando = True

    while ejecutando:
        print("\n" + "=" * 60)
        print("        PANEL DE REGLAS DE NEGOCIO Y TARIFAS (ADMIN)        ")
        print("=" * 60)
        print("1. Reconfigurar tarifas base y suites/lujo")
        print(f"2. Modo de Operación: [{'HÍBRIDO (Portal Online Activo)' if reglas_negocio['permitir_autoregistro'] else 'RECEPCIÓN EXCLUSIVA (Solo Mostrador)'}]")
        print(f"3. Precios por Oferta/Demanda: [{'ACTIVO' if reglas_negocio['oferta_demanda_activa'] else 'INACTIVO'}]")
        print(f"   (Umbral: {reglas_negocio['umbral_ocupacion_demanda']}% ocupación | Recargo: +{reglas_negocio['recargo_oferta_demanda']}%)")
        print(f"4. Reservas para terceros por huéspedes: [{'PERMITIDO' if reglas_negocio['permitir_reserva_terceros'] else 'DESHABILITADO'}]")
        print(f"5. Estadía máxima permitida: [{reglas_negocio['max_dias_estadia']} días]")
        print("6. Ver resumen de todas las reglas y tarifas activas")
        print("0. Volver al panel de administración")
        print("=" * 60)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevas_tarifas = configurar_tarifas_hotel(total_pisos)
            matriz_tarifas.clear()
            for fila in nuevas_tarifas:
                matriz_tarifas.append(fila)
            print("\n[Éxito] Tarifas del hotel actualizadas.")

        elif opcion == "2":
            reglas_negocio["permitir_autoregistro"] = not reglas_negocio["permitir_autoregistro"]
            nuevo = "HÍBRIDO (Autorregistro habilitado)" if reglas_negocio["permitir_autoregistro"] else "EXCLUSIVO MOSTRADOR (Solo recepción registra)"
            print(f"\n[Éxito] Modo de operación configurado a: {nuevo}.")

        elif opcion == "3":
            reglas_negocio["oferta_demanda_activa"] = not reglas_negocio["oferta_demanda_activa"]
            nuevo = "ACTIVADO" if reglas_negocio["oferta_demanda_activa"] else "DESACTIVADO"
            print(f"\n[Éxito] Régimen de precios por Oferta/Demanda: {nuevo}.")

            if reglas_negocio["oferta_demanda_activa"]:
                if confirmar_accion("¿Desea cambiar los parámetros de umbral y recargo? (s/n): "):
                    umbral = float(validar_generico("Ingrese el % de ocupación mínimo (ej: 70): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
                    recargo = float(validar_generico("Ingrese el % de aumento por alta demanda (ej: 25): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
                    reglas_negocio["umbral_ocupacion_demanda"] = umbral
                    reglas_negocio["recargo_oferta_demanda"] = recargo
                    print("\n[Éxito] Parámetros de oferta/demanda actualizados.")

        elif opcion == "4":
            reglas_negocio["permitir_reserva_terceros"] = not reglas_negocio["permitir_reserva_terceros"]
            nuevo = "PERMITIDAS" if reglas_negocio["permitir_reserva_terceros"] else "DESHABILITADAS"
            print(f"\n[Éxito] Reservas para terceros: {nuevo}.")

        elif opcion == "5":
            max_dias = int(validar_generico("Ingrese la cantidad máxima de días de estadía (ej: 30): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
            if max_dias > 0:
                reglas_negocio["max_dias_estadia"] = max_dias
                print(f"\n[Éxito] Estadía máxima fijada en {max_dias} días.")
            else:
                print("Error: Los días deben ser mayores a 0.")

        elif opcion == "6":
            print("\n=== RESUMEN DE POLÍTICAS DEL HOTEL ===")
            print(f"- Autorregistro de usuarios: {'HABILITADO' if reglas_negocio['permitir_autoregistro'] else 'BLOQUEADO (Solo Mostrador)'}")
            print(f"- Reservas de terceros:      {'PERMITIDAS' if reglas_negocio['permitir_reserva_terceros'] else 'DESHABILITADAS'}")
            print(f"- Precios Oferta/Demanda:    {'ACTIVA' if reglas_negocio['oferta_demanda_activa'] else 'INACTIVA'}")
            print(f"  * Umbral de ocupación:     {reglas_negocio['umbral_ocupacion_demanda']}%")
            print(f"  * Recargo aplicado:        +{reglas_negocio['recargo_oferta_demanda']}%")
            print(f"- Estadía máxima permitida:  {reglas_negocio['max_dias_estadia']} días")
            print(f"- Descuento cliente fiel:    {reglas_negocio['descuento_cliente_frecuente']}%")
            mostrar_resumen_tarifas(matriz_tarifas)

        elif opcion == "0":
            ejecutando = False
        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")
