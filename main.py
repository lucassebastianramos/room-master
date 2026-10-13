# =============================================================================
# SISTEMA DE GESTIÓN HOTELERA: ROOM MASTER
# =============================================================================
# Materia: Algoritmos y Estructura de Datos 1 / Programación 1
# Cátedra: Lic. Gustavo E. Escandell
# Arquitectura de Software: Modular, Multicapa y Desacoplada
# =============================================================================
# Módulos del Sistema:
#   - auth.py: Autenticación, control de roles (RBAC), perfiles y gestión de usuarios.
#   - hotel.py: Matrices bidimensionales, renderizado, estados (L, O, S, M) y mantenimiento.
#   - tarifas.py: Precios por piso, suites, oferta/demanda y políticas configurables.
#   - huespedes.py: Check-in, liquidación con consumos extras, extensión, swap y búsqueda.
#   - reportes.py: Análisis y facturación mediante orden superior (map, filter, reduce).
#   - validaciones.py: Integridad de datos y expresiones regulares (Regex).
# =============================================================================

import auth
from hotel import (
    reiniciar_matriz,
    renderizar_hotel,
    enviar_a_mantenimiento,
    liberar_de_mantenimiento
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
    restablecer_limpieza,
    cargar_consumo_habitacion,
    extender_estadia_huesped
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
        print("\n" + "=" * 58)
        print(f"     PANEL DE ADMINISTRACIÓN GENERAL - Operador: {nombre}")
        print("=" * 58)
        print("1.  Visualizar estado del hotel (Habitaciones y Estados)")
        print("2.  Check-in (Registrar nuevo huésped con confirmación)")
        print("3.  Check-out (Liberar habitación y liquidar cuenta con extras)")
        print("4.  Reubicar huésped (Swap de habitación)")
        print("5.  Cargar consumo adicional (Minibar, Cochera, Servicios)")
        print("6.  Extender estadía de un huésped (Noches adicionales)")
        print("7.  Buscar huésped por DNI")
        print("8.  Reportes y Facturación (Métricas analíticas y filtros)")
        print("9.  Poner habitación en Mantenimiento / Fuera de servicio [M]")
        print("10. Habilitar habitación reparada desde Mantenimiento [L]")
        print("11. Restablecer habitación a Disponible tras Limpieza [L]")
        print("12. Redimensionar hotel (Reiniciar matriz)")
        print("13. Gestión de Usuarios y Roles (Crear, Editar, Listar)")
        print("14. Políticas de Negocio y Precios Dinámicos (Oferta/Demanda)")
        print("0.  Cerrar sesión")
        print("=" * 58)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes, tarifas, sesion, reglas_negocio)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas, reglas_negocio)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            cargar_consumo_habitacion(hotel, huespedes)
        elif opcion == "6":
            extender_estadia_huesped(hotel, huespedes, reglas_negocio)
        elif opcion == "7":
            dni_busqueda = validar_generico_con_cancelacion("Ingrese el DNI a buscar: ", PATRON_DNI_VALIDO, ERROR_DNI)
            if dni_busqueda is not None:
                buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "8":
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
                            extras = float(h[6]) if len(h) > 6 else 0.0
                            extras_txt = f" | Extras: ${extras:,.2f}" if extras > 0 else ""
                            print(f"- {h[0]} (DNI: {h[1]}) | Habitación: {h[5]} | Días: {h[2]}{extras_txt}")
                    else:
                        print(f"\n[Aviso] No hay huéspedes registrados en el Piso {piso_f}.")
        elif opcion == "9":
            enviar_a_mantenimiento(hotel)
        elif opcion == "10":
            liberar_de_mantenimiento(hotel)
        elif opcion == "11":
            print("\n--- RESTABLECER HABITACIÓN TRAS LIMPIEZA ---")
            restablecer_limpieza(hotel)
        elif opcion == "12":
            hotel = reiniciar_matriz()
            tarifas = configurar_tarifas_hotel(len(hotel))
            huespedes.clear()
            print("\n[Éxito] Hotel redimensionado y registros reiniciados.")
        elif opcion == "13":
            auth.menu_gestion_usuarios(usuarios, sesion)
        elif opcion == "14":
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
        print("2. Reservar habitación (Check-in online)")
        print("3. Consultar mi reserva / estadía")
        print("4. Extender estadía (Noches adicionales)")
        print("5. Ver tarifas vigentes por piso")
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
            extender_estadia_huesped(hotel, huespedes, reglas_negocio)
        elif opcion == "5":
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
    print("\n" + "=" * 58)
    print("      BIENVENIDO AL SISTEMA HOTELERO ROOM MASTER     ")
    print("=" * 58)

    # 1. Configuración inicial de matrices y tarifas
    hotel = reiniciar_matriz()
    tarifas = configurar_tarifas_hotel(len(hotel))

    # 2. Registros de huéspedes en memoria: [nombre, dni, dias, piso, habitacion, num_comercial, extras]
    huespedes = []

    # 3. Base de usuarios en memoria (Diccionarios y Roles - auth.py)
    usuarios = auth.USUARIOS_DEFAULT.copy()

    # 4. Diccionario de reglas de negocio configurables por el administrador
    reglas_negocio = REGLAS_NEGOCIO_DEFAULT.copy()

    sistema_activo = True

    while sistema_activo:
        # Flujo de login obligatorio (Retorna tupla (usuario, rol, nombre, dni) o None al salir)
        sesion = auth.flujo_login(usuarios, reglas_negocio)

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
