# =============================================================================
# MÓDULO DE GESTIÓN DE HUÉSPEDES (huespedes.py)
# =============================================================================
# Responsabilidad: Ciclo de vida y operaciones completas de gestión:
# Alta (Check-in), Baja (Check-out con liquidación), Modificación (Swap,
# consumos adicionales, extensión de estadía) y Consulta (búsquedas y filtros).
# Uso de Tuplas para datos inmutables (DNI, configuración fija de habitación)
# y Conjuntos (set) para búsquedas O(1) y validación de unicidad.
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
    hay_habitaciones_disponibles,
    obtener_habitaciones_por_estado
)
from tarifas import obtener_tarifa_habitacion


def obtener_conjunto_dnis(lista_huespedes):
    """
    Retorna un conjunto (set) con todos los DNIs de los huéspedes actualmente alojados.
    Permite búsquedas y validaciones en tiempo constante O(1).
    """
    return {huesped[0][0] for huesped in lista_huespedes}


def obtener_conjunto_habitaciones_ocupadas(lista_huespedes):
    """
    Retorna un conjunto (set) con los números comerciales de las habitaciones ocupadas.
    Garantiza elementos únicos y validaciones directas.
    """
    return {huesped[1][2] for huesped in lista_huespedes}


def realizar_checkin(matriz, lista_huespedes, matriz_tarifas=None):
    """
    Alta de reserva (Check-in):
    - Valida que haya habitaciones disponibles.
    - Asigna una habitación libre.
    - Valida unicidad de DNI mediante conjunto (set).
    - Almacena datos inmutables en Tuplas:
      * identidad = (dni, nombre)
      * config_habitacion = (piso, habitacion, num_comercial)
    - Solicita confirmación explícita antes de asentar en la matriz.
    """
    if not hay_habitaciones_disponibles(matriz):
        print("\n[Aviso] El hotel se encuentra 100% completo. No hay habitaciones libres disponibles.")
        return matriz

    piso, habitacion = solicitar_habitacion_libre(matriz)
    if piso is None:
        return matriz

    num_comercial = obtener_numero_comercial(piso, habitacion)

    print("\n--- REGISTRO DE NUEVO HUÉSPED ---")
    dni = validar_generico_con_cancelacion("DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    if dni is None:
        return matriz

    # Validación de unicidad de DNI mediante Conjunto (set)
    dnis_activos = obtener_conjunto_dnis(lista_huespedes)
    if dni in dnis_activos:
        print(f"\n[Error] El huésped con DNI {dni} ya posee una reserva activa en el hotel.")
        return matriz

    nombre = validar_generico_con_cancelacion("Nombre y Apellido del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    if nombre is None:
        return matriz

    dias_str = validar_generico_con_cancelacion("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS)
    if dias_str is None:
        return matriz
    dias = int(dias_str)

    # Cálculo tarifario
    tarifa_noche = float(obtener_tarifa_habitacion(piso + 1, matriz_tarifas)) if matriz_tarifas else 0.0
    total_estimado = tarifa_noche * dias

    # Resumen y confirmación previa
    print("\n" + "=" * 52)
    print("             CONFIRMACIÓN DE CHECK-IN             ")
    print("=" * 52)
    print(f"Huésped titular:      {nombre}")
    print(f"DNI:                  {dni}")
    print(f"Habitación asignada:  {num_comercial} (Piso {piso + 1})")
    print(f"Días de estadía:      {dias} noches")
    if matriz_tarifas:
        print(f"Tarifa por noche:     ${tarifa_noche:,.2f}")
        print(f"Total estimado:       ${total_estimado:,.2f}")
    print("=" * 52)

    if not confirmar_accion("¿Confirma la reserva con estos datos? (s/n): "):
        print("\n[Operación cancelada] No se realizó el Check-in.")
        return matriz

    # Almacenamiento con Tuplas inmutables
    identidad_inmutable = (str(dni), str(nombre))
    config_habitacion = (int(piso), int(habitacion), int(num_comercial))
    consumos_extras = 0.0

    registro_huesped = [identidad_inmutable, config_habitacion, dias, consumos_extras]
    lista_huespedes.append(registro_huesped)
    matriz[piso][habitacion] = "O"

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")
    return matriz


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    """
    Baja de reserva (Check-out):
    - Valida existencia del DNI utilizando conjunto (set).
    - Desglosa liquidación: noches x tarifa, bonificación del 10% si noches > 7,
      y consumos adicionales (minibar/servicios).
    - Solicita confirmación explícita previa.
    - Libera la habitación a estado Sucio/Limpieza ('S') y retira al huésped.
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

    # Comprobación rápida O(1) con Conjunto (set)
    dnis_activos = obtener_conjunto_dnis(lista_huespedes)
    if dni_checkout not in dnis_activos:
        print(f"\n[Aviso] No se encontró ningún huésped alojado con el DNI: {dni_checkout}")
        return

    for huesped in lista_huespedes:
        dni_actual = huesped[0][0]
        if dni_actual == dni_checkout:
            nombre = huesped[0][1]
            piso, habitacion, num_comercial = huesped[1]
            dias = int(huesped[2])
            consumos_extras = float(huesped[3])

            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            subtotal_habitacion = tarifa * dias

            # Bonificación 10% por estadía prolongada (> 7 noches)
            descuento_larga = (subtotal_habitacion * 0.10) if dias > 7 else 0.0
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

            # Habitación pasa a sucia ('S') para posterior limpieza
            matriz_hotel[piso][habitacion] = "S"
            lista_huespedes.remove(huesped)

            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial} (requiere limpieza [S])")
            print(f"TOTAL COBRADO:       ${total_a_liquidar:,.2f}")
            print("===================================================")
            return


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Modificación de reserva: Reubicación de habitación (Swap).
    Traslada a un huésped a otra habitación libre y actualiza su tupla de habitación fija.
    """
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes alojados actualmente en el hotel.")
        return

    habitacion_swap_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación actual a reubicar: ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if habitacion_swap_str is None:
        return
    habitacion_swap = int(habitacion_swap_str)

    # Validación de que la habitación esté ocupada usando Conjuntos
    ocupadas_set = obtener_conjunto_habitaciones_ocupadas(lista_huespedes)
    if habitacion_swap not in ocupadas_set:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")
        return

    for huesped in lista_huespedes:
        piso_ant, hab_ant, num_ant = huesped[1]

        if num_ant == habitacion_swap:
            nombre = huesped[0][1]
            libres_set = obtener_habitaciones_por_estado(matriz_hotel, "L")

            if len(libres_set) == 0:
                print("\n[Aviso] No hay otras habitaciones libres disponibles para reubicar al huésped.")
                return

            habitacion_valida = False
            nuevo_piso = 0
            nueva_hab = 0
            nuevo_numero = 0

            while not habitacion_valida:
                nuevo_num_str = validar_generico_con_cancelacion(
                    "Ingrese el nuevo número de habitación libre: ",
                    PATRON_NUMERO_VALIDO,
                    ERROR_NUMERO
                )
                if nuevo_num_str is None:
                    return
                nuevo_numero = int(nuevo_num_str)

                if nuevo_numero not in libres_set:
                    print(f"Error: La habitación {nuevo_numero} no está libre para swap.")
                else:
                    nuevo_piso, nueva_hab = obtener_indices_matriz(nuevo_numero)
                    habitacion_valida = True

            print("\n=== CONFIRMACIÓN DE REUBICACIÓN ===")
            print(f"Huésped a trasladar: {nombre}")
            print(f"Habitación origen:   {num_ant}")
            print(f"Habitación destino:  {nuevo_numero}")
            print("===================================")

            if not confirmar_accion("¿Confirma la reubicación de habitación? (s/n): "):
                print("\n[Operación cancelada] No se realizaron cambios.")
                return

            # Ejecución atómica del traslado
            matriz_hotel[piso_ant][hab_ant] = "L"
            matriz_hotel[nuevo_piso][nueva_hab] = "O"

            # Reasignación de tupla inmutable de habitación fija
            huesped[1] = (nuevo_piso, nueva_hab, nuevo_numero)

            print(f"\n[Swap exitoso] Huésped {nombre} reubicado a la habitación {nuevo_numero}.")
            return


def cargar_consumo_habitacion(matriz_hotel, lista_huespedes):
    """
    Modificación de reserva: Cargar consumos adicionales (Minibar, Cochera, Servicios).
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

    ocupadas = obtener_conjunto_habitaciones_ocupadas(lista_huespedes)
    if num_hab not in ocupadas:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {num_hab}.")
        return

    for huesped in lista_huespedes:
        if huesped[1][2] == num_hab:
            nombre = huesped[0][1]
            dni = huesped[0][0]
            print(f"\nHuésped alojado: {nombre} (DNI: {dni})")

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
            print(f"Habitación:  {num_hab}")
            print(f"Huésped:     {nombre}")
            print(f"Concepto:    {concepto}")
            print(f"Importe:     ${monto:,.2f}")
            print("=================================")

            if confirmar_accion("¿Confirma cargar este consumo a la habitación? (s/n): "):
                huesped[3] += monto
                print(f"\n[Éxito] Se cargaron ${monto:,.2f} a la habitación {num_hab}.")
                print(f"Total acumulado en extras: ${huesped[3]:,.2f}")
            else:
                print("\n[Operación cancelada] No se imputó el consumo.")
            return


def extender_estadia_huesped(matriz_hotel, lista_huespedes):
    """
    Modificación de reserva: Prolongar noches de estadía de un huésped.
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

    ocupadas = obtener_conjunto_habitaciones_ocupadas(lista_huespedes)
    if num_hab not in ocupadas:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {num_hab}.")
        return

    for huesped in lista_huespedes:
        if huesped[1][2] == num_hab:
            nombre = huesped[0][1]
            dias_actuales = int(huesped[2])
            print(f"\nHuésped: {nombre} | Estadía actual: {dias_actuales} noches.")

            adicional_str = validar_generico_con_cancelacion(
                "Cantidad de noches adicionales a extender: ",
                PATRON_DIAS_VALIDO,
                ERROR_DIAS
            )
            if adicional_str is None:
                return
            noches_extra = int(adicional_str)
            total_noches = dias_actuales + noches_extra

            print("\n=== CONFIRMACIÓN DE EXTENSIÓN ===")
            print(f"Huésped:             {nombre}")
            print(f"Habitación:          {num_hab}")
            print(f"Noches actuales:     {dias_actuales}")
            print(f"Noches a agregar:    +{noches_extra}")
            print(f"Nueva estadía total: {total_noches} noches")
            print("=================================")

            if confirmar_accion("¿Confirma la extensión de la estadía? (s/n): "):
                huesped[2] = total_noches
                print(f"\n[Éxito] Estadía de {nombre} extendida a {total_noches} noches.")
            else:
                print("\n[Operación cancelada] No se modificó la estadía.")
            return


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Consulta de reserva: Búsqueda rápida por DNI mediante Conjunto (set).
    """
    if dni_busqueda is None:
        return

    dnis_activos = obtener_conjunto_dnis(lista_huespedes)
    if dni_busqueda not in dnis_activos:
        print(f"\n[Aviso] No se encontró ningún huésped alojado con el DNI: {dni_busqueda}")
        return

    for huesped in lista_huespedes:
        dni_actual = huesped[0][0]
        if dni_actual == str(dni_busqueda).strip():
            nombre = huesped[0][1]
            piso, hab, num_comercial = huesped[1]
            dias = huesped[2]
            extras = huesped[3]

            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print(f"Nombre:               {nombre}")
            print(f"DNI:                  {dni_actual}")
            print(f"Días de estadía:      {dias} noches")
            print(f"Piso asignado:        {piso + 1}")
            print(f"Habitación:           {num_comercial}")
            if extras > 0:
                print(f"Consumos adicionales: ${extras:,.2f}")
            print("====================================")
            return


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Consulta de reserva: Filtrado de huéspedes por piso utilizando 'filter' y 'lambda'.
    'piso_objetivo' es el número comercial de piso (1 para primer piso).
    """
    indice_piso = int(piso_objetivo) - 1
    filtrados = list(filter(
        lambda huesped: huesped[1][0] == indice_piso,
        lista_huespedes
    ))
    return filtrados


def restablecer_limpieza(matriz_hotel):
    """
    Restaura una habitación con estado 'S' (Sucia/Limpieza) a estado 'L' (Libre)
    con opción de cancelar y confirmación previa.
    """
    sucias_set = obtener_habitaciones_por_estado(matriz_hotel, "S")
    if len(sucias_set) == 0:
        print("\n[Aviso] No hay habitaciones pendientes de limpieza en el hotel.")
        return

    num_hab_str = validar_generico_con_cancelacion(
        "Ingrese el número de habitación en limpieza a habilitar: ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )
    if num_hab_str is None:
        return
    num_hab = int(num_hab_str)

    if num_hab not in sucias_set:
        print(f"Error: La habitación {num_hab} no se encuentra en estado de limpieza [S].")
        return

    piso, habitacion = obtener_indices_matriz(num_hab)
    if confirmar_accion(f"¿Confirma restablecer la habitación {num_hab} a Libre [L]? (s/n): "):
        matriz_hotel[piso][habitacion] = "L"
        print(f"\n[Éxito] Habitación {num_hab} restablecida a disponible [L].")
    else:
        print("\n[Operación cancelada] La habitación continúa en limpieza.")
