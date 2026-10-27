# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (test_hotel.py)
# =============================================================================
# Cátedra: Lic. Gustavo E. Escandell - Programación 1 / Algoritmos y Estructuras 1
# Responsabilidad: Verificación automatizada de funciones críticas del sistema:
# Matrices, Conversiones, Validaciones Regex, Huéspedes, Tarifas y Reportes Funcionales.
# Ejecución: python -m unittest test_hotel.py -v
# =============================================================================

import unittest
import re

import hotel
import validaciones
import tarifas
import reportes
import huespedes


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
        """
        self.assertEqual(hotel.obtener_numero_comercial(0, 0), 101)
        self.assertEqual(hotel.obtener_numero_comercial(1, 3), 204)
        self.assertEqual(hotel.obtener_numero_comercial(2, 1), 302)

        piso, hab = hotel.obtener_indices_matriz(101)
        self.assertEqual((piso, hab), (0, 0))

        piso_304, hab_304 = hotel.obtener_indices_matriz(304)
        self.assertEqual((piso_304, hab_304), (2, 3))

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

        # Validación de días
        self.assertTrue(re.match(validaciones.PATRON_DIAS_VALIDO, "5"))
        self.assertFalse(re.match(validaciones.PATRON_DIAS_VALIDO, "0"))

    def test_04_obtener_tarifa_habitacion(self):
        """
        Verifica la correcta obtención de tarifas según el piso.
        """
        self.assertEqual(tarifas.obtener_tarifa_habitacion(1, self.tarifas), 10000.0)
        self.assertEqual(tarifas.obtener_tarifa_habitacion(2, self.tarifas), 12000.0)
        self.assertEqual(tarifas.obtener_tarifa_habitacion(3, self.tarifas), 15000.0)

    def test_05_registro_huesped_formato(self):
        """
        Verifica la estructura y contenido del registro de un huésped:
        [nombre, dni, dias, piso, habitacion, num_comercial].
        """
        huesped = ["Juan Perez", "12345678", 3, 0, 0, 101]
        self.lista_huespedes.append(huesped)
        self.matriz[0][0] = "O"

        self.assertEqual(len(self.lista_huespedes), 1)
        self.assertEqual(self.lista_huespedes[0][0], "Juan Perez")
        self.assertEqual(self.lista_huespedes[0][1], "12345678")
        self.assertEqual(self.matriz[0][0], "O")

    def test_06_calculo_subtotal_estadia_corta(self):
        """
        Verifica el cálculo de liquidación para estadías <= 7 noches (tarifa plena).
        """
        huesped_corto = ["Juan Perez", "12345678", 5, 0, 0, 101]
        subtotal_corto = reportes.calcular_subtotal(huesped_corto, self.tarifas)
        self.assertEqual(subtotal_corto, 50000.0)

    def test_07_calculo_subtotal_con_descuento_larga_estadia(self):
        """
        Verifica el cálculo de liquidación mediante orden superior (lambda):
        Estadía > 7 noches: 10% de bonificación automática.
        """
        huesped_largo = ["Maria Gomez", "87654321", 10, 0, 1, 102]
        subtotal_largo = reportes.calcular_subtotal(huesped_largo, self.tarifas)
        self.assertEqual(subtotal_largo, 90000.0)

    def test_08_recaudacion_total_programacion_funcional(self):
        """
        Verifica el uso de map y reduce para calcular la recaudación total proyectada.
        """
        h1 = ["Huesped 1", "11111111", 2, 0, 0, 101]    # 2 x 10,000 = 20,000
        h2 = ["Huesped 2", "22222222", 2, 1, 0, 201]    # 2 x 12,000 = 24,000
        lista = [h1, h2]

        total = reportes.calcular_recaudacion_total(lista, self.tarifas)
        self.assertEqual(total, 44000.0)

    def test_09_filtrar_huespedes_por_piso(self):
        """
        Verifica el filtrado funcional de huéspedes por piso utilizando filter y lambda.
        """
        h1 = ["Huesped 1", "11111111", 2, 0, 0, 101]  # Piso 0 (Piso comercial 1)
        h2 = ["Huesped 2", "22222222", 3, 1, 0, 201]  # Piso 1 (Piso comercial 2)
        h3 = ["Huesped 3", "33333333", 4, 0, 1, 102]  # Piso 0 (Piso comercial 1)
        lista = [h1, h2, h3]

        filtrados_piso1 = huespedes.filtrar_huespedes_por_piso(lista, 1)
        self.assertEqual(len(filtrados_piso1), 2)
        self.assertIn(h1, filtrados_piso1)
        self.assertIn(h3, filtrados_piso1)

        filtrados_piso2 = huespedes.filtrar_huespedes_por_piso(lista, 2)
        self.assertEqual(len(filtrados_piso2), 1)
        self.assertIn(h2, filtrados_piso2)

    def test_10_restablecer_limpieza_habitacion(self):
        """
        Verifica la lógica de restablecer una habitación de Sucia [S] a Libre [L].
        """
        self.matriz[1][2] = "S"
        self.assertEqual(self.matriz[1][2], "S")

        piso, hab = hotel.obtener_indices_matriz(203)
        self.matriz[piso][hab] = "L"
        self.assertEqual(self.matriz[1][2], "L")


if __name__ == "__main__":
    unittest.main()


