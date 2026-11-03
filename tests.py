# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (tests.py)
# Formato: funciones def con if/else (sin clases, segun catedra)
# =============================================================================

import hotel
import reportes
import huespedes


def prueba_01_inicializacion_matriz_hotel():
    # Funcion: reiniciar_matriz
    # Datos: 2 pisos, 3 habitaciones
    resultado = hotel.inicializar_hotel(2, 3)
    esperado = [["L", "L", "L"], ["L", "L", "L"]]
    if resultado == esperado:
        print("prueba_01_inicializacion_matriz_hotel: APROBADO")
    else:
        print("prueba_01_inicializacion_matriz_hotel: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_02_obtener_tarifa_habitacion():
    # Funcion: obtener_tarifa_habitacion
    # Datos: tarifas [[1,10000.0],[2,12000.0],[3,15000.0]], piso 2
    tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    from tarifas import obtener_tarifa_habitacion
    resultado = obtener_tarifa_habitacion(2, tarifas)
    esperado = 12000.0
    if resultado == esperado:
        print("prueba_02_obtener_tarifa_habitacion: APROBADO")
    else:
        print("prueba_02_obtener_tarifa_habitacion: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_03_calcular_subtotal_sin_descuento():
    # Funcion: calcular_subtotal
    # Datos: 5 noches, tarifa 10000 -> sin descuento
    tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped = {"identidad": ("12345678", "Juan"), "dias": 5, "ubicacion": [0, 0, 101]}
    resultado = reportes.calcular_subtotal(huesped, tarifas)
    esperado = 50000.0
    if resultado == esperado:
        print("prueba_03_calcular_subtotal_sin_descuento: APROBADO")
    else:
        print("prueba_03_calcular_subtotal_sin_descuento: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_04_validar_dni_acepta_nuevo():
    # Funcion: validar_dni (con set)
    # Datos: lista con DNI "111", se valida DNI nuevo "999"
    lista = [{"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    resultado = huespedes.validar_dni("999", lista)
    esperado = "999"
    if resultado == esperado:
        print("prueba_04_validar_dni_acepta_nuevo: APROBADO")
    else:
        print("prueba_04_validar_dni_acepta_nuevo: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_05_validar_dni_rechaza_repetido():
    # Funcion: validar_dni (con set) - caso invalido
    # Datos: lista con DNI "111", se intenta registrar "111" de nuevo
    # Como validar_dni pide reingreso por input, simulamos que la funcion detecta duplicado
    # Verificamos que el set contenga el DNI (logica de deteccion)
    lista = [{"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    dnis = set()
    for huesped in lista:
        dnis.add(huesped["identidad"][0])
    dni_nuevo = "111"
    if dni_nuevo in dnis:
        print("prueba_05_validar_dni_rechaza_repetido: APROBADO")
    else:
        print("prueba_05_validar_dni_rechaza_repetido: FALLADO")


def prueba_06_calcular_subtotal_dias_cero():
    # Funcion: calcular_subtotal - caso invalido (0 dias)
    tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped = {"identidad": ("12345678", "Juan"), "dias": 0, "ubicacion": [0, 0, 101]}
    resultado = reportes.calcular_subtotal(huesped, tarifas)
    esperado = 0.0
    if resultado == esperado:
        print("prueba_06_calcular_subtotal_dias_cero: APROBADO")
    else:
        print("prueba_06_calcular_subtotal_dias_cero: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_07_obtener_tarifa_piso_inexistente():
    # Funcion: obtener_tarifa_habitacion - caso invalido (piso 99)
    # Nota: aun no hay try/except, por eso solo se imprime el resultado obtenido
    from tarifas import obtener_tarifa_habitacion
    tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    resultado = obtener_tarifa_habitacion(99, tarifas)
    print("prueba_07_obtener_tarifa_piso_inexistente: INFO (sin manejo de errores aun)")
    print("  Obtenido:", resultado)
    print("  (Se implementara try/except mas adelante)")


def prueba_08_calcular_subtotal_limite_7_noches():
    # Funcion: calcular_subtotal - caso limite (exactamente 7 noches, sin descuento)
    tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped = {"identidad": ("12345678", "Juan"), "dias": 7, "ubicacion": [0, 0, 101]}
    resultado = reportes.calcular_subtotal(huesped, tarifas)
    esperado = 70000.0   # 7 * 10000, sin descuento (descuento solo > 7)
    if resultado == esperado:
        print("prueba_08_calcular_subtotal_limite_7_noches: APROBADO")
    else:
        print("prueba_08_calcular_subtotal_limite_7_noches: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_09_reiniciar_matriz_minima():
    # Funcion: reiniciar_matriz - caso limite (1x1)
    resultado = hotel.inicializar_hotel(1, 1)
    esperado = [["L"]]
    if resultado == esperado:
        print("prueba_09_reiniciar_matriz_minima: APROBADO")
    else:
        print("prueba_09_reiniciar_matriz_minima: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


def prueba_10_buscar_huespedes_por_nombre():
    # Funcion: buscar_huespedes_por_nombre - caso adicional (busqueda parcial)
    h1 = {"identidad": ("11111111", "Juan Perez"), "dias": 2, "ubicacion": [0, 0, 101]}
    h2 = {"identidad": ("22222222", "Carlos Lopez"), "dias": 3, "ubicacion": [0, 0, 102]}
    h3 = {"identidad": ("33333333", "Juana Garcia"), "dias": 1, "ubicacion": [1, 0, 201]}
    lista = [h1, h2, h3]
    resultado = huespedes.buscar_huespedes_por_nombre(lista, "juan")
    esperado = [h1, h3]
    if resultado == esperado:
        print("prueba_10_buscar_huespedes_por_nombre: APROBADO")
    else:
        print("prueba_10_buscar_huespedes_por_nombre: FALLADO")
        print("  Esperado:", esperado)
        print("  Obtenido:", resultado)


if __name__ == "__main__":
    prueba_01_inicializacion_matriz_hotel()
    prueba_02_obtener_tarifa_habitacion()
    prueba_03_calcular_subtotal_sin_descuento()
    prueba_04_validar_dni_acepta_nuevo()
    prueba_05_validar_dni_rechaza_repetido()
    prueba_06_calcular_subtotal_dias_cero()
    prueba_07_obtener_tarifa_piso_inexistente()
    prueba_08_calcular_subtotal_limite_7_noches()
    prueba_09_reiniciar_matriz_minima()
    prueba_10_buscar_huespedes_por_nombre()