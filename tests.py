# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (tests.py)
# =============================================================================
# Implementación con doctest (sin clases, conforme a lineamientos de la cátedra)
# Cátedra: Lic. Gustavo E. Escandell
# =============================================================================

import doctest
import hotel
import tarifas
import reportes
import huespedes


def prueba_01_inicializacion_matriz_hotel():
    """
    Prueba 1: Inicialización de la matriz del hotel.
    Verifica que la matriz se cree con las dimensiones correctas y estado Libre ('L').

    >>> matriz = hotel.inicializar_hotel(2, 3)
    >>> matriz
    [['L', 'L', 'L'], ['L', 'L', 'L']]
    >>> hotel.inicializar_hotel(1, 1)
    [['L']]
    """
    matriz = hotel.inicializar_hotel(2, 3)
    assert matriz == [['L', 'L', 'L'], ['L', 'L', 'L']]


def prueba_02_conversion_coordenadas_comerciales():
    """
    Prueba 2: Conversión bidireccional entre índices de matriz y números comerciales.

    >>> hotel.obtener_numero_comercial(0, 0)
    101
    >>> hotel.obtener_indices_matriz(101)
    (0, 0)
    >>> hotel.obtener_numero_comercial(2, 4)
    305
    >>> hotel.obtener_indices_matriz(305)
    (2, 4)
    """
    assert hotel.obtener_numero_comercial(0, 0) == 101
    assert hotel.obtener_indices_matriz(101) == (0, 0)


def prueba_03_obtener_tarifa_habitacion():
    """
    Prueba 3: Obtención de tarifas por piso.

    >>> tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    >>> tarifas.obtener_tarifa_habitacion(2, tarifas_hotel)
    12000.0
    >>> tarifas.obtener_tarifa_habitacion(1, tarifas_hotel)
    10000.0
    >>> tarifas.obtener_tarifa_habitacion(99, tarifas_hotel)
    15000.0
    """
    tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    assert tarifas.obtener_tarifa_habitacion(2, tarifas_hotel) == 12000.0


def prueba_04_calcular_subtotal_sin_descuento():
    """
    Prueba 4: Cálculo de subtotal para estadías cortas (<= 7 noches, tarifa plena).
    5 noches a $10,000 = $50,000.0.

    >>> tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    >>> huesped = {"identidad": ("12345678", "Juan"), "dias": 5, "ubicacion": [0, 0, 101]}
    >>> reportes.calcular_subtotal(huesped, tarifas_hotel)
    50000.0
    """
    tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped = {"identidad": ("12345678", "Juan"), "dias": 5, "ubicacion": [0, 0, 101]}
    assert reportes.calcular_subtotal(huesped, tarifas_hotel) == 50000.0


def prueba_05_calcular_subtotal_con_descuento_larga_estadia():
    """
    Prueba 5: Bonificación del 10% con expresión lambda para estadías largas (> 7 noches).
    10 noches a $10,000 = $100,000 * 0.9 = $90,000.0.

    >>> tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    >>> huesped = {"identidad": ("12345678", "Juan"), "dias": 10, "ubicacion": [0, 0, 101]}
    >>> reportes.calcular_subtotal(huesped, tarifas_hotel)
    90000.0
    """
    tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped = {"identidad": ("12345678", "Juan"), "dias": 10, "ubicacion": [0, 0, 101]}
    assert reportes.calcular_subtotal(huesped, tarifas_hotel) == 90000.0


def prueba_06_calcular_subtotal_casos_limites():
    """
    Prueba 6: Casos límite de cálculo de subtotal.
    - Exactamente 7 noches: no recibe descuento (7 * 10000 = 70000.0).
    - 0 días de estadía: total 0.0.

    >>> tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    >>> huesped_7 = {"identidad": ("12345678", "Juan"), "dias": 7, "ubicacion": [0, 0, 101]}
    >>> reportes.calcular_subtotal(huesped_7, tarifas_hotel)
    70000.0
    >>> huesped_0 = {"identidad": ("12345678", "Juan"), "dias": 0, "ubicacion": [0, 0, 101]}
    >>> reportes.calcular_subtotal(huesped_0, tarifas_hotel)
    0.0
    """
    tarifas_hotel = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    huesped_7 = {"identidad": ("12345678", "Juan"), "dias": 7, "ubicacion": [0, 0, 101]}
    assert reportes.calcular_subtotal(huesped_7, tarifas_hotel) == 70000.0


def prueba_07_validar_dni_con_conjunto_set():
    """
    Prueba 7: Validación de DNI con conjunto (set).
    Verifica que acepte un DNI nuevo y detecte uno repetido en tiempo O(1).

    >>> lista = [{"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    >>> huespedes.validar_dni("999", lista)
    '999'
    >>> huespedes.dni_ya_registrado("111", lista)
    True
    >>> huespedes.dni_ya_registrado("999", lista)
    False
    """
    lista = [{"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    assert huespedes.validar_dni("999", lista) == "999"
    assert huespedes.dni_ya_registrado("111", lista) is True
    assert huespedes.dni_ya_registrado("999", lista) is False


def prueba_08_recaudacion_total_programacion_funcional():
    """
    Prueba 8: Recaudación total mediante programación funcional (map y functools.reduce).

    >>> tarifas_hotel = [[1, 10000.0], [2, 12000.0]]
    >>> h1 = {"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}
    >>> h2 = {"identidad": ("222", "Bob"), "dias": 3, "ubicacion": [1, 0, 201]}
    >>> total = reportes.calcular_recaudacion_total([h1, h2], tarifas_hotel)
    <BLANKLINE>
    === RECAUDACIÓN TOTAL ===
    Recaudación total proyectada: $56,000.00
    >>> total
    56000.0
    """
    tarifas_hotel = [[1, 10000.0], [2, 12000.0]]
    h1 = {"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}
    h2 = {"identidad": ("222", "Bob"), "dias": 3, "ubicacion": [1, 0, 201]}
    assert reportes.calcular_recaudacion_total([h1, h2], tarifas_hotel) == 56000.0


def prueba_09_buscar_huespedes_por_nombre_filter_lambda():
    """
    Prueba 9: Búsqueda funcional parcial por nombre mediante filter y función lambda.

    >>> h1 = {"identidad": ("11111111", "Juan Perez"), "dias": 2, "ubicacion": [0, 0, 101]}
    >>> h2 = {"identidad": ("22222222", "Carlos Lopez"), "dias": 3, "ubicacion": [0, 0, 102]}
    >>> h3 = {"identidad": ("33333333", "Juana Garcia"), "dias": 1, "ubicacion": [1, 0, 201]}
    >>> resultados = huespedes.buscar_huespedes_por_nombre([h1, h2, h3], "juan")
    >>> [h["identidad"][1] for h in resultados]
    ['Juan Perez', 'Juana Garcia']
    """
    h1 = {"identidad": ("11111111", "Juan Perez"), "dias": 2, "ubicacion": [0, 0, 101]}
    h2 = {"identidad": ("22222222", "Carlos Lopez"), "dias": 3, "ubicacion": [0, 0, 102]}
    h3 = {"identidad": ("33333333", "Juana Garcia"), "dias": 1, "ubicacion": [1, 0, 201]}
    resultados = huespedes.buscar_huespedes_por_nombre([h1, h2, h3], "juan")
    assert len(resultados) == 2


def prueba_10_mover_huesped_swap():
    """
    Prueba 10: Reubicación de huésped (Swap).
    Verifica que la habitación previa quede libre ('L'), la nueva ocupada ('O') y se actualicen sus coordenadas.

    >>> matriz = [['O', 'L'], ['L', 'L']]
    >>> huesped = {"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}
    >>> huespedes.mover_huesped(matriz, huesped, (0, 1, 102))
    >>> matriz[0][0]
    'L'
    >>> matriz[0][1]
    'O'
    >>> huesped["ubicacion"]
    [0, 1, 102]
    """
    matriz = [['O', 'L'], ['L', 'L']]
    huesped = {"identidad": ("111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}
    huespedes.mover_huesped(matriz, huesped, (0, 1, 102))
    assert matriz[0][0] == 'L'
    assert matriz[0][1] == 'O'
    assert huesped["ubicacion"] == [0, 1, 102]


if __name__ == "__main__":
    print("=" * 70)
    print("SUITE DE PRUEBAS UNITARIAS CON DOCTEST (SIN CLASES)")
    print("Materia: Algoritmos y Estructura de Datos 1 / Programación 1")
    print("Docente: Lic. Gustavo E. Escandell")
    print("=" * 70)

    # 1. Ejecutar las pruebas formales de tests.py
    print("\n--- EJECUTANDO CASOS DE PRUEBA FORMALES (tests.py) ---")
    fallos_suite, total_suite = doctest.testmod(verbose=True)

    # 2. Ejecutar las pruebas en los módulos del proyecto
    print("\n--- RESUMEN DE PRUEBAS EN MÓDULOS DEL PROYECTO ---")
    modulos = [hotel, tarifas, reportes, huespedes]
    total_fallos = fallos_suite
    total_pruebas = total_suite

    for mod in modulos:
        f, t = doctest.testmod(mod, verbose=False)
        print(f"Módulo {mod.__name__:<15}: {t:>2} pruebas ejecutadas | {t - f:>2} aprobadas | {f:>2} falladas")
        total_fallos += f
        total_pruebas += t

    print("\n" + "=" * 70)
    if total_fallos == 0:
        print(f"RESULTADO FINAL: TODAS LAS PRUEBAS APROBADAS ({total_pruebas} pruebas sin clases)")
    else:
        print(f"RESULTADO FINAL: {total_fallos} PRUEBAS FALLADAS de {total_pruebas}")
    print("=" * 70)
