import functools
import re

# =============================================================================
# MÓDULO 1: MATRIZ, CHECK-IN Y VALIDACIONES REGEX (Tiara)
# =============================================================================

def inicializar_hotel(pisos, habitaciones_por_piso):
    """
    Crea y retorna la matriz del hotel.
    Estados: 'L' (Libre), 'O' (Ocupada), 'S' (Sucia/Limpieza), 'M' (Mantenimiento).
    """
    matriz = []
    for _ in range(pisos):
        fila = []
        for _ in range(habitaciones_por_piso):
            fila.append("L")
        matriz.append(fila)
    return matriz


def renderizar_hotel(matriz):
    """
    Muestra en consola el estado visual de cada piso y habitación.
    """
    print("\n--- ESTADO ACTUAL DEL HOTEL ---")
    for i in range(len(matriz)):
        print(f"Piso {i + 1}:", end="  ")
        for j in range(len(matriz[i])):
            print(f"[{matriz[i][j]}]", end=" ")
        print()
    print("-------------------------------")


def validar_regex(patron, texto):
    """
    Valida cadenas mediante expresiones regulares.
    """
    return bool(re.match(patron, texto))


def realizar_checkin(matriz_hotel, lista_huespedes):
    # TODO (Tiara): Validar datos con Regex y cambiar estado a 'O'
    print("[En desarrollo: Check-in y validación de huéspedes]")


# =============================================================================
# MÓDULO 2: BÚSQUEDAS, FILTROS Y TARIFAS (Lucas)
# =============================================================================

def buscar_huesped_por_dni(lista_huespedes, dni_busqueda):
    """
    Realiza una búsqueda secuencial en la lista de cadenas formateadas.
    Estructura del string: "DNI;Nombre;Email;Tel;Piso;Hab;Dias"
    """
    encontrado = False
    
    for i in range(len(lista_huespedes)):
        # Desarmamos el registro usando split
        datos = lista_huespedes[i].split(";")
        dni_actual = datos[0]
        
        if dni_actual == dni_busqueda:
            encontrado = True
            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print("DNI:            ", datos[0])
            print("Nombre:         ", datos[1])
            print("Email:          ", datos[2])
            print("Teléfono:       ", datos[3])
            print("Piso asignado:  ", datos[4])
            print("Habitación:     ", datos[5])
            print("Días de estadía:", datos[6])
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
    # El índice 4 del string separado corresponde al número de piso
    filtrados = list(filter(lambda registro: int(registro.split(";")[4]) == piso_objetivo, lista_huespedes))
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
    # Inicialización predeterminada (3 pisos x 4 habitaciones)
    pisos = 3
    habitaciones_por_piso = 4
    hotel = inicializar_hotel(pisos, habitaciones_por_piso)
    
    # Matriz de tarifas: [ [Piso, Precio por noche], ... ]
    tarifas = [
        [1, 50000.0],  # Piso 1 (Estándar)
        [2, 75000.0],  # Piso 2 (Superior)
        [3, 110000.0]  # Piso 3 (Suite)
    ]
    
    # Registro de huéspedes (Formato: "DNI;Nombre;Email;Tel;Piso;Hab;Dias")
    huespedes = []
    
    opcion = ""
    while opcion != "0":
        print("\n==============================")
        print("     ROOM MASTER - PANEL      ")
        print("==============================")
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
            realizar_checkin(hotel, huespedes)
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
            nuevos_pisos = int(input("Ingrese cantidad de pisos: "))
            nuevas_hab = int(input("Ingrese habitaciones por piso: "))
            hotel = inicializar_hotel(nuevos_pisos, nuevas_hab)
            huespedes = []
            print("Hotel redimensionado y reiniciado exitosamente.")
        elif opcion == "0":
            print("Saliendo del sistema Room Master...")
        else:
            print("Opción inválida. Intente nuevamente.")
        
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

# Ejecución
menu_principal()
