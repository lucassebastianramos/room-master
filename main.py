import functools
import re

# MÓDULO 1: MATRIZ, CHECK-IN Y VALIDACIONES REGEX (Tiara)

def inicializar_hotel(pisos, habitaciones):
    """
    Crea y retorna la matriz del hotel.
    Estados: 'L' (Libre), 'O' (Ocupada), 'S' (Sucia/Limpieza).
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
        valor_num = int(validar_generico(mensaje, PATRON_NUMERO_VALIDO, ERROR_NUMERO))
        if min_val <= valor_num <= max_val:
            es_valido = True
        else:
            print(f"Error: El valor debe estar entre {min_val} y {max_val}.")

    return valor_num


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
            
            # Al llegar a 10 habitaciones hace un salto de línea
            if (c + 1) % 10 == 0:
                print()
                
        print("\n")  # Separación entre pisos


def reiniciar_matriz():
    """
    Solicita las dimensiones validadas e instancia una nueva matriz limpia ('L').
    """

    print("--- Inicializar matriz ---\n")

    pisos = solicitar_dimension_valida("Ingrese la cantidad de pisos del hotel (1 a 99): ", 1, 99)
    habitaciones = solicitar_dimension_valida("Ingrese la cantidad de habitaciones por piso (1 a 99): ", 1, 99)
    return inicializar_hotel(pisos, habitaciones)

def solicitar_habitacion_libre(matriz):
    """Pide y valida una habitación libre."""
    es_valida = False
    piso_final = 0
    hab_final = 0
    
    while not es_valida:
        num_comercial = int(validar_generico("\nIngrese el número de habitación (ej: 101): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
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

PATRON_NUMERO_VALIDO = r"^\d+$"
PATRON_DNI_VALIDO = r"^\d{7,8}$"
PATRON_TEXTO_VALIDO = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
PATRON_DIAS_VALIDO = r"^[1-9]\d*$"

ERROR_NUMERO = "Error: Debe ingresar un número entero válido."
ERROR_DNI = "DNI INVÁLIDO."
ERROR_TEXTO = "Error. El texto solo debe contener letras y no debe estar vacío."
ERROR_DIAS = "Error: La cantidad de días debe ser mayor a 0."


def validar_generico(mensaje, patron, mensaje_error):
    """Pide un dato, lo valida contra 'patron' hasta que sea correcto y lo devuelve como texto."""
    dato_ingresado = input(mensaje).strip()
    while not re.match(patron, dato_ingresado):
        print(mensaje_error)
        dato_ingresado = input(mensaje).strip()
    return dato_ingresado

def realizar_checkin(matriz, lista_huespedes):
    """
    Gestiona el registro completo de un nuevo huésped en el sistema.
    Valida datos de los huéspedes con Regex.
    """
    piso, habitacion = solicitar_habitacion_libre(matriz)

    nombre = validar_generico("Ingrese el nombre del huésped: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    dni = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
    dias = int(validar_generico("Cantidad de días de estadía: ", PATRON_DIAS_VALIDO, ERROR_DIAS))

    num_comercial = obtener_numero_comercial(piso, habitacion)

    # Registro del huésped como lista: [nombre, dni, dias, piso, habitacion, num_comercial]
    datos_huesped = [nombre, dni, dias, piso, habitacion, num_comercial]
    lista_huespedes.append(datos_huesped)

    matriz[piso][habitacion] = "O"
    
    print(f"\n[Check-in exitoso] {nombre} registrado en habitación {num_comercial} (piso {piso + 1}).")

    return matriz

# MÓDULO 2: BÚSQUEDAS, FILTROS Y TARIFAS (Lucas)

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


def configurar_tarifas_hotel(total_pisos):
    """
    Permite configurar dinámicamente las tarifas del hotel por piso.
    Permite definir un precio base general y segmentar pisos superiores como lujosos/suites con recargo.
    Retorna una matriz de tarifas: [[piso, precio_base], ...] donde piso va de 1 a total_pisos.
    """
    print("\n" + "=" * 45)
    print("      CONFIGURACIÓN DE TARIFAS DEL HOTEL     ")
    print("=" * 45)

    # 1. Precio base general (reutiliza validar_generico del Módulo 1)
    precio_base_valido = False
    precio_base = 0.0

    while not precio_base_valido:
        precio_base = float(validar_generico("Ingrese el precio base por noche del hotel ($): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))
        if precio_base > 0:
            precio_base_valido = True
        else:
            print("Error: El precio base debe ser mayor a 0.")

    matriz_tarifas = []

    # 2. Si el hotel tiene más de un piso, permitir segmentación de pisos lujosos
    piso_lujo_desde = total_pisos + 1  # Por defecto, sin pisos de lujo
    recargo_porcentaje = 0.0

    if total_pisos > 1:
        tiene_lujo_valido = False
        tiene_lujo = ""

        while not tiene_lujo_valido:
            tiene_lujo = input("¿Desea segmentar pisos como lujosos/suites con tarifa diferenciada? (s/n): ").strip().lower()
            if tiene_lujo in ["s", "si", "sí", "n", "no"]:
                tiene_lujo_valido = True
            else:
                print("Opción inválida. Ingrese 's' o 'n'.")

        if tiene_lujo in ["s", "si", "sí"]:
            # Reutiliza solicitar_dimension_valida de Tiara (Módulo 1)
            piso_lujo_desde = solicitar_dimension_valida(
                f"¿A partir de qué piso se consideran de lujo? (2 a {total_pisos}): ",
                2,
                total_pisos
            )

            # Reutiliza validar_generico de Tiara (Módulo 1)
            recargo_porcentaje = float(validar_generico("¿Qué porcentaje más caras serán las habitaciones de lujo? (ej: 30 o 50): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO))

    # 3. Construir la lista de tarifas para cada piso (de 1 a total_pisos)
    for p in range(1, total_pisos + 1):
        if p >= piso_lujo_desde:
            precio_piso = round(precio_base * (1 + recargo_porcentaje / 100.0), 2)
        else:
            precio_piso = round(precio_base, 2)
        matriz_tarifas.append([p, precio_piso])

    # 4. Mostrar resumen de tarifas
    print("\n--- ESQUEMA DE TARIFAS CONFIGURADO ---")
    for p, precio in matriz_tarifas:
        tipo = "Suite / Lujo" if p >= piso_lujo_desde else "Estándar"
        print(f"Piso {p} ({tipo}): ${precio:,.2f} por noche")
    print("=" * 45)
    input("\nPresione [Enter] para continuar...")
    return matriz_tarifas

def obtener_tarifa_habitacion(piso, matriz_tarifas):
    """
    Retorna el precio base por noche según el piso del hotel.
    matriz_tarifas tiene pares: [piso, precio_base] (piso 1-indexed: 1, 2, 3...)
    """
    for i in range(len(matriz_tarifas)):
        if matriz_tarifas[i][0] == piso:
            return matriz_tarifas[i][1]

    # Soporte por si se pasa piso en formato índice de matriz (0 para Piso 1)
    if piso == 0 and len(matriz_tarifas) > 0:
        return matriz_tarifas[0][1]

    # Fallback al último piso si excede el rango
    if len(matriz_tarifas) > 0:
        return matriz_tarifas[-1][1]

    return 0.0


def filtrar_huespedes_por_piso(lista_huespedes, piso_objetivo):
    """
    Uso de 'filter' y 'lambda' para aislar los huéspedes de un piso específico.
    Cumple con el requisito de funciones de orden superior y listas avanzadas.
    """
    # El índice 3 de cada sublista corresponde al piso (0-indexed, donde 0 es Piso 1)
    filtrados = list(filter(
        lambda huesped: int(huesped[3]) == int(piso_objetivo) - 1 or int(huesped[3]) == int(piso_objetivo),
        lista_huespedes
    ))
    return filtrados

# MÓDULO 3: CHECK-OUT, SWAP Y TRANSFORMACIONES MAP (Luca)

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
        piso = int(huesped[3])
        habitacion = int(huesped[4])
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

# MÓDULO 4: REPORTES Y PROGRAMACIÓN FUNCIONAL (Leandro)

def generar_reporte_ocupacion(matriz_hotel):
    """ Genera un reporte que muestra el total de habitaciones,
    las que se encuentran ocupadas y el porcentaje de ocupación del hotel.
    """

    # Total de habitaciones acumulando el largo de cada fila mediante reduce
    total_habitaciones = functools.reduce (
        lambda acumulado, fila: acumulado + len(fila),
        matriz_hotel,
        0
    )

    # Cuenta las habitaciones ocupadas en cada fila usando reduce
    ocupadas_por_fila = map(
        lambda fila: functools.reduce(
            lambda acum, hab: acum + (1 if hab == "O" else 0),
            fila,
            0
        ),
        matriz_hotel
    )

    # Acumula los subtotales de cada fila para obtener el total ocupado
    habitaciones_ocupadas = functools.reduce(
        lambda acumulado, cant: acumulado + cant,
        ocupadas_por_fila,
        0
    )

    if total_habitaciones > 0:
        porcentaje_ocupacion = habitaciones_ocupadas * 100 / total_habitaciones
    else:
        porcentaje_ocupacion = 0.0

    porcentaje_ocupacion = int(porcentaje_ocupacion * 100 + 0.5) / 100

    print("\n=== REPORTE DE OCUPACIÓN ===")
    print("Total de habitaciones: ", total_habitaciones)
    print("Habitaciones ocupadas: ", habitaciones_ocupadas)
    print("Porcentaje de ocupación: ", porcentaje_ocupacion, "%")

def calcular_subtotal(huesped, matriz_tarifas):
    """
    Calcula el subtotal a cobrar por un huésped específico y aplica un descuento del 10% si su estadía es mayor a 7 noches.
    Devuelve el subtotal para calcular la recaudación total del hotel.
    """

    dias = int(huesped[2])
    piso = int(huesped[3])
    piso_comercial = piso + 1

    precio_noche = obtener_tarifa_habitacion(piso_comercial, matriz_tarifas)
    subtotal = precio_noche * dias

    aplicar_descuento = lambda dias, subtotal: subtotal * 0.9 if dias > 7 else subtotal
    subtotal = aplicar_descuento(dias, subtotal)


    return subtotal


def calcular_recaudacion_total(lista_huespedes,matriz_tarifas):
    """
    Calcula la recaudación total del hotel sumando los subtotales de todos los huéspedes. 
    """

    #Transformación con map para convertir cada huésped en su monto subtotal
    subtotales = list(map(lambda huesped: calcular_subtotal(huesped, matriz_tarifas), lista_huespedes))

    #Acumulación con reduce de los subtotales generados
    recaudacion_total = functools.reduce(lambda acumulado, subtotal: acumulado + subtotal, subtotales, 0.0)

    print("\n=== RECAUDACIÓN TOTAL ===")
    print("Recaudación total: $", recaudacion_total)

# MÓDULO 5: RESTABLECER ESTADO DE HABITACION A "L" (Luca)

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

# PROGRAMA PRINCIPAL

def menu_principal():

    # Inicializa matriz (reiniciar_matriz() se reutiliza para redimensionar el hotel)
    hotel = reiniciar_matriz()
    
    # Matriz de tarifas dinámica: [ [Piso, Precio por noche], ... ]
    tarifas = configurar_tarifas_hotel(len(hotel))
    
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
        print("8. Restablecer habitacion")
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
            realizar_checkout(hotel, huespedes, tarifas)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            dni_busqueda = validar_generico("Ingrese el DNI a buscar: ", PATRON_DNI_VALIDO, ERROR_DNI)
            buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes, tarifas)
        elif opcion == "7":
            hotel = reiniciar_matriz()
            tarifas = configurar_tarifas_hotel(len(hotel))
            huespedes.clear()
            print("Hotel redimensionado y reiniciado con éxito")
        elif opcion == "8":
            print("\n--- RESTABLECER HABITACIÓN A LIBRE [L] ---")
            restablecer_limpieza(hotel)

        elif opcion == "0":
            print("Saliendo del sistema Room Master...")
            ejecutando = False  # Sale del bucle
        else:
            print("Opción inválida. Intente nuevamente.")

        # Muestra el resultado del menu de opciones hasta accion del usuario
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

# Ejecución
if __name__ == "__main__":
    menu_principal()
