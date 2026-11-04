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
    solicitar_habitacion_libre,
    hay_habitaciones_libres,
    habitacion_existe
)
from tarifas import obtener_tarifa_habitacion
from reportes import calcular_subtotal
from archivos import registrar_factura_txt

def hotel_vacio(lista_huespedes):
    """
    Devuelve True si no hay huéspedes alojados.
    """
    if len(lista_huespedes) == 0:
        return True
    return False


def obtener_huesped_por_habitacion(lista_huespedes, numero_habitacion):
    """
    Devuelve el huésped alojado en esa habitación, o -1 si no hay ninguno.
    """
    for huesped in lista_huespedes:
        if huesped["ubicacion"][2] == numero_habitacion:
            return huesped
    return -1


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
        dni_nuevo = validar_generico("Ingrese el DNI del huésped (-1 para cancelar): ", PATRON_DNI_VALIDO, ERROR_DNI)
        if dni_nuevo == "-1":
            return "-1"

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
    if piso == -1:
        return matriz

    nombre = validar_generico("Ingrese el nombre del huésped (-1 para cancelar): ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    if nombre == "-1":
        return matriz

    dni = validar_generico("Ingrese el DNI del huésped (-1 para cancelar): ", PATRON_DNI_VALIDO, ERROR_DNI)
    if dni == "-1":
        return matriz

    dni = validar_dni(dni, lista_huespedes)
    if dni == "-1":
        return matriz

    dias = validar_generico("Cantidad de días de estadía (-1 para cancelar): ", PATRON_DIAS_VALIDO, ERROR_DIAS)
    if dias == "-1":
        return matriz

    dias = int(dias)
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
    if hotel_vacio(lista_huespedes):
        print("No hay huéspedes alojados actualmente en el hotel.")
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
    Retorna True si el check-out se completó con éxito, False en caso contrario.
    """
    print("\n--- CHECK-OUT ---")

    if hotel_vacio(lista_huespedes):
        print("No hay huéspedes alojados actualmente en el hotel.")
        return False  # <-- Retorna False

    dni_checkout = validar_generico(
        "Ingrese el DNI del huésped para check-out (-1 para cancelar): ",
        PATRON_DNI_VALIDO,
        ERROR_DNI
    )

    if dni_checkout == "-1":
        print("Check-out cancelado.")
        return False  # <-- Retorna False

    for huesped in lista_huespedes:
        dni_actual = huesped["identidad"][0]

        if str(dni_actual) == str(dni_checkout):
            nombre = huesped["identidad"][1]
            dias = huesped["dias"]
            piso = huesped["ubicacion"][0]
            habitacion = huesped["ubicacion"][1]
            num_comercial = huesped["ubicacion"][2]

            monto_total = calcular_subtotal(huesped, matriz_tarifas)

            matriz_hotel[piso][habitacion] = "S"
            lista_huespedes.remove(huesped)

            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial}")
            print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
            print("===================================================")

            # Registro en el archivo TXT
            registrar_factura_txt(dni_checkout, nombre, num_comercial, piso + 1, dias, monto_total)
            print("[Info] Factura registrada en el historial de facturación (.txt)")
            return True  # <-- Retorna True solo cuando se cobra con éxito

    print(f"No se encontró al huésped con DNI: {dni_checkout}")
    return False  # <-- Retorna False si no lo encuentra

def puede_reubicar(matriz_hotel, lista_huespedes):
    """
    Devuelve True si hay huéspedes y habitaciones libres para reubicar.
    """
    if hotel_vacio(lista_huespedes):
        print("No hay huéspedes alojados actualmente en el hotel.")
        return False

    if hay_habitaciones_libres(matriz_hotel) == False:
        print("El hotel está completo. No hay habitaciones libres para reubicar.")
        return False

    return True


def pedir_huesped_a_reubicar(lista_huespedes):
    """
    Pide una habitación y devuelve el huésped que la ocupa.
    Devuelve -1 si se cancela o si no hay huésped en esa habitación.
    """
    entrada = validar_generico(
        "Ingrese el número de habitación a reubicar (-1 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )

    if entrada == "-1":
        print("Reubicación cancelada.")
        return -1

    numero = int(entrada)
    huesped = obtener_huesped_por_habitacion(lista_huespedes, numero)

    if huesped == -1:
        print(f"No se encontró ningún huésped alojado en la habitación {numero}.")

    return huesped


def pedir_habitacion_destino(matriz_hotel):
    """
    Pide una habitación destino hasta que exista y esté libre.
    Devuelve (piso, habitacion, numero) o (-1, -1, -1) si se cancela.
    """
    destino_elegido = False
    nuevo_piso = 0
    nueva_habitacion = 0
    nuevo_numero = 0

    while destino_elegido == False:
        entrada = validar_generico(
            "Ingrese el nuevo número de habitación (-1 para cancelar): ",
            PATRON_NUMERO_VALIDO,
            ERROR_NUMERO
        )

        if entrada == "-1":
            print("Reubicación cancelada.")
            return -1, -1, -1

        nuevo_numero = int(entrada)
        nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)

        if habitacion_existe(matriz_hotel, nuevo_piso, nueva_habitacion) == False:
            print(f"Error: La habitación {nuevo_numero} no existe en el hotel.")
        elif matriz_hotel[nuevo_piso][nueva_habitacion] != "L":
            print(f"Error: La habitación {nuevo_numero} no está libre.")
        else:
            destino_elegido = True

    return nuevo_piso, nueva_habitacion, nuevo_numero


def mover_huesped(matriz_hotel, huesped, destino):
    """
    Actualiza la matriz y la ubicación del huésped.
    """
    nuevo_piso, nueva_habitacion, nuevo_numero = destino
    piso_actual = huesped["ubicacion"][0]
    habitacion_actual = huesped["ubicacion"][1]

    matriz_hotel[piso_actual][habitacion_actual] = "L"
    matriz_hotel[nuevo_piso][nueva_habitacion] = "O"

    huesped["ubicacion"][0] = nuevo_piso
    huesped["ubicacion"][1] = nueva_habitacion
    huesped["ubicacion"][2] = nuevo_numero


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Coordina la reubicación de un huésped a otra habitación libre.
    """
    print("\n--- REUBICACIÓN DE HUÉSPED (SWAP) ---")

    if puede_reubicar(matriz_hotel, lista_huespedes) == False:
        return

    huesped = pedir_huesped_a_reubicar(lista_huespedes)
    if huesped == -1:
        return

    destino = pedir_habitacion_destino(matriz_hotel)
    if destino == (-1, -1, -1):
        return

    mover_huesped(matriz_hotel, huesped, destino)
    print(f"Huésped {huesped['identidad'][1]} reubicado a habitación {destino[2]} con éxito.")


def restablecer_limpieza(matriz_hotel):
    """
    Restaura una habitación con estado Sucio [S] a estado Libre [L].
    """
    entrada = validar_generico(
        "Ingrese el número de habitación en limpieza (-1 para cancelar): ",
        PATRON_NUMERO_VALIDO,
        ERROR_NUMERO
    )

    if entrada == "-1":
        print("Operación cancelada.")
        return

    piso, habitacion = obtener_indices_matriz(int(entrada))

    if habitacion_existe(matriz_hotel, piso, habitacion) == False:
        print("Error: La habitación ingresada no existe en el hotel.")
        return

    if matriz_hotel[piso][habitacion] != "S":
        print("Error: La habitación no está en limpieza.")
        return

    matriz_hotel[piso][habitacion] = "L"
    print("Habitación restablecida con éxito!")