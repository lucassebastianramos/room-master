# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (test_hotel.py)
# =============================================================================
# Cátedra: Lic. Gustavo E. Escandell - Programación 1 / Algoritmos y Estructuras 1
# Responsabilidad: Verificación automatizada de funciones críticas del sistema:
# Matrices, Conversiones, Validaciones Regex, Ciclo de Vida de Huéspedes,
# Tarifas y Descuentos, Tuplas Inmutables, Conjuntos (set) y Persistencia JSON.
# Ejecución: python -m unittest test_hotel.py -v
# =============================================================================

import unittest
import re
import os

import hotel
import validaciones
import tarifas
import reportes
import huespedes
import persistencia


class TestRoomMaster(unittest.TestCase):
    """
    Suite oficial de pruebas unitarias automatizadas para Room Master.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        """
        self.pisos = 3
        self.habitaciones_por_piso = 4
        self.matriz = hotel.inicializar_hotel(self.pisos, self.habitaciones_por_piso)
        self.tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
        self.lista_huespedes = []
        self.ruta_test_json = os.path.join("datos", "test_hotel_data.json")

    def tearDown(self):
        """
        Limpia archivos temporales de prueba si se crearon.
        """
        if os.path.exists(self.ruta_test_json):
            try:
                os.remove(self.ruta_test_json)
            except OSError:
                pass

    def test_01_inicializacion_matriz_hotel(self):
        """
        Verifica que la matriz se inicialice con las dimensiones exactas
        y que todas las habitaciones inicien en estado 'L' (Libre).
        """
        self.assertEqual(len(self.matriz), 3, "La cantidad de pisos debe ser 3.")
        self.assertEqual(len(self.matriz[0]), 4, "La cantidad de habitaciones por piso debe ser 4.")
        for fila in self.matriz:
            for hab in fila:
                self.assertEqual(hab, "L", "Toda habitación nueva debe estar Libre [L].")

    def test_02_conversion_coordenadas_comerciales(self):
        """
        Verifica la biyección matemática entre índices de matriz (0, 0)
        y números comerciales de habitación (101, 204, 302).
        Retorna Tuplas inmutables.
        """
        self.assertEqual(hotel.obtener_numero_comercial(0, 0), 101)
        self.assertEqual(hotel.obtener_numero_comercial(1, 3), 204)
        self.assertEqual(hotel.obtener_numero_comercial(2, 1), 302)

        indices = hotel.obtener_indices_matriz(101)
        self.assertIsInstance(indices, tuple, "Las coordenadas de matriz deben ser una tupla.")
        self.assertEqual(indices, (0, 0))

        indices_304 = hotel.obtener_indices_matriz(304)
        self.assertEqual(indices_304, (2, 3))

    def test_03_validaciones_expresiones_regulares(self):
        """
        Verifica las expresiones regulares de integridad de datos (Regex):
        DNI numérico de 7 a 8 dígitos, textos sin números y números enteros positivos.
        """
        # Validación de DNI
        self.assertTrue(re.match(validaciones.PATRON_DNI_VALIDO, "12345678"))
        self.assertTrue(re.match(validaciones.PATRON_DNI_VALIDO, "1234567"))
        self.assertFalse(re.match(validaciones.PATRON_DNI_VALIDO, "123456"))      # Corto
        self.assertFalse(re.match(validaciones.PATRON_DNI_VALIDO, "123456789"))   # Largo
        self.assertFalse(re.match(validaciones.PATRON_DNI_VALIDO, "1234abcd"))    # Alfanumérico

        # Validación de texto
        self.assertTrue(re.match(validaciones.PATRON_TEXTO_VALIDO, "Lucas Ramos"))
        self.assertTrue(re.match(validaciones.PATRON_TEXTO_VALIDO, "Tiara Menéndez"))
        self.assertFalse(re.match(validaciones.PATRON_TEXTO_VALIDO, "User123"))

    def test_04_estructuras_datos_tuplas_y_conjuntos(self):
        """
        Verifica el uso explícito de Tuplas para datos inmutables y Conjuntos (set)
        para búsquedas rápidas y validación de unicidad:
        - Tupla inmutable ESTADOS_VALIDOS
        - Conjuntos (set) de habitaciones por estado (L, O, S, M)
        - Conjunto (set) de DNIs activos para búsqueda O(1)
        """
        # Tupla inmutable de estados
        self.assertIsInstance(hotel.ESTADOS_VALIDOS, tuple)
        self.assertEqual(hotel.ESTADOS_VALIDOS, ("L", "O", "S", "M"))

        # Conjunto de habitaciones libres
        libres = hotel.obtener_habitaciones_por_estado(self.matriz, "L")
        self.assertIsInstance(libres, set)
        self.assertEqual(len(libres), 12)
        self.assertIn(101, libres)

        # Registro con tuplas inmutables
        identidad = ("44123456", "Juan Perez")
        config_hab = (0, 0, 101)
        huesped = [identidad, config_hab, 3, 0.0]
        self.lista_huespedes.append(huesped)

        # Validación con conjunto de DNIs
        conjunto_dnis = huespedes.obtener_conjunto_dnis(self.lista_huespedes)
        self.assertIsInstance(conjunto_dnis, set)
        self.assertIn("44123456", conjunto_dnis)
        self.assertNotIn("99999999", conjunto_dnis)

    def test_05_ciclo_mantenimiento_habitaciones(self):
        """
        Verifica que una habitación pueda colocarse en estado Mantenimiento [M]
        y que quede inhabilitada para reservas hasta ser reparada a [L].
        """
        self.matriz[0][1] = "M"
        self.assertEqual(self.matriz[0][1], "M")

        # Verificar que aparezca en el conjunto de mantenimiento
        en_mant = hotel.obtener_habitaciones_por_estado(self.matriz, "M")
        self.assertIn(102, en_mant)

        # Dar el alta técnica
        self.matriz[0][1] = "L"
        self.assertEqual(self.matriz[0][1], "L")
        libres = hotel.obtener_habitaciones_por_estado(self.matriz, "L")
        self.assertIn(102, libres)

    def test_06_calculo_subtotal_con_descuento_larga_estadia(self):
        """
        Verifica el cálculo de liquidación mediante orden superior (lambda):
        - Estadía <= 7 noches: tarifa plena.
        - Estadía > 7 noches: 10% de bonificación automática.
        Soporta la estructura de tuplas inmutables.
        """
        # Huésped 1: 5 noches en piso 1 ($10,000/noche) = $50,000
        huesped_corto = [("12345678", "Juan Perez"), (0, 0, 101), 5, 0.0]
        subtotal_corto = reportes.calcular_subtotal(huesped_corto, self.tarifas)
        self.assertEqual(subtotal_corto, 50000.0)

        # Huésped 2: 10 noches en piso 1 ($10,000/noche) = $100,000 - 10% = $90,000
        huesped_largo = [("87654321", "Maria Gomez"), (0, 1, 102), 10, 0.0]
        subtotal_largo = reportes.calcular_subtotal(huesped_largo, self.tarifas)
        self.assertEqual(subtotal_largo, 90000.0)

    def test_07_consumos_adicionales_y_liquidacion_con_extras(self):
        """
        Verifica la acumulación de consumos extras (Minibar, Cochera)
        y su correcto impacto en la facturación del huésped.
        """
        # Huésped con 3 noches en piso 2 ($12,000/noche = $36,000) + $4,500 en extras
        huesped_extras = [("20111222", "Carlos Tevez"), (1, 0, 201), 3, 4500.0]
        subtotal_con_extras = reportes.calcular_subtotal(huesped_extras, self.tarifas)
        self.assertEqual(subtotal_con_extras, 40500.0)

    def test_08_recaudacion_total_programacion_funcional(self):
        """
        Verifica el uso de map y reduce para calcular la recaudación total proyectada.
        """
        h1 = [("11111111", "Huesped 1"), (0, 0, 101), 2, 0.0]    # 2 x 10,000 = 20,000
        h2 = [("22222222", "Huesped 2"), (1, 0, 201), 2, 1000.0]  # 2 x 12,000 + 1,000 = 25,000
        lista = [h1, h2]

        total = reportes.calcular_recaudacion_total(lista, self.tarifas)
        self.assertEqual(total, 45000.0)

    def test_09_anti_bucle_infinito_hotel_completo(self):
        """
        Verifica que la función detectora de disponibilidad prevenga bucles infinitos
        cuando todas las habitaciones están en estado 'O', 'S' o 'M'.
        """
        # Hotel con habitaciones libres
        self.assertTrue(hotel.hay_habitaciones_disponibles(self.matriz))

        # Llenar todas las habitaciones
        for f in range(len(self.matriz)):
            for c in range(len(self.matriz[0])):
                self.matriz[f][c] = "O"

        self.assertFalse(hotel.hay_habitaciones_disponibles(self.matriz))

    def test_10_persistencia_datos_json(self):
        """
        Verifica la persistencia de datos en formato JSON mediante persistencia.py:
        - Guardar estado de hotel, huéspedes y tarifas.
        - Cargar estado y verificar restauración de tuplas inmutables.
        - Manejo seguro de excepciones sin caídas.
        """
        self.matriz[0][0] = "O"
        huesped_original = [("30123456", "Ana Diaz"), (0, 0, 101), 4, 1500.0]
        self.lista_huespedes.append(huesped_original)

        # Guardar en archivo JSON de prueba
        exito_guardar = persistencia.guardar_datos_json(
            self.matriz,
            self.lista_huespedes,
            self.tarifas,
            ruta=self.ruta_test_json
        )
        self.assertTrue(exito_guardar, "El guardado en JSON debe ser exitoso.")
        self.assertTrue(os.path.exists(self.ruta_test_json))

        # Cargar desde archivo JSON
        datos_recuperados = persistencia.cargar_datos_json(ruta=self.ruta_test_json)
        self.assertIsNotNone(datos_recuperados)
        self.assertEqual(datos_recuperados["hotel"][0][0], "O")
        self.assertEqual(len(datos_recuperados["huespedes"]), 1)

        # Verificar que las tuplas se reconstruyeron inmutables
        recuperado = datos_recuperados["huespedes"][0]
        self.assertIsInstance(recuperado[0], tuple, "La identidad debe ser una tupla inmutable.")
        self.assertIsInstance(recuperado[1], tuple, "La configuración de hab debe ser una tupla inmutable.")
        self.assertEqual(recuperado[0], ("30123456", "Ana Diaz"))
        self.assertEqual(recuperado[1], (0, 0, 101))
        self.assertEqual(recuperado[2], 4)
        self.assertEqual(recuperado[3], 1500.0)


if __name__ == "__main__":
    unittest.main()

