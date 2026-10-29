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
    for huesped in lista_huespedes:
        while huesped["dni"][0] == dni_nuevo:
            print(f"Error, el DNI {dni_nuevo} ya está registrado.")
            dni_nuevo = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
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
    dni_input = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    dni_input = validar_dni(dni_input, lista_huespedes)
    dias = int(validar_generico("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS))

    num_comercial = obtener_numero_comercial(piso, habitacion)

    # DNI guardado explícitamente como una Tupla inmutable
    dni_tupla = (dni_input,)

    # Estructura del huésped como Diccionario
    datos_huesped = {
        "nombre": nombre,
        "dni": dni_tupla,
        "dias": dias,
        "piso": piso,
        "habitacion": habitacion,
        "num_comercial": num_comercial
    }

    lista_huespedes.append(datos_huesped)
    matriz[piso][habitacion] = "O"

    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz


def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de diccionarios consultando la tupla de DNI.
    """
    encontrado = False

    for huesped in lista_huespedes:
        dni_actual = huesped["dni"][0]

        if str(dni_actual).strip() == str(dni_busqueda).strip():
            encontrado = True
            piso_real = int(huesped["piso"]) + 1

            # Acceso directo al primer elemento de la tupla del DNI
            dni = huesped["dni"][0]

            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print(f"{'Nombre:':<17} {huesped['nombre']}")
            print(f"{'DNI:':<17} {dni}")
            print(f"{'Días de estadía:':<17} {huesped['dias']}")
            print(f"{'Piso asignado:':<17} {piso_real}")
            print(f"{'Habitación:':<17} {huesped['num_comercial']}")
            print("====================================")

    if not encontrado:
        print("\n[Aviso] No se encontró ningún huésped alojado con el DNI:", dni_busqueda)


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Uso de 'filter' y 'lambda' sobre la lista de diccionarios.
    """
    filtrados = list(filter(
        lambda huesped: int(huesped["piso"]) == int(piso_objetivo) - 1,
        lista_huespedes
    ))
    return filtrados


def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    """
    Libera la habitación, pasa a estado 'S' y genera la liquidación.
    """
    print("\n--- CHECK-OUT ---")
    dni_checkout = validar_generico("Ingrese el DNI del huésped para check-out: ", PATRON_DNI_VALIDO, ERROR_DNI)

    for huesped in lista_huespedes:
        dni_actual = huesped["dni"][0]

        if str(dni_actual) == str(dni_checkout):
            nombre = huesped["nombre"]
            dias = huesped["dias"]
            piso = huesped["piso"]
            habitacion = huesped["habitacion"]
            num_comercial = huesped["num_comercial"]

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
        if huesped["num_comercial"] == habitacion_swap:
            piso = huesped["piso"]
            habitacion = huesped["habitacion"]

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

            huesped["piso"] = nuevo_piso
            huesped["habitacion"] = nueva_habitacion
            huesped["num_comercial"] = nuevo_num_comercial

            print(f"Huésped {huesped['nombre']} reubicado a habitación {nuevo_num_comercial} con éxito.")
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