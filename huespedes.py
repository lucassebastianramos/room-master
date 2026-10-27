# =============================================================================
# MÓDULO 3: GESTIÓN DE HUÉSPEDES, CHECK-OUT Y SWAP (huespedes.py)
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

def validar_dni(dni_nuevo, lista_huespedes):
    """
    Se fija que el DNI no se repita.
    """
    for i in range (len(lista_huespedes)):
        while lista_huespedes[i][1] == dni_nuevo:
            print(f"Error, el DNI {dni_nuevo} ya está registrado")
            dni_nuevo = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    return dni_nuevo

def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro completo de un nuevo huésped en el sistema.
    Valida datos de los huéspedes con Regex.
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)
    if piso is None:
        return matriz

    nombre = validar_generico("Ingrese el nombre del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    dni = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    dni = validar_dni(dni, lista_huespedes)
    dias = int(validar_generico("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS))

    num_comercial = obtener_numero_comercial(piso, habitacion)

    # Registro del huésped como lista: [nombre, dni, dias, piso, habitacion, num_comercial]
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial]
    lista_huespedes.append(datos_huesped)

    matriz[piso][habitacion] = "O"

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de huéspedes (sublistas).
    Estructura de cada registro: [nombre, dni, dias, piso, habitacion, num_comercial]
    """
    encontrado = False

    for i in range(len(lista_huespedes)):
        huesped = lista_huespedes[i]
        nombre = huesped[0]
        dni_actual = huesped[1]
        dias = huesped[2]
        piso = int(huesped[3])
        hab = int(huesped[4])

        # Obtenemos el número comercial único de la habitación (ej: 101) y piso real (ej: 1)
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
        print("\n[Aviso] No se encontró ningún huésped alojado con el DNI:", dni_busqueda)


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Uso de 'filter' y 'lambda' para aislar los huéspedes de un piso específico.
    Cumple con el requisito de funciones de orden superior y listas avanzadas.
    piso_objetivo: número de piso comercial (1, 2, ...).
    """
    filtrados = list(filter(
        lambda huesped: int(huesped[3]) == int(piso_objetivo) - 1,
        lista_huespedes
    ))
    return filtrados


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    # Liberar habitación, pasar a 'S' (Limpieza) y calcular cobro
    print("\n--- CHECK-OUT ---")
    dni_checkout = validar_generico("Ingrese el DNI del huésped para check-out: ", PATRON_DNI_VALIDO, ERROR_DNI)
    buscar_huesped_por_dni(lista_huespedes, dni_checkout)
    for huesped in lista_huespedes:
        if str(huesped[1]) == str(dni_checkout):
            nombre = huesped[0]
            dias = huesped[2]
            piso = huesped[3]
            habitacion = huesped[4]

            matriz_hotel[piso][habitacion] = "S"
            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            dias_num = int(dias)
            monto_total = tarifa * dias_num
            num_comercial = obtener_numero_comercial(piso, habitacion)

            # Borrar huésped de la lista
            lista_huespedes.remove(huesped)

            # Recibo
            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial}")
            print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
            print("===================================================")
            return

    print(f"No se encontró al huésped con DNI: {dni_checkout}")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    # Trasladar huésped, habitación vieja queda libre ('L')
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")
    if len(lista_huespedes) == 0:
        print("No hay huéspedes alojados actualmente en el hotel.")
        return
    habitacion_swap = int(validar_generico("Ingrese el número de habitación a reubicar: ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
    encontrado = False

    for huesped in lista_huespedes:
        piso, habitacion = map(int, [huesped[3], huesped[4]])
        num_comercial = obtener_numero_comercial(piso, habitacion)

        if num_comercial == habitacion_swap:
            encontrado = True
            # Validar y solicitar la nueva habitación hasta que sea válida y libre
            habitacion_valida = False
            nuevo_piso = 0
            nueva_habitacion = 0
            nuevo_numero = 0

            while not habitacion_valida:
                nuevo_numero = int(validar_generico("Ingrese el nuevo número de habitación: ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
                nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)

                # Validar que los índices existan dentro de la matriz
                if nuevo_piso < 0 or nuevo_piso >= len(matriz_hotel) or nueva_habitacion < 0 or nueva_habitacion >= len(matriz_hotel[0]):
                    print(f"Error: La habitación {nuevo_numero} no existe en el hotel.")
                elif matriz_hotel[nuevo_piso][nueva_habitacion] != "L":
                    print(f"Error: La habitación {nuevo_numero} no está libre (estado actual: [{matriz_hotel[nuevo_piso][nueva_habitacion]}]).")
                else:
                    habitacion_valida = True

            # Actualizar la matriz y los datos del huésped
            matriz_hotel[piso][habitacion] = "L"  # Habitación vieja queda libre
            matriz_hotel[nuevo_piso][nueva_habitacion] = "O"  # Nueva habitación ocupada
            huesped[3] = nuevo_piso
            huesped[4] = nueva_habitacion
            if len(huesped) > 5:
                huesped[5] = nuevo_numero

            print(f"Huésped {huesped[0]} reubicado a habitación {nuevo_numero} con éxito.")
            return

    if not encontrado:
        print(f"No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")


def restablecer_limpieza(matriz_hotel):
    num_hab = int(validar_generico("Ingrese el número de habitación en limpieza: ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
    piso, habitacion = obtener_indices_matriz(num_hab)
    if 0 <= piso < len(matriz_hotel) and 0 <= habitacion < len(matriz_hotel[0]):
        if matriz_hotel[piso][habitacion] == "S":
            matriz_hotel[piso][habitacion] = "L"
            print("Habitación restablecida con éxito!")
        else:
            print("Error: La habitación no está en limpieza.")
    else:
        print("Error: La habitación ingresada no existe en el hotel.")

