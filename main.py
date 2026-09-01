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


def obtener_numero_comercial(piso, habitacion):
    """
    Convierte índices de matriz (0, 0) a número comercial visible (101).
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


def validar_num(mensaje):
    """Pide un valor, valida que sean números enteros positivos y lo devuelve como int."""
    num = input(mensaje).strip()
    while not re.match(r"^\d+$", num):
        print("Error: Debe ingresar un número entero válido.")
        num = input(mensaje).strip()
    return int(num)


def validar_string(mensaje):
    """Pide un texto y valida que solo contenga letras y espacios."""
    palabra = input(mensaje).strip()
    while not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", palabra) or len(palabra) == 0:
        print("Error: El texto solo debe contener letras y no puede estar vacío.")
        palabra = input(mensaje).strip()
    return palabra


def validar_dni(mensaje):
    """Pide el DNI y valida que contenga entre 7 y 8 dígitos numéricos."""
    dni_huesped = input(mensaje).strip()
    while not re.match(r"^\d{7,8}$", dni_huesped):
        print("Error: DNI inválido. Debe contener entre 7 y 8 dígitos numéricos.")
        dni_huesped = input(mensaje).strip()
    return dni_huesped


def solicitar_dimension_valida(mensaje, min_val, max_val):
    """
    Solicita una entrada al usuario y valida únicamente que se encuentre
    dentro del rango (min_val, max_val).
    """
    es_valido = False
    valor_num = 0

    while not es_valido:
        valor_num = validar_num(mensaje)
        if min_val <= valor_num <= max_val:
            es_valido = True
        else:
            print(f"Error: El valor debe estar entre {min_val} y {max_val}.")

    return valor_num


def renderizar_hotel(matriz):
    """
    Muestra la matriz en consola desde el piso más alto hasta la Planta Baja.
    Muestra cada habitación con su número comercial (ej: [101: L]).
    """
    print("\nESTADO ACTUAL DEL HOTEL\n")
    for f in range(len(matriz) - 1, -1, -1):  # Recorre al revés (piso superior a inferior)
        print(f"Piso {f + 1}:", end="\t")
        for c in range(len(matriz[0])):
            num_hab = obtener_numero_comercial(f, c)
            print(f"[{num_hab}: {matriz[f][c]}]", end="\t")
        print()


def reiniciar_matriz():
    """
    Solicita las dimensiones validadas e instancia una nueva matriz limpia ('L').
    """
    pisos = solicitar_dimension_valida("Ingrese la cantidad de pisos (1 a 99): ", 1, 99)
    habitaciones = solicitar_dimension_valida("Ingrese la cantidad de habitaciones por piso (1 a 99): ", 1, 99)
    return inicializar_hotel(pisos, habitaciones)


def solicitar_habitacion_libre(matriz):
    """Pide y valida una habitación libre."""
    es_valida = False
    piso_final = 0
    hab_final = 0
    
    while not es_valida:
        num_comercial = validar_num("\nIngrese el número de habitación (ej: 101): ")
        piso, hab = obtener_indices_matriz(num_comercial)
        
        if piso < 0 or piso >= len(matriz) or hab < 0 or hab >= len(matriz[0]):
            print(f"Error: La habitación {num_comercial} no existe en el hotel.")
        elif matriz[piso][hab] != "L":
            print(f"Error: La habitación {num_comercial} no está libre (Estado actual: {matriz[piso][hab]}).")
        else:
            es_valida = True
            piso_final = piso
            hab_final = hab
            
    return piso_final, hab_final


def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro completo de un nuevo huésped en el sistema.
    Valida datos de los huéspedes con Regex.
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)

    nombre = validar_string("Ingrese el nombre del huésped: ")
    dni = validar_dni("Ingrese el DNI del huésped: ")
    dias = solicitar_dimension_valida("Cantidad de días de estadía (1 a 365): ", 1, 365)
    
    num_comercial = obtener_numero_comercial(piso, habitacion)

    # Registro del huésped como lista: [nombre, dni, dias, piso, habitacion, num_comercial]
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial]
    lista_huespedes.append(datos_huesped)

    matriz[piso][habitacion] = "O"
    
    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz


# =============================================================================
# MÓDULO 2: BÚSQUEDAS, FILTROS Y TARIFAS (Lucas)
# =============================================================================

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
        num_comercial = huesped[5] if len(huesped) > 5 else obtener_numero_comercial(piso, hab)
        
        if str(dni_actual) == str(dni_busqueda):
            encontrado = True
            print("\n=== DATOS DEL HUÉSPED ENCONTRADO ===")
            print("Nombre:         ", nombre)
            print("DNI:            ", dni_actual)
            print("Días de estadía:", dias)
            print("Piso asignado:  ", piso + 1)
            print("Habitación:     ", num_comercial)
            print("====================================")
            
    if not encontrado:
        print("\n[Aviso] No se encontró ningún huésped alojado con el DNI:", dni_busqueda)


def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    matriz_tarifas tiene pares: [piso, precio_base]
    """
    precio = matriz_tarifas[-1][1] if matriz_tarifas else 0.0
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            precio = matriz_tarifas[i][1]
    return precio


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Uso de 'filter' y 'lambda' para aislar los huéspedes de un piso específico.
    Cumple con el requisito de funciones de orden superior y listas avanzadas.
    """
    # El índice 3 de cada sublista corresponde al piso (0-indexed)
    filtrados = list(filter(lambda huesped: (int(huesped[3]) + 1) == int(piso_objetivo), lista_huespedes))
    return filtrados


# =============================================================================
# MÓDULO 3: CHECK-OUT, SWAP Y TRANSFORMACIONES MAP (Luca)
# =============================================================================

def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    """
    Realiza el Check-out de un huésped dado su DNI, libera la habitación pasándola a 'S' (Limpieza)
    y calcula la facturación correspondiente.
    """
    if len(lista_huespedes) == 0:
        print("\n[Aviso] No hay huéspedes alojados actualmente en el hotel.")
        return

    print("\n--- CHECK-OUT ---")
    dni_checkout = validar_dni("Ingrese el DNI del huésped: ")

    huesped_encontrado = None
    for huesped in lista_huespedes:
        if str(huesped[1]) == str(dni_checkout):
            huesped_encontrado = huesped
            break

    if huesped_encontrado is None:
        print(f"\n[Aviso] No se encontró ningún huésped alojado con el DNI: {dni_checkout}")
        return

    nombre = huesped_encontrado[0]
    dni = huesped_encontrado[1]
    dias = int(huesped_encontrado[2])
    piso = int(huesped_encontrado[3])
    habitacion = int(huesped_encontrado[4])
    num_comercial = huesped_encontrado[5] if len(huesped_encontrado) > 5 else obtener_numero_comercial(piso, habitacion)

    matriz_hotel[piso][habitacion] = "S"  # Pasa a sucia/limpieza
    piso_comercial = piso + 1
    tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
    monto_total = tarifa * dias

    lista_huespedes.remove(huesped_encontrado)

    print("\n================ CHECK-OUT EXITOSO ================")
    print(f"Huésped:             {nombre}")
    print(f"DNI:                 {dni}")
    print(f"Habitación liberada: {num_comercial} (Piso {piso_comercial})")
    print(f"Días de estadía:     {dias}")
    print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
    print("===================================================")


def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    """
    Traslada un huésped a una nueva habitación libre.
    La habitación anterior pasa a estado 'M' (Mantenimiento).
    """
    if len(lista_huespedes) == 0:
        print("\n[Aviso] No hay huéspedes alojados actualmente en el hotel.")
        return

    habitacion_swap = validar_num("Ingrese el número de habitación a reubicar (ej: 101): ")

    huesped_encontrado = None
    for huesped in lista_huespedes:
        piso = int(huesped[3])
        habitacion = int(huesped[4])
        num_comercial = huesped[5] if len(huesped) > 5 else obtener_numero_comercial(piso, habitacion)

        if num_comercial == habitacion_swap:
            huesped_encontrado = huesped
            break

    if huesped_encontrado is None:
        print(f"\n[Aviso] No se encontró ningún huésped alojado en la habitación {habitacion_swap}.")
        return

    print(f"Huésped encontrado: {huesped_encontrado[0]} en habitación {habitacion_swap}")
    nuevo_numero = validar_num("Ingrese el nuevo número de habitación (ej: 102): ")
    nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)

    if (nuevo_piso < 0 or nuevo_piso >= len(matriz_hotel) or 
        nueva_habitacion < 0 or nueva_habitacion >= len(matriz_hotel[0])):
        print(f"Error: La habitación {nuevo_numero} no existe en el hotel.")
        return

    if matriz_hotel[nuevo_piso][nueva_habitacion] == "L":
        piso_viejo = int(huesped_encontrado[3])
        hab_vieja = int(huesped_encontrado[4])

        matriz_hotel[piso_viejo][hab_vieja] = "M"  # Habitación vieja pasa a Mantenimiento
        matriz_hotel[nuevo_piso][nueva_habitacion] = "O"  # Nueva habitación ocupada
        
        huesped_encontrado[3] = nuevo_piso
        huesped_encontrado[4] = nueva_habitacion
        if len(huesped_encontrado) > 5:
            huesped_encontrado[5] = nuevo_numero
        else:
            huesped_encontrado.append(nuevo_numero)

        print(f"\n[Reubicación exitosa] {huesped_encontrado[0]} reubicado a la habitación {nuevo_numero}.")
    else:
        print(f"Error: La nueva habitación {nuevo_numero} no está libre (Estado actual: {matriz_hotel[nuevo_piso][nueva_habitacion]}).")


# =============================================================================
# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (Leandro)
# =============================================================================

def generar_reporte_ocupacion(matriz_hotel):
    """
    Genera un reporte que muestra el total de habitaciones,
    las que se encuentran ocupadas y el porcentaje de ocupación del hotel.
    """
    habitaciones_ocupadas = 0
    total_habitaciones = 0

    for i in range(len(matriz_hotel)):
        for j in range(len(matriz_hotel[i])):
            total_habitaciones += 1
            if matriz_hotel[i][j] == "O":
                habitaciones_ocupadas += 1

    porcentaje_ocupacion = (habitaciones_ocupadas * 100 / total_habitaciones) if total_habitaciones > 0 else 0.0
    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones:  ", total_habitaciones)
    print("Habitaciones ocupadas:  ", habitaciones_ocupadas)
    print(f"Porcentaje de ocupación: {porcentaje_ocupacion:.2f}%")


def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a cobrar por un huésped específico y aplica un descuento del 10% si su estadía es mayor a 7 noches.
    """
    dias = int(huesped[2])
    piso = int(huesped[3])

    precio_noche = obtener_tarifa_habitacion(piso + 1, matriz_tarifas)
    subtotal = precio_noche * dias

    aplicar_descuento = lambda d, st: st * 0.9 if d > 7 else st
    subtotal = aplicar_descuento(dias, subtotal)

    return subtotal


def calcular_recaudacion_total(lista_huespedes, matriz_tarifas):
    """
    Calcula la recaudación total del hotel sumando los subtotales de todos los huéspedes.
    Uso de functools.reduce y lambdas.
    """
    if len(lista_huespedes) == 0:
        print("\n=== RECAUDACIÓN TOTAL ===")
        print("Recaudación total: $0.00")
        return

    recaudacion_total = functools.reduce(
        lambda total, huesped: total + calcular_subtotal(huesped, matriz_tarifas),
        lista_huespedes,
        0
    )

    print("\n=== RECAUDACIÓN TOTAL ===")
    print(f"Recaudación total: ${recaudacion_total:,.2f}")


# =============================================================================
# MÓDULO 5: RESTABLECER ESTADO DE HABITACIÓN A "L" (Luca)
# =============================================================================

def restablecer_mantenimiento(matriz_hotel):
    num_comercial = validar_num("Ingrese el número de habitación en mantenimiento (ej: 101): ")
    piso, habitacion = obtener_indices_matriz(num_comercial)
    
    if piso < 0 or piso >= len(matriz_hotel) or habitacion < 0 or habitacion >= len(matriz_hotel[0]):
        print(f"Error: La habitación {num_comercial} no existe en el hotel.")
        return

    if matriz_hotel[piso][habitacion] == "M":
        matriz_hotel[piso][habitacion] = "L"
        print(f"Habitación {num_comercial} restablecida a Libre ('L') con éxito.")
    else:
        print(f"Error: La habitación {num_comercial} no está en mantenimiento (Estado actual: {matriz_hotel[piso][habitacion]}).")


def restablecer_limpieza(matriz_hotel):
    num_comercial = validar_num("Ingrese el número de habitación en limpieza (ej: 101): ")
    piso, habitacion = obtener_indices_matriz(num_comercial)
    
    if piso < 0 or piso >= len(matriz_hotel) or habitacion < 0 or habitacion >= len(matriz_hotel[0]):
        print(f"Error: La habitación {num_comercial} no existe en el hotel.")
        return

    if matriz_hotel[piso][habitacion] == "S":
        matriz_hotel[piso][habitacion] = "L"
        print(f"Habitación {num_comercial} restablecida a Libre ('L') con éxito.")
    else:
        print(f"Error: La habitación {num_comercial} no está en limpieza (Estado actual: {matriz_hotel[piso][habitacion]}).")


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
    
    # Registro de huéspedes (Formato: [nombre, dni, dias, piso, habitacion, num_comercial])
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
        print("8. Restablecer habitación (Limpieza / Mantenimiento)")
        print("0. Salir")
        print("==============================")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            dni_busqueda = validar_dni("Ingrese el DNI a buscar: ")
            buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes, tarifas)
        elif opcion == "7":
            hotel = reiniciar_matriz()
            huespedes.clear()
            print("\nHotel redimensionado y reiniciado con éxito.")
        elif opcion == "8":
            print("\n--- RESTABLECER HABITACIÓN ---")
            print("1. Restablecer habitación en Limpieza ('S' -> 'L')")
            print("2. Restablecer habitación en Mantenimiento ('M' -> 'L')")
            print("==============================")

            opcion_restablecer = solicitar_dimension_valida("Seleccione una opción (1 o 2): ", 1, 2)

            if opcion_restablecer == 1:
                restablecer_limpieza(hotel)
            elif opcion_restablecer == 2:
                restablecer_mantenimiento(hotel)
        elif opcion == "0":
            print("\nSaliendo del sistema Room Master...")
            ejecutando = False  # Sale del bucle
        else:
            print("\nError: Opción inválida. Intente nuevamente.")

        # Muestra el resultado del menú de opciones hasta acción del usuario
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

# Ejecución
menu_principal()
