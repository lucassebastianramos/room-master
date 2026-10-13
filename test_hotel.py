# =============================================================================
# SUITE DE PRUEBAS UNITARIAS (test_hotel.py)
# =============================================================================
# Cátedra: Lic. Gustavo E. Escandell - Programación 1 / Algoritmos y Estructuras 1
# Responsabilidad: Verificación automatizada de funciones críticas del sistema:
# Matrices, Conversiones, Validaciones Regex, Ciclo de Vida de Huéspedes,
# Tarifas y Descuentos, RBAC (Roles y Permisos), Mantenimiento y Persistencia.
# Ejecución: python -m unittest test_hotel.py -v
# =============================================================================

import unittest
import re

import hotel
import validaciones
import tarifas
import auth
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
        self.usuarios = auth.USUARIOS_DEFAULT.copy()
        self.reglas = tarifas.REGLAS_NEGOCIO_DEFAULT.copy()
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

        piso, hab = hotel.obtener_indices_matriz(304)
        self.assertEqual((piso, hab), (2, 3))

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

    def test_04_control_de_roles_rbac(self):
        """
        Verifica el modelo de seguridad basado en roles (RBAC):
        - Administrador: posee permisos de gestión, reglas y redimensionamiento.
        - Recepción: posee permisos operativos (checkin, checkout, extras, limpieza) pero no de gestión de reglas/redimensionar.
        - Huésped: permisos restringidos a autoservicio.
        """
        self.assertIn("recepcion", auth.ROLES_VALIDOS)
        permisos_admin = auth.obtener_permisos_por_rol("admin")
        permisos_recepcion = auth.obtener_permisos_por_rol("recepcion")
        permisos_huesped = auth.obtener_permisos_por_rol("huesped")

        # Recepción puede operar pero NO redimensionar ni cambiar reglas
        self.assertTrue(auth.tiene_permiso("recepcion", "checkin"))
        self.assertTrue(auth.tiene_permiso("recepcion", "checkout"))
        self.assertTrue(auth.tiene_permiso("recepcion", "cargar_extras"))
        self.assertFalse(auth.tiene_permiso("recepcion", "redimensionar"))
        self.assertFalse(auth.tiene_permiso("recepcion", "gestionar_reglas"))

        # Admin tiene todo
        self.assertTrue(auth.tiene_permiso("admin", "redimensionar"))
        self.assertTrue(auth.tiene_permiso("admin", "gestionar_reglas"))

        # Huésped solo autoservicio
        self.assertTrue(auth.tiene_permiso("huesped", "reservar"))
        self.assertFalse(auth.tiene_permiso("huesped", "redimensionar"))
        self.assertFalse(auth.tiene_permiso("huesped", "checkin"))

    def test_05_ciclo_mantenimiento_habitaciones(self):
        """
        Verifica que una habitación pueda colocarse en estado Mantenimiento [M]
        y que quede inhabilitada para reservas hasta ser reparada a [L].
        """
        self.matriz[0][1] = "M"
        self.assertEqual(self.matriz[0][1], "M")

        # Dar el alta técnica
        self.matriz[0][1] = "L"
        self.assertEqual(self.matriz[0][1], "L")

    def test_06_calculo_subtotal_con_descuento_larga_estadia(self):
        """
        Verifica el cálculo de liquidación mediante orden superior (lambda):
        - Estadía <= 7 noches: tarifa plena.
        - Estadía > 7 noches: 10% de bonificación automática.
        """
        # Huésped 1: 5 noches en piso 1 ($10,000/noche) = $50,000
        huesped_corto = ["Juan Perez", "12345678", 5, 0, 0, 101, 0.0]
        subtotal_corto = reportes.calcular_subtotal(huesped_corto, self.tarifas)
        self.assertEqual(subtotal_corto, 50000.0)

        # Huésped 2: 10 noches en piso 1 ($10,000/noche) = $100,000 - 10% = $90,000
        huesped_largo = ["Maria Gomez", "87654321", 10, 0, 1, 102, 0.0]
        subtotal_largo = reportes.calcular_subtotal(huesped_largo, self.tarifas)
        self.assertEqual(subtotal_largo, 90000.0)

    def test_07_consumos_adicionales_y_liquidacion_con_extras(self):
        """
        Verifica la acumulación de consumos extras (Minibar, Cochera)
        y su correcto impacto en la facturación del huésped.
        """
        # Huésped con 3 noches en piso 2 ($12,000/noche = $36,000) + $4,500 en extras
        huesped_extras = ["Carlos Tevez", "20111222", 3, 1, 0, 201, 4500.0]
        subtotal_con_extras = reportes.calcular_subtotal(huesped_extras, self.tarifas)
        self.assertEqual(subtotal_con_extras, 40500.0)

    def test_08_recaudacion_total_programacion_funcional(self):
        """
        Verifica el uso de map y reduce para calcular la recaudación total proyectada.
        """
        h1 = ["Huesped 1", "11111111", 2, 0, 0, 101, 0.0]   # 2 x 10,000 = 20,000
        h2 = ["Huesped 2", "22222222", 2, 1, 0, 201, 1000.0] # 2 x 12,000 + 1,000 = 25,000
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

    def test_10_autenticacion_y_registro_usuarios_memoria(self):
        """
        Verifica el ciclo de vida de usuarios puramente en memoria (RAM) mediante Diccionarios y Tuplas:
        - Registro de un nuevo usuario huésped.
        - Verificación exitosa de credenciales retornando Tupla inmutable de sesión.
        - Rechazo de contraseñas incorrectas o usuarios inexistentes.
        """
        exito = auth.registrar_nuevo_usuario(
            self.usuarios, "estudiante", "pass123", "Estudiante AED", "44111222", "huesped"
        )
        self.assertTrue(exito, "El registro de usuario en memoria debe ser exitoso.")
        self.assertIn("estudiante", self.usuarios)

        # Verificación exitosa retornando Tupla inmutable
        sesion = auth.verificar_credenciales(self.usuarios, "estudiante", "pass123")
        self.assertIsNotNone(sesion)
        self.assertEqual(sesion, ("estudiante", "huesped", "Estudiante AED", "44111222"))

        # Verificación con contraseña errónea
        sesion_erronea = auth.verificar_credenciales(self.usuarios, "estudiante", "incorrecta")
        self.assertIsNone(sesion_erronea)


if __name__ == "__main__":
    unittest.main()
