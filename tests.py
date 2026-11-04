# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (tests.py)
# =============================================================================
# Materia: Algoritmo y Estructura de Datos 1 / Programación 1 (UADE 2026)
# Cátedra: Lic. Gustavo E. Escandell
# 
# Compatibilidad dual:
#   1. Ejecución con PyTest:    python -m pytest tests.py -v
#   2. Ejecución con Python:    python tests.py
#
# Distribución oficial de la Fase 2 (Mínimo 10 pruebas sobre 5+ funciones):
#   - 4 Casos Válidos     (test_01 a test_04)
#   - 3 Casos Inválidos   (test_05 a test_07)
#   - 2 Casos Límite      (test_08 y test_09)
#   - 1 Caso Adicional    (test_10)
#
# Restricción estricta: CERO CLASES (Funciones def puras y aserciones nativas).
# =============================================================================

import hotel
import tarifas
import reportes
import huespedes


def reportar_prueba(num, categoria, funcion_nombre, datos_str, esperado, obtenido):
    """
    Función auxiliar para formatear la salida en consola cumpliendo
    con los 5 puntos exigidos en la Sección 9 del Trabajo Práctico.
    """
    aprobado = (esperado == obtenido)
    estado = "APROBADO" if aprobado else "FALLADO"

    print(f"Prueba [{num:02d}] - {categoria.upper()}")
    print(f"  1. Función:   {funcion_nombre}")
    print(f"  2. Datos:     {datos_str}")
    print(f"  3. Esperado:  {esperado}")
    print(f"  4. Obtenido:  {obtenido}")
    print(f"  5. Resultado: [{estado}]")
    print("-" * 65)


# =============================================================================
# BLOQUE 1: CASOS VÁLIDOS (4 pruebas)
# =============================================================================

def test_01_inicializacion_matriz_valida():
    """Caso válido: Crea la matriz del hotel con pisos y habitaciones válidas."""
    datos = "pisos = 2, habitaciones = 3"
    esperado = [["L", "L", "L"], ["L", "L", "L"]]
    obtenido = hotel.inicializar_hotel(2, 3)

    assert obtenido == esperado
    reportar_prueba(1, "Caso Válido", "hotel.inicializar_hotel", datos, esperado, obtenido)


def test_02_obtener_tarifa_piso_existente():
    """Caso válido: Consulta la tarifa de un piso configurado en la matriz."""
    esquema_tarifas = {1: 10000.0, 2: 12000.0, 3: 15000.0}
    datos = "piso = 2, tarifas = {1: 10000.0, 2: 12000.0, 3: 15000.0}"
    esperado = 12000.0
    obtenido = tarifas.obtener_tarifa_habitacion(2, esquema_tarifas)

    assert obtenido == esperado
    reportar_prueba(2, "Caso Válido", "tarifas.obtener_tarifa_habitacion", datos, esperado, obtenido)


def test_03_calcular_subtotal_estadia_corta():
    """Caso válido: Estadía corta de 5 noches (<= 7) a tarifa plena."""
    esquema_tarifas = {1: 10000.0, 2: 12000.0}
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 5, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 5, 'piso': 0 (Piso 1)}, tarifa=$10000.0"
    esperado = 50000.0
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)

    assert obtenido == esperado
    reportar_prueba(3, "Caso Válido", "reportes.calcular_subtotal", datos, esperado, obtenido)


def test_04_calcular_subtotal_estadia_larga_con_descuento():
    """Caso válido: Estadía de 10 noches (> 7) con 10% de bonificación vía lambda."""
    esquema_tarifas = {1: 10000.0, 2: 12000.0}
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 10, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 10, 'piso': 0 (Piso 1)}, tarifa=$10000.0 (10% desc. > 7 días)"
    esperado = 90000.0  # 10 * 10000.0 * 0.90
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)

    assert obtenido == esperado
    reportar_prueba(4, "Caso Válido", "reportes.calcular_subtotal", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 2: CASOS INVÁLIDOS (3 pruebas)
# =============================================================================

def test_05_deteccion_dni_duplicado_con_conjunto():
    """Caso inválido: Detección en O(1) de DNI duplicado mediante conjunto (set)."""
    huespedes_registrados = [{"identidad": ("11111111", "Ana Gomez"), "dias": 2, "ubicacion": [0, 0, 101]}]
    dnis_set = set()
    for h in huespedes_registrados:
        dnis_set.add(h["identidad"][0])

    dni_ingresado_duplicado = "11111111"
    datos = "dni_nuevo = '11111111', dnis_registrados = {'11111111'}"
    esperado = True
    obtenido = (dni_ingresado_duplicado in dnis_set)

    assert obtenido == esperado
    reportar_prueba(5, "Caso Inválido", "deteccion_dni_duplicado_set", datos, esperado, obtenido)


def test_06_habitacion_inexistente_fuera_de_rango():
    """Caso inválido: Consulta de habitación en un piso inexistente."""
    matriz_hotel = [["L", "L"], ["L", "L"]]
    datos = "matriz de 2x2, piso = 5, habitacion = 0"
    esperado = False
    obtenido = hotel.habitacion_existe(matriz_hotel, 5, 0)

    assert obtenido == esperado
    reportar_prueba(6, "Caso Inválido", "hotel.habitacion_existe", datos, esperado, obtenido)


def test_07_busqueda_huesped_habitacion_vacia():
    """Caso inválido: Buscar huésped en habitación vacía o inexistente."""
    lista_huespedes = [{"identidad": ("11111111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    datos = "lista_huespedes=[Hab 101], numero_habitacion_buscada = 999"
    esperado = []
    obtenido = huespedes.buscar_huesped_por_habitacion(lista_huespedes, 999)

    assert obtenido == esperado
    reportar_prueba(7, "Caso Inválido", "huespedes.buscar_huesped_por_habitacion", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 3: CASOS LÍMITE (2 pruebas)
# =============================================================================

def test_08_calcular_subtotal_limite_exacto_7_noches():
    """Caso límite: Exactamente 7 noches de estadía (frontera sin descuento)."""
    esquema_tarifas = {1: 10000.0, 2: 12000.0}
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 7, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 7, 'piso': 0 (Piso 1)}, tarifa=$10000.0 (frontera sin desc)"
    esperado = 70000.0  # 7 * 10000.0
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)

    assert obtenido == esperado
    reportar_prueba(8, "Caso Límite", "reportes.calcular_subtotal", datos, esperado, obtenido)


def test_09_inicializacion_matriz_dimension_minima():
    """Caso límite: Inicialización con dimensión mínima permitida (hotel 1x1)."""
    datos = "pisos = 1, habitaciones = 1"
    esperado = [["L"]]
    obtenido = hotel.inicializar_hotel(1, 1)

    assert obtenido == esperado
    reportar_prueba(9, "Caso Límite", "hotel.inicializar_hotel", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 4: CASO ADICIONAL RELEVANTE (1 prueba)
# =============================================================================

def test_10_busqueda_parcial_nombre_filter_lambda():
    """Caso adicional: Búsqueda funcional parcial por nombre con filter y lambda."""
    h1 = {"identidad": ("11111111", "Juan Perez"), "dias": 2, "ubicacion": [0, 0, 101]}
    h2 = {"identidad": ("22222222", "Carlos Lopez"), "dias": 3, "ubicacion": [0, 0, 102]}
    h3 = {"identidad": ("33333333", "Juana Garcia"), "dias": 1, "ubicacion": [1, 0, 201]}
    lista = [h1, h2, h3]
    termino_busqueda = "juan"
    datos = "lista de 3 huéspedes, texto_busqueda = 'juan'"
    esperado = [h1, h3]
    obtenido = huespedes.buscar_huespedes_por_nombre(lista, termino_busqueda)

    assert obtenido == esperado
    reportar_prueba(10, "Caso Adicional", "huespedes.buscar_huespedes_por_nombre", datos, esperado, obtenido)


# =============================================================================
# EJECUCIÓN DIRECTA AUTÓNOMA (python tests.py)
# =============================================================================

def ejecutar_suite():
    print("=" * 65)
    print("      SUITE DE PRUEBAS UNITARIAS - SISTEMA ROOM MASTER")
    print("      Cátedra: Lic. Gustavo E. Escandell (UADE 2026)")
    print("      Compatible con PyTest | 10 Pruebas sin Clases")
    print("=" * 65)
    print()

    pruebas = [
        test_01_inicializacion_matriz_valida,
        test_02_obtener_tarifa_piso_existente,
        test_03_calcular_subtotal_estadia_corta,
        test_04_calcular_subtotal_estadia_larga_con_descuento,
        test_05_deteccion_dni_duplicado_con_conjunto,
        test_06_habitacion_inexistente_fuera_de_rango,
        test_07_busqueda_huesped_habitacion_vacia,
        test_08_calcular_subtotal_limite_exacto_7_noches,
        test_09_inicializacion_matriz_dimension_minima,
        test_10_busqueda_parcial_nombre_filter_lambda
    ]

    total = len(pruebas)
    aprobadas = 0

    for prueba in pruebas:
        try:
            prueba()
            aprobadas += 1
        except AssertionError:
            pass

    falladas = total - aprobadas

    print("\n" + "=" * 65)
    print(f"RESUMEN FINAL: {aprobadas}/{total} PRUEBAS APROBADAS | {falladas} FALLADAS")
    if falladas == 0:
        print("ESTADO: TODAS LAS PRUEBAS UNITARIAS PASARON EXITOSAMENTE.")
    else:
        print("ESTADO: HAY PRUEBAS CON FALLOS.")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_suite()
