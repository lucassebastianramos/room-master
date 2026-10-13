# =============================================================================
# MÓDULO DE GESTIÓN DE HUÉSPEDES (huespedes.py)
# =============================================================================
# Responsabilidad: Ciclo de vida y transacciones de los huéspedes del hotel:
# Check-in inteligente (propio o terceros), confirmaciones explícitas con resumen,
# cancelaciones seguras con '0', cargos de consumos extras (Minibar, Cochera),
# extensión de estadía, Check-out con liquidación detallada, Swap y limpieza.
# =============================================================================

from validaciones import (
    validar_generico_con_cancelacion,
    confirmar_accion,
    PATRON_NUMERO_VALIDO,
    PATRON_DNI_VALIDO,
    PATRON_TEXTO_VALIDO,
    PATRON_DIAS_VALIDO,
    ERROR_NUMERO,
    ERROR_DNI,
    ERROR_TEXTO,
    ERROR_DIAS
)
from hotel import (
    obtener_numero_comercial,
    obtener_indices_matriz,
    solicitar_habitacion_libre,
    hay_habitaciones_disponibles
)
from tarifas import (
    obtener_tarifa_habitacion,
    calcular_tarifa_dinamica
)

try:
    from persistencia import registrar_evento_auditoria
except ImportError:
    def registrar_evento_auditoria(operador, accion, detalle):
        return True


def realizar_checkin(matriz, lista_huespedes, matriz_tarifas=None, sesion=None, reglas_negocio=None):
    """
    Gestiona el registro de un nuevo huésped en el hotel:
    - Previene bucle si el hotel está 100% ocupado.
    - Soporta reservas propias o para terceros si la política lo permite.
    - Valida el límite de estadía máxima configurado.
    - Calcula la tarifa dinámica estimada (considerando alta demanda si rige).
    - Muestra resumen completo y solicita confirmación explícita (s/n) antes de registrar.
    Estructura de registro: [nombre, dni, dias, piso, habitacion, num_comercial, consumos_extras].
    """
    if not hay_habitaciones_disponibles(matriz):
        print("\n[Aviso] El hotel se encuentra 100% completo. No hay habitaciones libres disponibles.")
        return matriz

    piso, habitacion = solicitar_habitacion_libre(matriz)
    if piso is None:
        return matriz

    num_comercial = obtener_numero_comercial(piso, habitacion)
    nombre = None
    dni = None

    # Determinación del huésped titular según el rol de la sesión activa
    if sesion is not None and sesion[1] == "huesped":
        nombre_sesion = sesion[2]
        dni_sesion = sesion[3] if len(sesion) > 3 else ""
        permitir_terceros = True if reglas_negocio is None else reglas_negocio.get("permitir_reserva_terceros", True)

        if permitir_terceros:
            print(f"\nTitular de la cuenta: {nombre_sesion} (DNI: {dni_sesion if dni_sesion else 'No registrado'})")
            es_para_si_mismo = input("¿La reserva es para usted mismo? (s/n, o 0 para cancelar): ").strip().lower()

            if es_para_si_mismo in ["0", "cancelar"]:
                print("[Operación cancelada] Regresando al menú...")
                return matriz

            if es_para_si_mismo in ["s", "si", "sí"]:
                nombre = nombre_sesion
                if dni_sesion:
                    dni = dni_sesion
                else:
                    dni = validar_generico_con_cancelacion("Ingrese su DNI: ", PATRON_DNI_VALIDO, ERROR_DNI)
                    if dni is None:
                        return matriz
            else:
                print("\n--- DATOS DE LA PERSONA A HOSPEDAR ---")
                nombre = validar_generico_con_cancelacion("Nombre completo del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
                if nombre is None:
                    return matriz
                dni = validar_generico_con_cancelacion("DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
                if dni is None:
                    return matriz
        else:
            print(f"\n[Política del Hotel] Las reservas online deben realizarse a nombre del titular ({nombre_sesion}).")
            nombre = nombre_sesion
            if dni_sesion:
                dni = dni_sesion
            else:
                dni = validar_generico_con_cancelacion("Ingrese su DNI: ", PATRON_DNI_VALIDO, ERROR_DNI)
                if dni is None:
                    return matriz
    else:
        print("\n--- DATOS DEL HUÉSPED ---")
        nombre = validar_generico_con_cancelacion("Nombre completo del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
        if nombre is None:
            return matriz

        dni = validar_generico_con_cancelacion("DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
        if dni is None:
            return matriz

    # Límite máximo de estadía configurado por la administración
    max_dias = reglas_negocio.get("max_dias_estadia", 30) if reglas_negocio else 30

    dias_validos = False
    dias = 0
    while not dias_validos:
        dias_str = validar_generico_con_cancelacion(
            f"Cantidad de días de estadía (máximo {max_dias} días): ",
            PATRON_DIAS_VALIDO,
            ERROR_DIAS
        )
        if dias_str is None:
            return matriz
        dias_candidatos = int(dias_str)
        if dias_candidatos <= max_dias:
            dias = dias_candidatos
            dias_validos = True
        else:
            print(f"Error: La estadía máxima permitida por el hotel es de {max_dias} días.")

    # Cálculo tarifario y detección de alta demanda
    total_hab = len(matriz) * len(matriz[0])
    ocupadas = sum(1 for fila in matriz for h in fila if h == "O")
    ocupacion_pct = (ocupadas * 100.0) / total_hab if total_hab > 0 else 0.0

    if matriz_tarifas is not None:
        tarifa_noche, aplico_demanda = calcular_tarifa_dinamica(
            piso + 1,
            matriz_tarifas,
            ocupacion_pct,
            reglas_negocio
        )
    else:
        tarifa_noche, aplico_demanda = 0.0, False

    total_estimado = tarifa_noche * dias

    # Resumen y confirmación previa de la operación
    print("\n" + "=" * 52)
    print("             CONFIRMACIÓN DE CHECK-IN             ")
    print("=" * 52)
    print(f"Huésped titular:      {nombre}")
    print(f"DNI:                  {dni}")
    print(f"Habitación asignada:  {num_comercial} (Piso {piso + 1})")
    print(f"Días de estadía:      {dias} noches")
    if matriz_tarifas is not None:
        demanda_txt = " (+ Recargo por Oferta/Demanda)" if aplico_demanda else ""
        print(f"Tarifa por noche:     ${tarifa_noche:,.2f}{demanda_txt}")
        print(f"Total estimado:       ${total_estimado:,.2f}")
    print("=" * 52)

    if not confirmar_accion("¿Confirma la reserva con estos datos? (s/n): "):
        print("\n[Operación cancelada] No se realizó el Check-in.")
        return matriz

    # Confirmación aceptada: inicializa consumos_extras en 0.0
    consumos_extras = 0.0
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial, consumos_extras]
    lista_huespedes.append(datos_huesped)
    matriz[piso][habitacion] = "O"

    operador_log = sesion[0] if sesion else "mostrador"
    registrar_evento_auditoria(operador_log, "CHECK-IN", f"{nombre} (DNI: {dni}) en hab {num_comercial} por {dias} noches")

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")
    return matriz


def cargar_consumo_habitacion(matriz_hotel, lista_huespedes):
    """
    Permite cargar consumos adicionales (Minibar, Cochera, Desayuno, Spa, etc.)
    a una habitación ocupada, para ser cobrados en la liquidación final de Check-out.
    """
    print("\n--- CARGAR CONSUMO EXTRA A HABITACIÓN ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes registrados actualmente en el hotel.")
        return

    num_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación (o 0 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if num_str is None:
        return
    num_hab = int(num_str)

    for huesped in lista_huespedes:
        piso, hab = int(huesped[3]), int(huesped[4])
        num_comercial = obtener_numero_comercial(piso, hab)

        if num_comercial == num_hab:
            print(f"\nHuésped alojado: {huesped[0]} (DNI: {huesped[1]})")
            concepto = input("Concepto del consumo (ej: Minibar, Cochera, Room Service): ").strip()
            if not concepto:
                concepto = "Consumo general"

            monto_str = validar_generico_con_cancelacion(
                "Ingrese el monto del consumo ($): ",
                PATRON_NUMERO_VALIDO,
                ERROR_NUMERO
            )
            if monto_str is None:
                return
            monto = float(monto_str)

            print("\n=== RESUMEN DEL CONSUMO EXTRA ===")
            print(f"Habitación:  {num_comercial}")
            print(f"Huésped:     {huesped[0]}")
            print(f"Concepto:    {concepto}")
            print(f"Importe:     ${monto:,.2f}")
            print("=================================")

            if confirmar_accion("¿Confirma cargar este consumo a la habitación? (s/n): "):
                if len(huesped) > 6:
                    huesped[6] += monto
                else:
                    huesped.append(monto)
                registrar_evento_auditoria("operador", "CONSUMO_EXTRA", f"Hab {num_comercial} ({huesped[0]}): {concepto} ${monto:,.2f}")
                print(f"\n[Éxito] Se cargaron ${monto:,.2f} a la habitación {num_comercial}.")
                print(f"Total acumulado en extras: ${huesped[6]:,.2f}")
            else:
                print("\n[Operación cancelada] No se imputó el consumo.")
            return

    print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {num_hab}.")


def extender_estadia_huesped(matriz_hotel, lista_huespedes, reglas_negocio=None):
    """
    Permite prolongar los días de estadía de un huésped actualmente alojado
    sin necesidad de realizar un Check-out y Check-in adicional.
    """
    print("\n--- EXTENDER ESTADÍA DE HUÉSPED ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes registrados actualmente en el hotel.")
        return

    num_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación (o 0 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if num_str is None:
        return
    num_hab = int(num_str)

    max_dias = reglas_negocio.get("max_dias_estadia", 30) if reglas_negocio else 30

    for huesped in lista_huespedes:
        piso, hab = int(huesped[3]), int(huesped[4])
        num_comercial = obtener_numero_comercial(piso, hab)

        if num_comercial == num_hab:
            dias_actuales = int(huesped[2])
            print(f"\nHuésped: {huesped[0]} | Estadía contratada: {dias_actuales} noches.")

            adicional_str = validar_generico_con_cancelacion(
                "Cantidad de noches adicionales a extender: ",
                PATRON_DIAS_VALIDO,
                ERROR_DIAS
            )
            if adicional_str is None:
                return
            noches_extra = int(adicional_str)
            total_noches = dias_actuales + noches_extra

            if total_noches > max_dias:
                print(f"Error: La estadía total resultante ({total_noches} noches) supera el límite de {max_dias} días.")
                return

            print("\n=== CONFIRMACIÓN DE EXTENSIÓN ===")
            print(f"Huésped:             {huesped[0]}")
            print(f"Habitación:          {num_comercial}")
            print(f"Noches actuales:     {dias_actuales}")
            print(f"Noches a agregar:    +{noches_extra}")
            print(f"Nueva estadía total: {total_noches} noches")
            print("=================================")

            if confirmar_accion("¿Confirma la extensión de la estadía? (s/n): "):
                huesped[2] = total_noches
                registrar_evento_auditoria("operador", "EXTENDER_ESTADIA", f"Hab {num_comercial} ({huesped[0]}): +{noches_extra} noches (Total: {total_noches})")
                print(f"\n[Éxito] Estadía de {huesped[0]} extendida a {total_noches} noches.")
            else:
                print("\n[Operación cancelada] No se modificó la estadía.")
            return

    print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {num_hab}.")


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de huéspedes.
    Estructura de cada registro: [nombre, dni, dias, piso, habitacion, num_comercial, consumos_extras].
    """
    if dni_busqueda is None:
        return

    encontrado = False

    for i in range(len(lista_huespedes)):
        huesped = lista_huespedes[i]
        nombre = huesped[0]
        dni_actual = huesped[1]
        dias = huesped[2]
        piso = int(huesped[3])
        hab = int(huesped[4])
        extras = float(huesped[6]) if len(huesped) > 6 else 0.0

        num_comercial = huesped[5] if len(huesped) > 5 else obtener_numero_comercial(piso, hab)
        piso_real = piso + 1

        if str(dni_actual).strip() == str(dni_busqueda).strip():
            encontrado = True
            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print("Nombre:               ", nombre)
            print("DNI:                  ", dni_actual)
            print("Días de estadía:      ", dias)
            print("Piso asignado:        ", piso_real)
            print("Habitación:           ", num_comercial)
            if extras > 0:
                print(f"Consumos adicionales: ${extras:,.2f}")
            print("====================================")

    if not encontrado:
        print(f"\n[Aviso] No se encontró ningún huésped alojado con el DNI: {dni_busqueda}")


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Filtra los huéspedes de un piso específico utilizando 'filter' y 'lambda'.
    'piso_objetivo' representa el número comercial de piso (1 para primer piso, etc.).
    """
    indice_piso = int(piso_objetivo) - 1
    filtrados = list(filter(
        lambda huesped: int(huesped[3]) == indice_piso,
        lista_huespedes
    ))
    return filtrados


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas, reglas_negocio=None):
    """
    Procesa la salida de un huésped:
    - Solicita DNI con opción de cancelar con '0'.
    - Desglosa liquidación: Noches x Tarifa, Descuento estadía larga (>7 noches),
      Descuento cliente frecuente y Consumos adicionales (Minibar, extras).
    - Solicita confirmación explícita antes de liberar la habitación a 'S'.
    """
    print("\n--- CHECK-OUT ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes registrados actualmente en el hotel.")
        return

    dni_checkout = validar_generico_con_cancelacion(
        "Ingrese el DNI del huésped para check-out: ",
        PATRON_DNI_VALIDO,
        ERROR_DNI
    )
    if dni_checkout is None:
        return

    for huesped in lista_huespedes:
        if str(huesped[1]) == str(dni_checkout):
            nombre = huesped[0]
            dias = int(huesped[2])
            piso = huesped[3]
            habitacion = huesped[4]
            num_comercial = obtener_numero_comercial(piso, habitacion)

            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            subtotal_habitacion = tarifa * dias

            # Bonificación 10% por estadía larga (> 7 noches)
            descuento_larga = (subtotal_habitacion * 0.10) if dias > 7 else 0.0

            # Consumos extras acumulados (Minibar, cochera, etc.)
            consumos_extras = float(huesped[6]) if len(huesped) > 6 else 0.0

            total_a_liquidar = (subtotal_habitacion - descuento_larga) + consumos_extras

            print("\n" + "=" * 54)
            print("             LIQUIDACIÓN FINAL DE CHECK-OUT       ")
            print("=" * 54)
            print(f"Huésped:                 {nombre}")
            print(f"DNI:                     {dni_checkout}")
            print(f"Habitación liberada:     {num_comercial} (Piso {piso_comercial})")
            print(f"Estadía:                 {dias} noches @ ${tarifa:,.2f}/noche")
            print(f"Subtotal de habitación:  ${subtotal_habitacion:,.2f}")
            if descuento_larga > 0:
                print(f"Descuento estadía >7 d: -${descuento_larga:,.2f} (10%)")
            if consumos_extras > 0:
                print(f"Consumos extras:        +${consumos_extras:,.2f} (Servicios/Minibar)")
            print("-" * 54)
            print(f"TOTAL FINAL A COBRAR:    ${total_a_liquidar:,.2f}")
            print("=" * 54)

            if not confirmar_accion("¿Confirma el Check-out y cobro final de este huésped? (s/n): "):
                print("\n[Operación cancelada] El huésped permanece registrado.")
                return

            # Confirmación aprobada: habitación pasa a sucia ('S') para limpieza
            matriz_hotel[piso][habitacion] = "S"
            lista_huespedes.remove(huesped)

            registrar_evento_auditoria("operador", "CHECK-OUT", f"{nombre} (DNI: {dni_checkout}) liberó hab {num_comercial}. Cobrado ${total_a_liquidar:,.2f}")

            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial} (requiere limpieza)")
            print(f"TOTAL COBRADO:       ${total_a_liquidar:,.2f}")
            print("===================================================")
            return

    print(f"\n[Aviso] No se encontró al huésped con DNI: {dni_checkout}")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Traslada a un huésped de una habitación a otra disponible:
    - Permite cancelar con '0' en cada paso.
    - Pide confirmación explícita con el resumen del traslado antes de aplicar el swap.
    """
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes alojados actualmente en el hotel.")
        return

    habitacion_swap_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación a reubicar: ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if habitacion_swap_str is None:
        return
    habitacion_swap = int(habitacion_swap_str)

    encontrado = False

    for huesped in lista_huespedes:
        piso, habitacion = int(huesped[3]), int(huesped[4])
        num_comercial = obtener_numero_comercial(piso, habitacion)

        if num_comercial == habitacion_swap:
            encontrado = True
            habitacion_valida = False
            nuevo_piso = 0
            nueva_habitacion = 0
            nuevo_numero = 0

            while not habitacion_valida:
                nuevo_numero_str = validar_generico_con_cancelacion(
                    "Ingrese el nuevo número de habitación: ",
                    PATRON_NUMERO_VALIDO,
                    ERROR_NUMERO
                )
                if nuevo_numero_str is None:
                    return
                nuevo_numero = int(nuevo_numero_str)

                nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)

                if nuevo_piso < 0 or nuevo_piso >= len(matriz_hotel) or nueva_habitacion < 0 or nueva_habitacion >= len(matriz_hotel[0]):
                    print(f"Error: La habitación {nuevo_numero} no existe en el hotel.")
                elif matriz_hotel[nuevo_piso][nueva_habitacion] == "M":
                    print(f"Error: La habitación {nuevo_numero} está en Mantenimiento [M].")
                elif matriz_hotel[nuevo_piso][nueva_habitacion] != "L":
                    print(f"Error: La habitación {nuevo_numero} no está libre (estado actual: [{matriz_hotel[nuevo_piso][nueva_habitacion]}]).")
                else:
                    habitacion_valida = True

            print("\n=== CONFIRMACIÓN DE REUBICACIÓN ===")
            print(f"Huésped a trasladar: {huesped[0]}")
            print(f"Habitación origen:   {num_comercial}")
            print(f"Habitación destino:  {nuevo_numero}")
            print("===================================")

            if not confirmar_accion("¿Confirma la reubicación de habitación? (s/n): "):
                print("\n[Operación cancelada] No se realizaron cambios.")
                return

            # Ejecución atómica del swap
            matriz_hotel[piso][habitacion] = "L"
            matriz_hotel[nuevo_piso][nueva_habitacion] = "O"
            huesped[3] = nuevo_piso
            huesped[4] = nueva_habitacion
            if len(huesped) > 5:
                huesped[5] = nuevo_numero

            registrar_evento_auditoria("operador", "SWAP", f"{huesped[0]} trasladado de hab {num_comercial} a {nuevo_numero}")

            print(f"\n[Swap exitoso] Huésped {huesped[0]} reubicado a la habitación {nuevo_numero}.")
            return

    if not encontrado:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")


def restablecer_limpieza(matriz_hotel):
    """
    Restaura una habitación con estado 'S' (Sucia/Limpieza) a estado 'L' (Libre)
    con opción de cancelar y confirmación previa.
    """
    num_hab_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación en limpieza: ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if num_hab_str is None:
        return
    num_hab = int(num_hab_str)

    piso, habitacion = obtener_indices_matriz(num_hab)
    if 0 <= piso < len(matriz_hotel) and 0 <= habitacion < len(matriz_hotel[0]):
        if matriz_hotel[piso][habitacion] == "S":
            if confirmar_accion(f"¿Confirma restablecer la habitación {num_hab} a Libre [L]? (s/n): "):
                matriz_hotel[piso][habitacion] = "L"
                registrar_evento_auditoria("operador", "LIMPIEZA", f"Habitación {num_hab} restablecida a Libre [L]")
                print(f"\n[Éxito] Habitación {num_hab} restablecida a disponible [L].")
            else:
                print("\n[Operación cancelada] La habitación continúa en limpieza.")
        else:
            print(f"Error: La habitación {num_hab} no está en limpieza (estado actual: [{matriz_hotel[piso][habitacion]}]).")
    else:
        print(f"Error: La habitación {num_hab} no existe en el hotel.")
