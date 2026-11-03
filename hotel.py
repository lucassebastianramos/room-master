# =============================================================================
# MÓDULO 1: MATRIZ Y GESTIÓN DE HABITACIONES (hotel.py)
# =============================================================================

from validaciones import (
    validar_generico,
    solicitar_dimension_valida,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)


def inicializar_hotel(pisos, habitaciones):
    """
    Crea y retorna la matriz del hotel.
    Estados: 'L' (Libre), 'O' (Ocupada), 'S' (Sucia/Limpieza).

    >>> inicializar_hotel(2, 3)
    [['L', 'L', 'L'], ['L', 'L', 'L']]
    >>> inicializar_hotel(1, 1)
    [['L']]
    """
    matriz = []
    for f in range(pisos):
        fila = []
        for c in range(habitaciones):
            fila.append("L")
        matriz.append(fila)
    return matriz


def obtener_numero_comercial(piso, habitacion):
    """
    Convierte índices de matriz (0, 0) a número comercial visible (101).

    >>> obtener_numero_comercial(0, 0)
    101
    >>> obtener_numero_comercial(2, 4)
    305
    """
    n_habitacion = (piso + 1) * 100 + (habitacion + 1)
    return n_habitacion


def obtener_indices_matriz(numero_comercial):
    """
    Convierte el número comercial visible (101) a índices de matriz (0, 0).

    >>> obtener_indices_matriz(101)
    (0, 0)
    >>> obtener_indices_matriz(305)
    (2, 4)
    """
    piso = (numero_comercial // 100) - 1
    habitacion = (numero_comercial % 100) - 1
    return piso, habitacion


def renderizar_hotel(matriz):
    """
    Muestra la matriz en consola desde el piso más alto hasta el más bajo.
    Hace un salto de línea cada 10 habitaciones para evitar que la pantalla se desborde.
    """
    print("\n--- ESTADO ACTUAL DEL HOTEL ---")
    print("Estados: [L] Libre | [O] Ocupada | [S] Sucia\n")

    for f in range(len(matriz) - 1, -1, -1):
        print(f"Piso {f + 1}:")

        for c in range(len(matriz[0])):
            num_hab = obtener_numero_comercial(f, c)
            print(f"[{num_hab}: {matriz[f][c]}]", end="  ")

            if (c + 1) % 10 == 0:
                print()

        print("\n")


def reiniciar_matriz():
    """Inicialización de la matriz del hotel al arrancar el programa."""
    print("\n--- INICIALIZACIÓN DEL SISTEMA ROOM MASTER ---")
    pisos = solicitar_dimension_valida("Ingrese la cantidad de pisos del hotel (1 a 99): ", 1, 99, permitir_cancelar=False)
    habitaciones = solicitar_dimension_valida("Ingrese la cantidad de habitaciones por piso (1 a 99): ", 1, 99, permitir_cancelar=False)
    
    return inicializar_hotel(pisos, habitaciones)


def redimensionar_hotel():
    """Opción 7: Reinicia el hotel perdiendo los datos. Permite cancelar."""
    print("\n" + "!" * 55)
    print(" ADVERTENCIA: REDIMENSIONAMIENTO DEL HOTEL")
    print(" Esta acción borrará a todos los huéspedes alojados")
    print(" y reiniciará el estado de todas las habitaciones.")
    print(" Úselo SOLAMENTE si ha cambiado la estructura edilicia.")
    print("!" * 55)

    pisos = solicitar_dimension_valida("\nNueva cantidad de pisos (-1 para cancelar): ", 1, 99, permitir_cancelar=True)
    if pisos == -1:
        return -1
        
    habitaciones = solicitar_dimension_valida("Nueva cantidad de habitaciones por piso (-1 para cancelar): ", 1, 99, permitir_cancelar=True)
    if habitaciones == -1:
        return -1
        
    return inicializar_hotel(pisos, habitaciones)


def hay_habitaciones_libres(matriz):
    """
    Devuelve True si hay al menos una habitación en estado Libre ('L').

    >>> hay_habitaciones_libres([['L', 'O'], ['O', 'O']])
    True
    >>> hay_habitaciones_libres([['O', 'O'], ['S', 'O']])
    False
    """
    for fila in matriz:
        for estado in fila:
            if estado == "L":
                return True
    return False


def habitacion_existe(matriz, piso, habitacion):
    """
    Devuelve True si el piso y la habitación existen dentro de la matriz.

    >>> matriz = [['L', 'L'], ['L', 'L']]
    >>> habitacion_existe(matriz, 0, 1)
    True
    >>> habitacion_existe(matriz, 2, 0)
    False
    >>> habitacion_existe(matriz, -1, 0)
    False
    """
    if piso < 0 or piso >= len(matriz):
        return False
    if habitacion < 0 or habitacion >= len(matriz[0]):
        return False
    return True


def solicitar_habitacion_libre(matriz):
    """Pide y valida una habitación libre."""
    if hay_habitaciones_libres(matriz) == False:
        print("\n[Aviso] El hotel se encuentra completo. No hay habitaciones libres disponibles.")
        return -1, -1

    es_valida = False
    piso_final = 0
    hab_final = 0

    while es_valida == False:
        dato = validar_generico("\nIngrese el número de habitación (ej: 101) (-1 para cancelar): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO)
        if dato == "-1":
            return -1, -1

        piso, hab = obtener_indices_matriz(int(dato))

        if habitacion_existe(matriz, piso, hab) == False:
            print("Error: La habitación ingresada no existe en el hotel.")
        elif matriz[piso][hab] != "L":
            print("Error: La habitación no está libre.")
        else:
            es_valida = True
            piso_final = piso
            hab_final = hab

    return piso_final, hab_final


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
