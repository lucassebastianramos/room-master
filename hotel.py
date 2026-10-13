# =============================================================================
# MÓDULO DE GESTIÓN DE MATRICES Y HOTEL (hotel.py)
# =============================================================================
# Responsabilidad: Creación, conversión de coordenadas, visualización y
# control de estados y disponibilidad de las habitaciones del hotel.
# Estados: 'L' (Libre), 'O' (Ocupada), 'S' (Sucia/Limpieza).
# =============================================================================

from validaciones import (
    validar_generico,
    solicitar_dimension_valida,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)


def inicializar_hotel(pisos, habitaciones):
    """
    Crea y retorna una nueva matriz bidimensional para el hotel.
    Todas las habitaciones se inicializan con estado 'L' (Libre).
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
    Convierte índices de matriz basados en cero (0, 0) a número comercial visible (101).
    """
    n_habitacion = (piso + 1) * 100 + (habitacion + 1)
    return n_habitacion


def obtener_indices_matriz(numero_comercial):
    """
    Convierte el número comercial visible (101) a índices de matriz (0, 0).
    """
    piso = (numero_comercial // 100) - 1
    habitacion = (numero_comercial % 100) - 1
    return piso, habitacion


def renderizar_hotel(matriz):
    """
    Muestra la matriz en consola desde el piso más alto hasta el más bajo.
    Hace un salto de línea cada 10 habitaciones para evitar desbordes de pantalla.
    """
    print("\n--- ESTADO ACTUAL DEL HOTEL ---")
    print("Estados: [L] Libre | [O] Ocupada | [S] Sucia\n")

    for f in range(len(matriz) - 1, -1, -1):
        print(f"Piso {f + 1}:")

        for c in range(len(matriz[0])):
            num_hab = obtener_numero_comercial(f, c)
            print(f"[{num_hab}: {matriz[f][c]}]", end="  ")

            # Al llegar a 10 habitaciones hace un salto de línea
            if (c + 1) % 10 == 0:
                print()

        print("\n")  # Separación entre pisos


def hay_habitaciones_disponibles(matriz):
    """
    Verifica si existe al menos una habitación con estado 'L' (Libre) en el hotel.
    Previene el bucle infinito cuando el hotel se encuentra al 100% de ocupación.
    """
    for fila in matriz:
        if "L" in fila:
            return True
    return False


def solicitar_habitacion_libre(matriz):
    """
    Pide y valida una habitación libre.
    Si el hotel está lleno o el usuario ingresa 0, cancela la operación de forma segura.
    Retorna (piso, habitacion) o (None, None) si se cancela.
    """
    if not hay_habitaciones_disponibles(matriz):
        print("\n[Aviso] El hotel se encuentra 100% completo. No hay habitaciones libres disponibles.")
        return None, None

    es_valida = False
    piso_final = None
    hab_final = None

    while not es_valida:
        num_comercial = int(validar_generico(
            "\nIngrese el número de habitación (ej: 101, o 0 para cancelar): ",
            PATRON_NUMERO_VALIDO,
            ERROR_NUMERO
        ))

        if num_comercial == 0:
            print("\n[Operación cancelada] Regresando al menú...")
            return None, None

        piso, hab = obtener_indices_matriz(num_comercial)

        if piso < 0 or piso >= len(matriz) or hab < 0 or hab >= len(matriz[0]):
            print("Error: El piso o la habitación ingresada no existen en el hotel.")
        elif matriz[piso][hab] != "L":
            print(f"Error: La habitación {num_comercial} no está libre (estado actual: [{matriz[piso][hab]}]).")
        else:
            es_valida = True
            piso_final = piso
            hab_final = hab

    return piso_final, hab_final


def reiniciar_matriz():
    """
    Solicita las dimensiones validadas e instancia una nueva matriz limpia ('L').
    """
    print("--- Inicializar matriz ---\n")
    pisos = solicitar_dimension_valida("Ingrese la cantidad de pisos del hotel (1 a 99): ", 1, 99)
    habitaciones = solicitar_dimension_valida("Ingrese la cantidad de habitaciones por piso (1 a 99): ", 1, 99)
    return inicializar_hotel(pisos, habitaciones)
