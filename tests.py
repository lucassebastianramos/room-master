# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (tests.py)
# =============================================================================
# Materia: Algoritmo y Estructura de Datos 1 / Programación 1 (UADE)
# Docente: Lic. Gustavo E. Escandell
# Requisitos: Mínimo 10 pruebas sobre al menos 5 funciones.
# Distribución obligatoria:
#   - 4 Casos Válidos
#   - 3 Casos Inválidos
#   - 2 Casos Límite
#   - 1 Caso Adicional
# Restricción estricta: NO UTILIZAR CLASES (Programación modular y estructurada).
# Formato de cada prueba:
#   1. Función que se prueba
#   2. Datos utilizados
#   3. Resultado esperado
#   4. Resultado obtenido
#   5. Veredicto (Aprobado o Fallado)
# =============================================================================

import hotel
import tarifas
import reportes
import huespedes


def reportar_prueba(num, categoria, funcion_nombre, datos_str, esperado, obtenido):
    """
    Función auxiliar para formatear la salida de cada prueba unitaria
    cumpliendo estrictamente con los 5 puntos exigidos en la Sección 9 del TP.
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

    return aprobado


# =============================================================================
# BLOQUE 1: CASOS VÁLIDOS (4 pruebas)
# =============================================================================

def prueba_01_inicializacion_matriz_valida():
    """Caso válido: Crea la matriz del hotel con pisos y habitaciones válidas."""
    datos = "pisos = 2, habitaciones = 3"
    esperado = [["L", "L", "L"], ["L", "L", "L"]]
    obtenido = hotel.inicializar_hotel(2, 3)
    return reportar_prueba(1, "Caso Válido", "hotel.inicializar_hotel", datos, esperado, obtenido)


def prueba_02_obtener_tarifa_piso_existente():
    """Caso válido: Consulta la tarifa de un piso configurado en la matriz."""
    esquema_tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
    datos = "piso = 2, tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]"
    esperado = 12000.0
    obtenido = tarifas.obtener_tarifa_habitacion(2, esquema_tarifas)
    return reportar_prueba(2, "Caso Válido", "tarifas.obtener_tarifa_habitacion", datos, esperado, obtenido)


def prueba_03_calcular_subtotal_estadia_corta():
    """Caso válido: Estadía de 5 noches (<= 7) sin aplicar bonificación."""
    esquema_tarifas = [[1, 10000.0], [2, 12000.0]]
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 5, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 5, 'piso': 0 (Piso 1)}, tarifa=$10000.0"
    esperado = 50000.0  # 5 * 10000.0
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)
    return reportar_prueba(3, "Caso Válido", "reportes.calcular_subtotal", datos, esperado, obtenido)


def prueba_04_calcular_subtotal_estadia_larga_con_descuento():
    """Caso válido: Estadía de 10 noches (> 7) con 10% de descuento vía lambda."""
    esquema_tarifas = [[1, 10000.0], [2, 12000.0]]
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 10, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 10, 'piso': 0 (Piso 1)}, tarifa=$10000.0 (10% desc. > 7 días)"
    esperado = 90000.0  # 10 * 10000.0 * 0.90
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)
    return reportar_prueba(4, "Caso Válido", "reportes.calcular_subtotal", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 2: CASOS INVÁLIDOS (3 pruebas)
# =============================================================================

def prueba_05_deteccion_dni_duplicado_con_conjunto():
    """Caso inválido: Detecta que un DNI ya existe usando un conjunto (set)."""
    huespedes_registrados = [{"identidad": ("11111111", "Ana Gomez"), "dias": 2, "ubicacion": [0, 0, 101]}]
    dnis_set = set()
    for h in huespedes_registrados:
        dnis_set.add(h["identidad"][0])

    dni_ingresado_duplicado = "11111111"
    datos = "dni_nuevo = '11111111', dnis_registrados = {'11111111'}"
    esperado = True  # El conjunto detecta pertenencia O(1) de DNI repetido
    obtenido = (dni_ingresado_duplicado in dnis_set)
    return reportar_prueba(5, "Caso Inválido", "deteccion_dni_duplicado_set", datos, esperado, obtenido)


def prueba_06_habitacion_inexistente_fuera_de_rango():
    """Caso inválido: Consulta de habitación en un piso que no existe en la matriz."""
    matriz_hotel = [["L", "L"], ["L", "L"]]  # 2 pisos, 2 habitaciones
    datos = "matriz de 2x2, piso = 5, habitacion = 0"
    esperado = False  # La habitación no existe
    obtenido = hotel.habitacion_existe(matriz_hotel, 5, 0)
    return reportar_prueba(6, "Caso Inválido", "hotel.habitacion_existe", datos, esperado, obtenido)


def prueba_07_busqueda_huesped_habitacion_vacia():
    """Caso inválido: Buscar huésped en una habitación donde no hay nadie alojado."""
    lista_huespedes = [{"identidad": ("11111111", "Ana"), "dias": 2, "ubicacion": [0, 0, 101]}]
    datos = "lista_huespedes=[Hab 101], numero_habitacion_buscada = 999"
    esperado = []  # Lista vacía retornada por filter/lambda
    obtenido = huespedes.buscar_huesped_por_habitacion(lista_huespedes, 999)
    return reportar_prueba(7, "Caso Inválido", "huespedes.buscar_huesped_por_habitacion", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 3: CASOS LÍMITE (2 pruebas)
# =============================================================================

def prueba_08_calcular_subtotal_limite_exacto_7_noches():
    """Caso límite: Exactamente 7 noches de estadía (sin descuento, descuento es > 7)."""
    esquema_tarifas = [[1, 10000.0], [2, 12000.0]]
    huesped = {"identidad": ("12345678", "Juan Perez"), "dias": 7, "ubicacion": [0, 0, 101]}
    datos = "huesped={'dias': 7, 'piso': 0 (Piso 1)}, tarifa=$10000.0 (frontera sin desc)"
    esperado = 70000.0  # 7 * 10000.0
    obtenido = reportes.calcular_subtotal(huesped, esquema_tarifas)
    return reportar_prueba(8, "Caso Límite", "reportes.calcular_subtotal", datos, esperado, obtenido)


def prueba_09_inicializacion_matriz_dimension_minima():
    """Caso límite: Inicialización con dimensión mínima permitida (hotel 1x1)."""
    datos = "pisos = 1, habitaciones = 1"
    esperado = [["L"]]
    obtenido = hotel.inicializar_hotel(1, 1)
    return reportar_prueba(9, "Caso Límite", "hotel.inicializar_hotel", datos, esperado, obtenido)


# =============================================================================
# BLOQUE 4: CASO ADICIONAL RELEVANTE (1 prueba)
# =============================================================================

def prueba_10_busqueda_parcial_nombre_filter_lambda():
    """Caso adicional: Búsqueda funcional parcial por nombre con filter y lambda."""
    h1 = {"identidad": ("11111111", "Juan Perez"), "dias": 2, "ubicacion": [0, 0, 101]}
    h2 = {"identidad": ("22222222", "Carlos Lopez"), "dias": 3, "ubicacion": [0, 0, 102]}
    h3 = {"identidad": ("33333333", "Juana Garcia"), "dias": 1, "ubicacion": [1, 0, 201]}
    lista = [h1, h2, h3]
    termino_busqueda = "juan"
    datos = "lista de 3 huéspedes, texto_busqueda = 'juan'"
    esperado = [h1, h3]  # Debe encontrar a 'Juan Perez' y 'Juana Garcia'
    obtenido = huespedes.buscar_huespedes_por_nombre(lista, termino_busqueda)
    return reportar_prueba(10, "Caso Adicional", "huespedes.buscar_huespedes_por_nombre", datos, esperado, obtenido)


# =============================================================================
# EJECUCIÓN PRINCIPAL DE LA SUITE
# =============================================================================

def ejecutar_suite():
    print("=" * 65)
    print("      SUITE DE PRUEBAS UNITARIAS - SISTEMA ROOM MASTER")
    print("      Cátedra: Lic. Gustavo E. Escandell (UADE 2026)")
    print("      Restricción: Sin clases | Mínimo 10 pruebas")
    print("=" * 65)
    print()

    pruebas = [
        prueba_01_inicializacion_matriz_valida,
        prueba_02_obtener_tarifa_piso_existente,
        prueba_03_calcular_subtotal_estadia_corta,
        prueba_04_calcular_subtotal_estadia_larga_con_descuento,
        prueba_05_deteccion_dni_duplicado_con_conjunto,
        prueba_06_habitacion_inexistente_fuera_de_rango,
        prueba_07_busqueda_huesped_habitacion_vacia,
        prueba_08_calcular_subtotal_limite_exacto_7_noches,
        prueba_09_inicializacion_matriz_dimension_minima,
        prueba_10_busqueda_parcial_nombre_filter_lambda
    ]

    total = len(pruebas)
    aprobadas = 0

    for prueba in pruebas:
        if prueba():
            aprobadas += 1

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
