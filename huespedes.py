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
    Verifica que el DNI no esté repetido en la lista de diccionarios.
    El DNI en el diccionario se accede como el primer elemento de la tupla: huesped["dni"][0]
    """
    # Uso de conjunto (set) para verificar duplicados y busqueda O(1)
    dnis_registrados = set()
    for huesped in lista_huespedes:
        dnis_registrados.add(huesped["identidad"][0])

    while dni_nuevo in dnis_registrados:
        print(f"Error, el DNI {dni_nuevo} ya está registrado.")
        dni_nuevo = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
        dnis_registrados = set()
        for huesped in lista_huespedes:
            dnis_registrados.add(huesped["identidad"][0])
    return dni_nuevo


def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro completo de un huésped guardando sus datos en un diccionario
    y almacenando el DNI como una TUPLA INMUTABLE según lineamientos de la cátedra.
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)
    if piso is None:
        return matriz

    nombre = validar_generico("Ingrese el nombre del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    dni = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    dni = validar_dni(dni, lista_huespedes)
    dias = int(validar_generico("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS))

    num_comercial = obtener_numero_comercial(piso, habitacion)

    # identidad: tupla inmutable (DNI, Nombre) -> no cambia nunca
    # ubicacion: lista mutable [piso, habitacion, num_comercial] -> se puede modificar (swap)
    datos_huesped = {
        "identidad": (dni, nombre),
        "dias": dias,
        "ubicacion": [piso, habitacion, num_comercial]
    }

    lista_huespedes.append(datos_huesped)
    matriz[piso][habitacion] = "O"

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de diccionarios consultando la tupla de DNI.
    """
    if len(lista_huespedes) == 0:
        print("\n[Aviso] No hay huéspedes alojados en el hotel.")
        return

    encontrado = False

    for huesped in lista_huespedes:
        dni_actual = huesped["identidad"][0]

        if str(dni_actual).strip() == str(dni_busqueda).strip():
            encontrado = True
            piso_real = int(huesped["ubicacion"][0]) + 1

            # Acceso a la tupla identidad: [0]=DNI, [1]=Nombre
            dni = huesped["identidad"][0]
            nombre = huesped["identidad"][1]

            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print(f"{'Nombre:':<17} {nombre}")
            print(f"{'DNI:':<17} {dni}")
            print(f"{'Días de estadía:':<17} {huesped['dias']}")
            print(f"{'Piso asignado:':<17} {piso_real}")
            print(f"{'Habitación:':<17} {huesped['ubicacion'][2]}")
            print("====================================")

    if not encontrado:
        print("\n[Aviso] No se encontró ningún huésped alojado con el DNI:", dni_busqueda)


def buscar_huespedes_por_nombre(lista_huespedes, texto_busqueda):
    """
    Busca huéspedes cuyo nombre contenga el texto ingresado (sin importar mayúsculas).
    Usa filter y lambda.
    """
    return list(filter(
        lambda huesped: texto_busqueda.lower() in huesped["identidad"][1].lower(),
        lista_huespedes
    ))


def buscar_huesped_por_habitacion(lista_huespedes, numero_habitacion):
    """
    Busca huéspedes alojados en la habitación indicada.
    Usa filter y lambda.
    """
    return list(filter(
        lambda huesped: huesped["ubicacion"][2] == numero_habitacion,
        lista_huespedes
    ))


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    """
    Libera la habitación, pasa a estado 'S' y genera la liquidación.
    """
    print("\n--- CHECK-OUT ---")
    dni_checkout = validar_generico("Ingrese el DNI del huésped para check-out: ", PATRON_DNI_VALIDO, ERROR_DNI)

    for huesped in lista_huespedes:
        dni_actual = huesped["identidad"][0]

        if str(dni_actual) == str(dni_checkout):
            nombre = huesped["identidad"][1]
            dias = huesped["dias"]
            piso = huesped["ubicacion"][0]
            habitacion = huesped["ubicacion"][1]
            num_comercial = huesped["ubicacion"][2]

            matriz_hotel[piso][habitacion] = "S"
            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            monto_total = tarifa * int(dias)

            lista_huespedes.remove(huesped)

            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial}")
            print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
            print("===================================================")
            return

    print(f"No se encontró al huésped con DNI: {dni_checkout}")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Traslada un huésped a una habitación libre actualizando su diccionario.
    """
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")
    if len(lista_huespedes) == 0:
        print("No hay huéspedes alojados actualmente en el hotel.")
        return

    habitacion_swap = int(validar_generico("Ingrese el número de habitación a reubicar: ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))

    for huesped in lista_huespedes:
        if huesped["ubicacion"][2] == habitacion_swap:
            piso = huesped["ubicacion"][0]
            habitacion = huesped["ubicacion"][1]

            # Verificar si hay alguna habitación libre antes de pedir
            hay_libre = False
            for fila in matriz_hotel:
                for habitacion_libre in fila:
                    if habitacion_libre == "L":
                        hay_libre = True

            if not hay_libre:
                print("Error: No hay habitaciones libres en el hotel. No se puede reubicar.")
                return

            habitacion_valida = False
            nuevo_piso = 0
            nueva_habitacion = 0
            nuevo_num_comercial = 0

            while not habitacion_valida:
                nuevo_num_comercial = int(validar_generico("Ingrese el nuevo número de habitación: ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
                nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_num_comercial)

                if nuevo_piso < 0 or nuevo_piso >= len(matriz_hotel) or nueva_habitacion < 0 or nueva_habitacion >= len(matriz_hotel[0]):
                    print(f"Error: La habitación {nuevo_num_comercial} no existe en el hotel.")
                elif matriz_hotel[nuevo_piso][nueva_habitacion] != "L":
                    print(f"Error: La habitación {nuevo_num_comercial} no está libre (estado actual: [{matriz_hotel[nuevo_piso][nueva_habitacion]}]).")
                else:
                    habitacion_valida = True

            # Actualizar matriz y diccionario
            matriz_hotel[piso][habitacion] = "L"
            matriz_hotel[nuevo_piso][nueva_habitacion] = "O"

            # Mutacion de la lista ubicacion (demostrando que es mutable)
            huesped["ubicacion"][0] = nuevo_piso
            huesped["ubicacion"][1] = nueva_habitacion
            huesped["ubicacion"][2] = nuevo_num_comercial

            print(f"Huésped {huesped['identidad'][1]} reubicado a habitación {nuevo_num_comercial} con éxito.")
            return

    print(f"No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")


def restablecer_limpieza(matriz_hotel):
    """
    Restaura una habitación con estado Sucio [S] a estado Libre [L].
    """
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