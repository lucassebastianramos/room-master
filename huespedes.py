# =============================================================================
# MÓDULO DE GESTIÓN DE HUÉSPEDES (huespedes.py)
# =============================================================================
# Responsabilidad: Ciclo de vida y transacciones de los huéspedes del hotel:
# Check-in, Check-out con facturación, reubicación de habitación (Swap),
# búsquedas secuenciales por DNI, filtros por piso y restablecimiento de limpieza.
# =============================================================================

from validaciones import (
    validar_generico,
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
    solicitar_habitacion_libre
)
from tarifas import obtener_tarifa_habitacion


def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro de un nuevo huésped en el hotel.
    Valida la disponibilidad, los datos personales mediante expresiones regulares
    y asigna la habitación actualizando la matriz a estado 'O' (Ocupada).
    Estructura de registro: [nombre, dni, dias, piso, habitacion, num_comercial].
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)
    if piso is None:
        return matriz

    nombre = validar_generico("Ingrese el nombre del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    dni = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    dias = int(validar_generico("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS))

    num_comercial = obtener_numero_comercial(piso, habitacion)

    # Registro de la entidad huésped como lista normalizada
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial]
    lista_huespedes.append(datos_huesped)

    # Marcamos la habitación como ocupada
    matriz[piso][habitacion] = "O"

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")
    return matriz


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de huéspedes.
    Estructura de cada registro: [nombre, dni, dias, piso, habitacion, num_comercial].
    """
    encontrado = False

    for i in range(len(lista_huespedes)):
        huesped = lista_huespedes[i]
        nombre = huesped[0]
        dni_actual = huesped[1]
        dias = huesped[2]
        piso = int(huesped[3])
        hab = int(huesped[4])

        num_comercial = huesped[5] if len(huesped) > 5 else obtener_numero_comercial(piso, hab)
        piso_real = piso + 1

        if str(dni_actual).strip() == str(dni_busqueda).strip():
            encontrado = True
            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print("Nombre:         ", nombre)
            print("DNI:            ", dni_actual)
            print("Días de estadía:", dias)
            print("Piso asignado:  ", piso_real)
            print("Habitación:     ", num_comercial)
            print("====================================")

    if not encontrado:
        print(f"\n[Aviso] No se encontró ningún huésped alojado con el DNI: {dni_busqueda}")


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Filtra los huéspedes de un piso específico utilizando 'filter' y 'lambda'.
    'piso_objetivo' representa el número comercial de piso (1 para primer piso, etc.).
    Cumple con el requisito de funciones de orden superior y programación funcional.
    """
    indice_piso = int(piso_objetivo) - 1
    filtrados = list(filter(
        lambda huesped: int(huesped[3]) == indice_piso,
        lista_huespedes
    ))
    return filtrados


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    """
    Procesa la salida de un huésped:
    Calcula el monto total adeudado según días y tarifa del piso,
    elimina el huésped de los registros y cambia la habitación a estado 'S' (Limpieza/Sucia).
    """
    print("\n--- CHECK-OUT ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes registrados actualmente en el hotel.")
        return

    dni_checkout = validar_generico("Ingrese el DNI del huésped para check-out: ", PATRON_DNI_VALIDO, ERROR_DNI)
    buscar_huesped_por_dni(lista_huespedes, dni_checkout)

    for huesped in lista_huespedes:
        if str(huesped[1]) == str(dni_checkout):
            nombre = huesped[0]
            dias = huesped[2]
            piso = huesped[3]
            habitacion = huesped[4]

            # La habitación pasa a requerir limpieza ('S')
            matriz_hotel[piso][habitacion] = "S"
            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            dias_num = int(dias)
            monto_total = tarifa * dias_num
            num_comercial = obtener_numero_comercial(piso, habitacion)

            # Remover al huésped de la lista activa
            lista_huespedes.remove(huesped)

            # Generar comprobante en consola
            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial} (requiere limpieza)")
            print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
            print("===================================================")
            return

    print(f"\n[Aviso] No se encontró al huésped con DNI: {dni_checkout}")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Traslada a un huésped de una habitación a otra disponible.
    La habitación anterior queda libre ('L') y la nueva pasa a ocupada ('O').
    Permite cancelar ingresando 0.
    """
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")
    if len(lista_huespedes) == 0:
        print("[Aviso] No hay huéspedes alojados actualmente en el hotel.")
        return

    habitacion_swap = int(validar_generico(
        "Ingrese el número de habitación a reubicar (o 0 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    ))

    if habitacion_swap == 0:
        print("[Operación cancelada] Regresando al menú...")
        return

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
                nuevo_numero = int(validar_generico(
                    "Ingrese el nuevo número de habitación (o 0 para cancelar): ",
                    PATRON_NUMERO_VALIDO,
                    ERROR_NUMERO
                ))

                if nuevo_numero == 0:
                    print("[Operación cancelada] No se realizaron cambios.")
                    return

                nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)

                # Validaciones de límites de la matriz y estado libre
                if nuevo_piso < 0 or nuevo_piso >= len(matriz_hotel) or nueva_habitacion < 0 or nueva_habitacion >= len(matriz_hotel[0]):
                    print(f"Error: La habitación {nuevo_numero} no existe en el hotel.")
                elif matriz_hotel[nuevo_piso][nueva_habitacion] != "L":
                    print(f"Error: La habitación {nuevo_numero} no está libre (estado actual: [{matriz_hotel[nuevo_piso][nueva_habitacion]}]).")
                else:
                    habitacion_valida = True

            # Actualización atómica del swap en la matriz y el registro
            matriz_hotel[piso][habitacion] = "L"  # Habitación anterior queda libre
            matriz_hotel[nuevo_piso][nueva_habitacion] = "O"  # Nueva habitación ocupada
            huesped[3] = nuevo_piso
            huesped[4] = nueva_habitacion
            if len(huesped) > 5:
                huesped[5] = nuevo_numero

            print(f"\n[Swap exitoso] Huésped {huesped[0]} reubicado a la habitación {nuevo_numero}.")
            return

    if not encontrado:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")


def restablecer_limpieza(matriz_hotel):
    """
    Restaura una habitación con estado 'S' (Sucia/Limpieza) a estado 'L' (Libre).
    Permite cancelar ingresando 0.
    """
    num_hab = int(validar_generico(
        "Ingrese el número de habitación en limpieza (o 0 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    ))

    if num_hab == 0:
        print("[Operación cancelada] Regresando al menú...")
        return

    piso, habitacion = obtener_indices_matriz(num_hab)
    if 0 <= piso < len(matriz_hotel) and 0 <= habitacion < len(matriz_hotel[0]):
        if matriz_hotel[piso][habitacion] == "S":
            matriz_hotel[piso][habitacion] = "L"
            print(f"\n[Éxito] Habitación {num_hab} restablecida a disponible [L].")
        else:
            print(f"Error: La habitación {num_hab} no está en limpieza (estado actual: [{matriz_hotel[piso][habitacion]}]).")
    else:
        print(f"Error: La habitación {num_hab} no existe en el hotel.")
