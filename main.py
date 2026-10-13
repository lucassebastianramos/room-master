# =============================================================================
# SISTEMA DE GESTIÓN HOTELERA: ROOM MASTER
# =============================================================================
# Materia: Algoritmos y Estructura de Datos 1 / Programación 1
# Cátedra: Lic. Gustavo E. Escandell
# Arquitectura de Software: Modular, Multicapa y Desacoplada
# =============================================================================
# Módulos del Sistema:
#   - auth.py: Autenticación, control de roles (RBAC), perfiles y gestión de usuarios.
#   - hotel.py: Matrices bidimensionales, renderizado y disponibilidad de habitaciones.
#   - tarifas.py: Precios por piso, suites, oferta/demanda y reglas de negocio.
#   - huespedes.py: Check-in inteligente, confirmaciones, cancelaciones, check-out y swap.
#   - reportes.py: Análisis y facturación mediante orden superior (map, filter, reduce).
#   - validaciones.py: Integridad de datos y expresiones regulares (Regex).
# =============================================================================

import auth
from hotel import (
    reiniciar_matriz,
    renderizar_hotel
)
from tarifas import (
    configurar_tarifas_hotel,
    mostrar_resumen_tarifas,
    menu_configuracion_reglas_negocio,
    REGLAS_NEGOCIO_DEFAULT
)
from huespedes import (
    realizar_checkin,
    realizar_checkout,
    reubicar_huesped_swap,
    buscar_huesped_por_dni,
    filtrar_huespedes_por_piso,
    restablecer_limpieza
)
from reportes import (
    generar_reporte_ocupacion,
    calcular_recaudacion_total
)
from validaciones import (
    validar_generico_con_cancelacion,
    solicitar_dimension_valida,
    PATRON_DNI_VALIDO,
    ERROR_DNI
)


def menu_admin(hotel, huespedes, tarifas, sesion, usuarios, reglas_negocio):
    """
    Panel de administración integral del hotel.
    Acceso exclusivo para usuarios con rol 'admin'.
    """
    username, rol, nombre = sesion[:3]
    ejecutando = True

    while ejecutando:
        print("\n" + "=" * 55)
        print(f"   PANEL DE ADMINISTRACIÓN - Operador: {nombre}")
        print("=" * 55)
        print("1.  Visualizar estado del hotel")
        print("2.  Check-in (Nuevo huésped con confirmación)")
        print("3.  Check-out (Liberar habitación y facturar)")
        print("4.  Reubicar huésped (Swap)")
        print("5.  Buscar huésped por DNI")
        print("6.  Reportes y Facturación")
        print("7.  Redimensionar hotel")
        print("8.  Restablecer habitación (Limpieza)")
        print("9.  Gestión de Usuarios y Roles (Crear, Editar, Listar)")
        print("10. Reglas de Negocio y Precios Dinámicos (Oferta/Demanda)")
        print("0.  Cerrar sesión")
        print("=" * 55)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes, tarifas, sesion, reglas_negocio)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            dni_busqueda = validar_generico_con_cancelacion("Ingrese el DNI a buscar: ", PATRON_DNI_VALIDO, ERROR_DNI)
            if dni_busqueda is not None:
                buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes, tarifas)
            if len(huespedes) > 0:
                ver_filtro = input("\n¿Desea filtrar huéspedes de un piso específico? (s/n): ").strip().lower()
                if ver_filtro in ["s", "si", "sí"]:
                    piso_f = solicitar_dimension_valida(f"Piso a consultar (1 a {len(hotel)}): ", 1, len(hotel))
                    filtrados = filtrar_huespedes_por_piso(huespedes, piso_f)
                    if len(filtrados) > 0:
                        print(f"\n--- Huéspedes alojados en Piso {piso_f} ---")
                        for h in filtrados:
                            print(f"- {h[0]} (DNI: {h[1]}) | Habitación: {h[5]} | Días: {h[2]}")
                    else:
                        print(f"\n[Aviso] No hay huéspedes registrados en el Piso {piso_f}.")
        elif opcion == "7":
            hotel = reiniciar_matriz()
            tarifas = configurar_tarifas_hotel(len(hotel))
            huespedes.clear()
            print("\n[Éxito] Hotel redimensionado y registros reiniciados.")
        elif opcion == "8":
            print("\n--- RESTABLECER HABITACIÓN A LIBRE [L] ---")
            restablecer_limpieza(hotel)
        elif opcion == "9":
            auth.menu_gestion_usuarios(usuarios, sesion)
        elif opcion == "10":
            menu_configuracion_reglas_negocio(tarifas, reglas_negocio, len(hotel))
        elif opcion == "0":
            print(f"\nCerrando sesión de {nombre}...")
            ejecutando = False
        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

    return hotel, tarifas


def menu_huesped(hotel, huespedes, tarifas, sesion, reglas_negocio):
    """
    Portal de autoservicio para clientes y huéspedes.
    Acceso para usuarios con rol 'huesped'.
    """
    username = sesion[0]
    nombre = sesion[2]
    dni_cuenta = sesion[3] if len(sesion) > 3 else ""
    ejecutando = True

    while ejecutando:
        print("\n" + "=" * 55)
        print(f"      PORTAL DEL HUÉSPED - Bienvenido/a {nombre}")
        print("=" * 55)
        print("1. Visualizar disponibilidad del hotel")
        print("2. Reservar habitación (Check-in)")
        print("3. Consultar mi reserva / estadía")
        print("4. Ver tarifas vigentes por piso")
        print("0. Cerrar sesión")
        print("=" * 55)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes, tarifas, sesion, reglas_negocio)
        elif opcion == "3":
            if dni_cuenta:
                print(f"\nConsultando reserva con su DNI registrado ({dni_cuenta})...")
                buscar_huesped_por_dni(huespedes, dni_cuenta)
            else:
                dni_busqueda = validar_generico_con_cancelacion("Ingrese su DNI para buscar su reserva: ", PATRON_DNI_VALIDO, ERROR_DNI)
                if dni_busqueda is not None:
                    buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "4":
            mostrar_resumen_tarifas(tarifas)
        elif opcion == "0":
            print(f"\nCerrando sesión de {nombre}...")
            ejecutando = False
        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

    return hotel


def menu_principal():
    """
    Punto de entrada de la aplicación Room Master.
    Inicializa el estado en memoria y gestiona la autenticación con roles RBAC.
    """
    print("\n" + "=" * 55)
    print("      BIENVENIDO AL SISTEMA HOTELERO ROOM MASTER     ")
    print("=" * 55)

    # 1. Configuración inicial de matrices y tarifas
    hotel = reiniciar_matriz()
    tarifas = configurar_tarifas_hotel(len(hotel))

    # 2. Registros de huéspedes en memoria: [nombre, dni, dias, piso, habitacion, num_comercial]
    huespedes = []

    # 3. Base de usuarios en memoria (Diccionarios y Roles - auth.py)
    usuarios = auth.USUARIOS_DEFAULT.copy()

    # 4. Diccionario de reglas de negocio configurables por el administrador
    reglas_negocio = REGLAS_NEGOCIO_DEFAULT.copy()

    sistema_activo = True

    while sistema_activo:
        # Flujo de login obligatorio (Retorna tupla (usuario, rol, nombre, dni) o None al salir)
        sesion = auth.flujo_login(usuarios)

        if sesion is None:
            print("\n¡Gracias por utilizar Room Master! Hasta luego.")
            sistema_activo = False
        else:
            rol = sesion[1]
            if rol == "admin":
                hotel, tarifas = menu_admin(hotel, huespedes, tarifas, sesion, usuarios, reglas_negocio)
            elif rol == "huesped":
                hotel = menu_huesped(hotel, huespedes, tarifas, sesion, reglas_negocio)


if __name__ == "__main__":
    menu_principal()
