import functools
import re

# =============================================================================
# MÓDULO 1: MATRIZ, CHECK-IN Y VALIDACIONES REGEX (Tiara)
# =============================================================================

def inicializar_hotel(pisos, habitaciones):
    """
    Crea y retorna la matriz del hotel.
    Estados: 'L' (Libre), 'O' (Ocupada), 'S' (Sucia/Limpieza), 'M' (Mantenimiento).
    """
    matriz = []
    for f in range(pisos):
        fila = []
        for c in range(habitaciones):
            fila.append("L")
        matriz.append(fila)
    return matriz


def renderizar_hotel(matriz):
    """
    Muestra la matriz en consola. Imprime desde el piso más alto
    hasta el piso 0 (Planta Baja) para simular la altura real del edificio.
    """
    print("\nESTADO ACTUAL DEL HOTEL\n")
    for f in range(len(matriz)-1, -1, -1): # Recorre al revés
        print(f"Piso {f}:", end="\t")
        for c in range(len(matriz[0])):
            print(f"[{matriz[f][c]}]", end="\t")
        print()

def reiniciar_matriz():
    """
    Solicita las dimensiones generales (pisos y habitaciones por piso) para instanciar
    una nueva matriz limpia ('L'). Luego de su uso se reinicia la lista de huespedes.
    """
    print("\nDIMENSIONAR / REINICIAR HOTEL")
    pisos = int(input("Ingrese la cantidad de pisos: "))
    habitaciones = int(input("Ingrese la cantidad de habitaciones por piso: "))
    
    return inicializar_hotel(pisos, habitaciones)

def validar_regex(patron, texto):
    """
    Valida cadenas mediante expresiones regulares.
    """
    return bool(re.match(patron, texto))

def pedir_habitacion(matriz):
    '''
    Pide al usuario el número de piso y habitación dentro del rango
    de la matriz ya existente para realizar una operación puntual.
    '''
    piso = int(input(f"Ingrese el piso (0 a {len(matriz) - 1}): "))
    habitacion = int(input(f"Ingrese la habitación (0 a {len(matriz[0]) - 1}): "))
    return piso, habitacion

def validar_habitacion(piso, habitacion, matriz):
    '''
    Valida el numero de piso y habitacion ingresados, verificando que exista
    el rango en las dimensiones del hotel y la habitacion no este ocupada.
    '''
    es_valida = False
    
    while not es_valida:
        if piso < 0 or piso >= len(matriz) or habitacion < 0 or habitacion >= len(matriz[0]):
            print("Error: El piso o la habitación ingresada no existen en el hotel.")
            piso, habitacion = pedir_habitacion(matriz)
            
        elif matriz[piso][habitacion] != "L":
            print("Error: La habitación no está libre.")
            piso, habitacion = pedir_habitacion(matriz)
            
        else:
            es_valida = True

    return piso, habitacion

def realizar_checkin(matriz, lista_huespedes):
    '''
    Gestiona el registro completo de un nuevo huésped en el sistema.
    Solicita y valida una habitación disponible, recopila los datos personales del
    huésped, almacena el registro en 'lista_huespedes' y actualiza el estado de la 
    habitación a "ocupada" en la matriz.
    '''
    # TODO (Tiara): Validar datos de los huespedes con Regex. Evaluar si pedir 
    # mas datos al huesped para reportes

    piso, habitacion = pedir_habitacion(matriz)
    piso, habitacion = validar_habitacion(piso, habitacion, matriz)
    
    nombre = input("Ingrese el nombre del huésped: ")
    dni = input("Ingrese el DNI del huésped: ")
    dias = input("Cantidad de días de estadía: ")
    
    # Registro del huésped como lista: [nombre, dni, dias, piso, habitacion]
    datos_huesped = [nombre, dni, dias, piso, habitacion]
    lista_huespedes.append(datos_huesped)

    matriz[piso][habitacion] = "O"
    print(f"\n[Check-in exitoso] {nombre} registrado en Piso {piso}, Habitación {habitacion}.")

    return matriz

# =============================================================================
# MÓDULO 2: BÚSQUEDAS, FILTROS Y TARIFAS (Lucas)
# =============================================================================

def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de huéspedes (sublistas).
    Estructura de cada registro: [nombre, dni, dias, piso, habitacion]
    """
    encontrado = False
    
    for i in range(len(lista_huespedes)):
        huesped = lista_huespedes[i]
        nombre = huesped[0]
        dni_actual = huesped[1]
        dias = huesped[2]
        piso = huesped[3]
        hab = huesped[4]
        
        if str(dni_actual) == str(dni_busqueda):
            encontrado = True
            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print("Nombre:         ", nombre)
            print("DNI:            ", dni_actual)
            print("Días de estadía:", dias)
            print("Piso asignado:  ", piso)
            print("Habitación:     ", hab)
            print("====================================")
            
    if not encontrado:
        print("\n[Aviso] No se encontró ningún huésped alojado con el DNI:", dni_busqueda)


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    matriz_tarifas tiene pares: [piso, precio_base]
    """
    precio = 0.0
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            precio = matriz_tarifas[i][1]
    return precio


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Uso de 'filter' y 'lambda' para aislar los huéspedes de un piso específico.
    Cumple con el requisito de funciones de orden superior y listas avanzadas.
    """
    # El índice 3 de cada sublista corresponde al piso
    filtrados = list(filter(lambda huesped: int(huesped[3]) == int(piso_objetivo), lista_huespedes))
    return filtrados


# =============================================================================
# MÓDULO 3: CHECK-OUT, SWAP Y TRANSFORMACIONES MAP (Luca)
# =============================================================================

def realizar_checkout(matriz_hotel, lista_huespedes):
    # TODO (Luca): Liberar habitación, pasar a 'S' (Limpieza) y calcular cobro
    print("[En desarrollo: Check-out y facturación]")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    # TODO (Luca): Trasladar huésped, habitación vieja pasa a 'M' (Mantenimiento)
    print("[En desarrollo: Reubicación / Swap de habitación]")


# =============================================================================
# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (Leandro)
# =============================================================================

def generar_reporte_ocupacion(matriz_hotel):
    # TODO (Leandro): Porcentaje de ocupación
    print("[En desarrollo: Cálculo de porcentaje de ocupación]")


def calcular_recaudacion_total(lista_huespedes):
    # TODO (Leandro): Uso obligatorio de functools.reduce y lambdas
    print("[En desarrollo: Recaudación total con map/filter/reduce]")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def menu_principal():

    # Inicializa matriz (reiniciar_matriz() se reutiliza para redimensionar el hotel)
    hotel = reiniciar_matriz()
    
    # Matriz de tarifas: [ [Piso, Precio por noche], ... ]
    tarifas = [
        [1, 50000.0],  # Piso 1 (Estándar)
        [2, 75000.0],  # Piso 2 (Superior)
        [3, 110000.0]  # Piso 3 (Suite)
    ]
    
    # Registro de huéspedes (Formato: [nombre, dni, dias, piso, habitacion])
    huespedes = []
    
    ejecutando = True
    
    while ejecutando:
        print("\nROOM MASTER - MENÚ PRINCIPAL\n")

        print("1. Visualizar estado del hotel")
        print("2. Check-in (Nuevo huésped)")
        print("3. Check-out (Liberar habitación)")
        print("4. Reubicar huésped (Swap)")
        print("5. Buscar huésped por DNI")
        print("6. Reportes y Facturación")
        print("7. Redimensionar hotel")
        print("0. Salir")
        print("==============================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            hotel = realizar_checkin(hotel, huespedes)
            # hacerlo con datos de lista huespedes para evitar print dentro de realizar_checkin
            # print(f"Check-in exitoso. {nombre} registrado en piso {piso}, habitación {habitacion}.")
        elif opcion == "3":
            realizar_checkout(hotel, huespedes)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            dni_busqueda = input("Ingrese el DNI a buscar: ")
            buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes)
        elif opcion == "7":
            hotel = reiniciar_matriz()
            huespedes.clear()
            print("Hotel redimensionado y reiniciado con éxito")
        elif opcion == "0":
            print("Saliendo del sistema Room Master...")
            ejecutando = False  # Sale del bucle
        else:
            print("Opción inválida. Intente nuevamente.")
        
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

# Ejecución
menu_principal()
