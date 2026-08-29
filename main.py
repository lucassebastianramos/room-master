import functools
import re

# MÓDULO 1: MATRIZ, CHECK-IN Y VALIDACIONES REGEX (Tiara)

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
    #TODO VER SI SE PUEDE HACER MAS LINDO

    """
    Muestra la matriz en consola desde el piso más alto hasta la Planta Baja.
    Muestra cada habitación con su número comercial (ej: [101: L]).
    """
    print("\nESTADO ACTUAL DEL HOTEL\n")
    for f in range(len(matriz) -1, -1, -1):  # Recorre al revés (piso superior a inferior)
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
            print("Error: El piso o la habitación ingresada no existen en el hotel.")
        elif matriz[piso][hab] != "L":
            print("Error: La habitación no está libre.")
        else:
            es_valida = True
            piso_final = piso
            hab_final = hab
            
    return piso_final, hab_final

def validar_num(mensaje):
    """Pide un valor, valida que sean números y lo devuelve como entero (int)."""
    num = input(mensaje).strip()
    while not re.match(r"^\d+$", num):
        print("Error: Debe ingresar un número entero válido.")
        num = input(mensaje).strip()
    return int(num)

def validar_string(mensaje):
    """Pide un texto y valida que solo contenga letras."""
    palabra = input(mensaje).strip()
    while not re.match(r"^[a-zA-Za-eíóúÁÉÍÓÚñÑ\s]+$", palabra) or len(palabra) == 0:
        print("Error. El texto solo debe contener letras y no puede estar vacío.")
        palabra = input(mensaje).strip()
    return palabra

def validar_dni(mensaje):
    """Pide el DNI y valida su longitud."""
    dni_huesped = input(mensaje).strip()
    while not re.match(r"^\d{7,8}$", dni_huesped):
        print("DNI INVÁLIDO.")
        dni_huesped = input(mensaje).strip()
    return dni_huesped

def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro completo de un nuevo huésped en el sistema.
    Valida datos de los huéspedes con Regex.
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)

    nombre = validar_string("Ingrese el nombre del huésped: ")
    dni = validar_dni("Ingrese el DNI del huésped: ")
    dias = validar_num("Cantidad de días de estadía: ")
    
    num_comercial = obtener_numero_comercial(piso, habitacion)

    # Registro del huésped como lista: [nombre, dni, dias, piso, habitacion]
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial]
    lista_huespedes.append(datos_huesped)

    matriz[piso][habitacion] = "O"
    
    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz

# MÓDULO 2: BÚSQUEDAS, FILTROS Y TARIFAS (Lucas)

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

# MÓDULO 3: CHECK-OUT, SWAP Y TRANSFORMACIONES MAP (Luca)

def realizar_checkout(matriz_hotel, lista_huespedes, matriz_tarifas):
    # TODO (Luca): Liberar habitación, pasar a 'S' (Limpieza) y calcular cobro
    # print("[En desarrollo: Check-out y facturación]")
    print("---CHECK-OUT---")
    DNI_Checkout=int(input("Ingrese el DNI del huesped"))
    buscar_huesped_por_dni(lista_huespedes, DNI_Checkout)
    for huesped in lista_huespedes:
        if str(huesped[1]) == str(DNI_Checkout):
            nombre = huesped[0]
            dias = huesped[2]
            piso = huesped[3]
            habitacion = huesped[4]


            matriz_hotel[piso][habitacion] = "S"
            piso_comercial = piso + 1
            tarifa = float(obtener_tarifa_habitacion(piso_comercial, matriz_tarifas))
            dias_num=int(dias)
            monto_total = tarifa * dias_num
            num_comercial = obtener_numero_comercial(piso, habitacion)

        #Borrar huesped de la lista|
            lista_huespedes.remove(huesped)

        #Recivo
            print("\n================ CHECK-OUT EXITOSO ================")
            print(f"Huésped:             {nombre}")
            print(f"Habitación liberada: {num_comercial}")
            print(f"TOTAL A COBRAR:      ${monto_total:,.2f}")
            print("===================================================")
            return
        
    print(f"No se encontró al huésped con DNI: {DNI_Checkout}")
    

def reubicar_huesped_swap(matriz_hotel, lista_huespedes):
    # TODO (Luca): Trasladar huésped, habitación vieja pasa a 'M' (Mantenimiento)
    # print("[En desarrollo: Reubicación / Swap de habitación]")
    habitacion_swap = int(input("Ingrese el número de habitación a reubicar: "))

    for huesped in lista_huespedes:
        piso = int(huesped[3])
        habitacion = int(huesped[4])
        num_comercial = obtener_numero_comercial(piso, habitacion)

        if num_comercial == habitacion_swap:
            print(f"Huésped encontrado: {huesped[0]} en habitación {num_comercial}")
            nuevo_numero = int(input("Ingrese el nuevo número de habitación: "))
            nuevo_piso, nueva_habitacion = obtener_indices_matriz(nuevo_numero)
        

            # Validar que la nueva habitación esté libre
            if matriz_hotel[nuevo_piso][nueva_habitacion] == "L":
                # Actualizar la matriz y los datos del huésped
                matriz_hotel[piso][habitacion] = "M"  # Habitación vieja pasa a Mantenimiento
                matriz_hotel[nuevo_piso][nueva_habitacion] = "O"  # Nueva habitación ocupada
                huesped[3] = nuevo_piso
                huesped[4] = nueva_habitacion

                print(f"Huésped {huesped[0]} reubicado a habitación {nuevo_numero}.")
                return
            else:
                print("Error: La nueva habitación", nuevo_numero,"esta ocupada.")
        else:
            print("No se encontro ningun huesped en la habitacion",habitacion_swap)
            return

# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (Leandro)

def generar_reporte_ocupacion(matriz_hotel):
    # TODO (Leandro): Porcentaje de ocupación

    habitaciones_ocupadas = 0
    total_habitaciones = 0

    for i in range(len(matriz_hotel)):
        for j in range(len(matriz_hotel[i])):
            total_habitaciones += 1

            if matriz_hotel[i][j] == "O":
                habitaciones_ocupadas += 1

    porcentaje_ocupacion = habitaciones_ocupadas * 100 / total_habitaciones 
    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones: ", total_habitaciones)
    print("Habitaciones ocupadas: ", habitaciones_ocupadas)
    print("Porcentaje de ocupación: ", porcentaje_ocupacion, "%")
    

def calcular_recaudacion_total(lista_huespedes):
    # TODO (Leandro): Uso obligatorio de functools.reduce y lambdas
    print("[En desarrollo: Recaudación total con map/filter/reduce]")


# PROGRAMA PRINCIPAL

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
            print("Configuración de la vista del hotel")
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes,tarifas)
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

        # Muestra el resultado del menu de opciones hasta accion del usuario
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

# Ejecución
menu_principal()
