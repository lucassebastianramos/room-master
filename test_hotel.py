# =============================================================================
# SUITE DE PRUEBAS UNITARIAS ACTUALIZADA (test_hotel.py)
# =============================================================================

import unittest
import hotel
import reportes
import huespedes


class TestRoomMaster(unittest.TestCase):

    def setUp(self):
        self.matriz = hotel.inicializar_hotel(3, 4)
        self.tarifas = [[1, 10000.0], [2, 12000.0], [3, 15000.0]]
        self.lista_huespedes = []

    def test_05_registro_huesped_formato_diccionario(self):
        """
        Verifica el registro de un huésped en formato diccionario.
        """
        huesped = {
            "nombre": "Juan Perez",
            "dni": "12345678",
            "dias": 3,
            "piso": 0,
            "habitacion": 0,
            "num_comercial": 101
        }
        self.lista_huespedes.append(huesped)
        self.matriz[0][0] = "O"

        self.assertEqual(len(self.lista_huespedes), 1)
        self.assertEqual(self.lista_huespedes[0]["nombre"], "Juan Perez")
        self.assertEqual(self.lista_huespedes[0]["dni"], "12345678")
        self.assertEqual(self.matriz[0][0], "O")

    def test_06_calculo_subtotal_diccionario(self):
        huesped = {"nombre": "Juan", "dni": "12345678", "dias": 5, "piso": 0, "habitacion": 0, "num_comercial": 101}
        subtotal = reportes.calcular_subtotal(huesped, self.tarifas)
        self.assertEqual(subtotal, 50000.0)

    def test_09_filtrar_huespedes_por_piso_diccionario(self):
        h1 = {"nombre": "H1", "dni": "11111111", "dias": 2, "piso": 0, "habitacion": 0, "num_comercial": 101}
        h2 = {"nombre": "H2", "dni": "22222222", "dias": 3, "piso": 1, "habitacion": 0, "num_comercial": 201}
        lista = [h1, h2]

        filtrados = huespedes.filtrar_huespedes_por_piso(lista, 1)
        self.assertEqual(len(filtrados), 1)
        self.assertEqual(filtrados[0]["nombre"], "H1")


if __name__ == "__main__":
    unittest.main()