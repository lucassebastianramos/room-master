# =============================================================================
# SISTEMA DE GESTIÓN HOTELERA: ROOM MASTER
# =============================================================================
# Materia: Algoritmos y Estructura de Datos 1 / Programación 1
# Cátedra: Lic. Gustavo E. Escandell
# Arquitectura: Modular, Procedural y Desacoplada (Sin POO, Vista Única)
# =============================================================================
# Módulos del Sistema:
#   - hotel.py: Matrices bidimensionales, estados (L, O, S, M), coordenadas y sets.
#   - huespedes.py: Check-in, Check-out, Swap, consumos extras, extensiones y búsqueda.
#   - tarifas.py: Precios por piso y segmentación de suites de lujo.
#   - reportes.py: Análisis y facturación mediante map, filter y functools.reduce.
#   - persistencia.py: Almacenamiento y recuperación en archivos JSON.
#   - validaciones.py: Integridad de datos y expresiones regulares (Regex).
# =============================================================================

from hotel import (
    reiniciar_matriz,
    renderizar_hotel,
    enviar_a_mantenimiento,
    liberar_de_mantenimiento
)
from tarifas import (
    configurar_tarifas_hotel,
    mostrar_resumen_tarifas,
    menu_configuracion_tarifas
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
from persistencia import (
    guardar_datos_json,
    cargar_datos_json,
    existe_datos_json
)
from validaciones import (
    validar_generico_con_cancelacion,
    solicitar_dimension_valida,
    confirmar_accion,
    PATRON_DNI_VALIDO,
    ERROR_DNI
)


def ejecutar_menu_hotel(hotel, huespedes, tarifas):
    """
    Menú interactivo unificado de administración y gestión integral del hotel.
    Reúne el ciclo de vida completo: Alta, Baja, Modificación, Consulta,
    Mantenimiento, Limpieza, Reportes y Persistencia JSON.
    """
    ejecutando = True

    while ejecutando:
        print("\n" + "=" * 60)
        print("          ROOM MASTER - PANEL DE GESTIÓN INTEGRAL          ")
        print("=" * 60)
        print("1.  Visualizar estado del hotel (Habitaciones y Estados)")
        print("2.  Check-in (Alta de reserva con confirmación y validación de DNI)")
        print("3.  Check-out (Baja y liquidación con consumos extras)")
        print("4.  Reubicar huésped (Modificación - Swap de habitación)")
        print("5.  Cargar consumos adicionales (Minibar, Cochera, Servicios)")
        print("6.  Extender estadía de un huésped (Noches adicionales)")
        print("7.  Buscar huésped por DNI (Consulta rápida con conjunto/set)")
        print("8.  Filtrar huéspedes por piso (Consulta funcional con filter)")
        print("9.  Reportes y Facturación (Ocupación y Recaudación Total)")
        print("10. Enviar habitación a Mantenimiento [M]")
        print("11. Habilitar habitación reparada desde Mantenimiento [L]")
        print("12. Restablecer habitación a Disponible tras Limpieza [L]")
        print("13. Configuración y consulta de tarifas por piso")
        print("14. Guardar estado del hotel en archivo JSON")
        print("15. Cargar estado del hotel desde archivo JSON")
        print("16. Redimensionar hotel (Reiniciar matriz y tarifas)")
        print("0.  Salir del sistema")
        print("=" * 60)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            renderizar_hotel(hotel)

        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes, tarifas)

        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas)

        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)

        elif opcion == "5":
            cargar_consumo_habitacion(hotel, huespedes)

        elif opcion == "6":
            extender_estadia_huesped(hotel, huespedes)

        elif opcion == "7":
            dni_busqueda = validar_generico_con_cancelacion(
                "Ingrese el DNI a buscar (o 0 para cancelar): ",
                PATRON_DNI_VALIDO,
                ERROR_DNI
            )
            if dni_busqueda is not None:
                buscar_huesped_por_dni(huespedes, dni_busqueda)

        elif opcion == "8":
            if len(huespedes) == 0:
                print("\n[Aviso] No hay huéspedes alojados actualmente en el hotel.")
            else:
                piso_f = solicitar_dimension_valida(
                    f"Piso a consultar (1 a {len(hotel)}): ",
                    1,
                    len(hotel)
                )
                filtrados = filtrar_huespedes_por_piso(huespedes, piso_f)
                if len(filtrados) > 0:
                    print(f"\n--- Huéspedes alojados en Piso {piso_f} ---")
                    for h in filtrados:
                        # Estructura: [(dni, nombre), (piso, hab, num), dias, extras]
                        nombre = h[0][1]
                        dni = h[0][0]
                        num_hab = h[1][2]
                        dias = h[2]
                        extras = float(h[3]) if len(h) > 3 else 0.0
                        extras_txt = f" | Extras: ${extras:,.2f}" if extras > 0 else ""
                        print(f"- {nombre} (DNI: {dni}) | Habitación: {num_hab} | Estadía: {dias} noches{extras_txt}")
                else:
                    print(f"\n[Aviso] No hay huéspedes registrados en el Piso {piso_f}.")

        elif opcion == "9":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes, tarifas)

        elif opcion == "10":
            enviar_a_mantenimiento(hotel)

        elif opcion == "11":
            liberar_de_mantenimiento(hotel)

        elif opcion == "12":
            restablecer_limpieza(hotel)

        elif opcion == "13":
            menu_configuracion_tarifas(tarifas, len(hotel))

        elif opcion == "14":
            if guardar_datos_json(hotel, huespedes, tarifas):
                print("\n[Éxito] El estado del hotel se guardó correctamente en archivo JSON.")

        elif opcion == "15":
            if confirmar_accion("¿Está seguro de cargar datos de JSON? Se sobrescribirá el estado actual en memoria (s/n): "):
                datos = cargar_datos_json()
                if datos:
                    hotel = datos["hotel"]
                    huespedes.clear()
                    for h in datos["huespedes"]:
                        huespedes.append(h)
                    tarifas.clear()
                    for t in datos["tarifas"]:
                        tarifas.append(t)
                    print("\n[Éxito] Estado restaurado exitosamente desde archivo JSON.")
                else:
                    print("\n[Aviso] No se pudo cargar el archivo JSON o no existe.")

        elif opcion == "16":
            if confirmar_accion("¿Confirma redimensionar el hotel? Esto reseteará las habitaciones y huéspedes (s/n): "):
                hotel = reiniciar_matriz()
                tarifas = configurar_tarifas_hotel(len(hotel))
                huespedes.clear()
                print("\n[Éxito] Hotel redimensionado y registros reiniciados.")

        elif opcion == "0":
            if confirmar_accion("¿Desea guardar los cambios en archivo JSON antes de salir? (s/n): "):
                guardar_datos_json(hotel, huespedes, tarifas)
                print("[Éxito] Datos guardados.")
            print("\n¡Gracias por utilizar Room Master! Hasta luego.")
            ejecutando = False

        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")

    return hotel, huespedes, tarifas


def menu_principal():
    """
    Punto de entrada de la aplicación Room Master.
    Verifica existencia de persistencia JSON previa o inicializa nueva matriz.
    """
    print("\n" + "=" * 60)
    print("      BIENVENIDO AL SISTEMA HOTELERO ROOM MASTER     ")
    print("=" * 60)

    hotel = None
    huespedes = []
    tarifas = []

    # Verificación de datos persistidos en JSON
    if existe_datos_json():
        print("\nSe encontró un archivo de datos guardado previamente en formato JSON.")
        if confirmar_accion("¿Desea restaurar el estado del hotel desde JSON? (s/n): "):
            datos = cargar_datos_json()
            if datos:
                hotel = datos["hotel"]
                huespedes = datos["huespedes"]
                tarifas = datos["tarifas"]
                print(f"[Éxito] Restaurado hotel de {len(hotel)} pisos con {len(huespedes)} huéspedes registrados.")

    # Si no se cargó desde JSON, inicializa configuración fresca
    if hotel is None:
        hotel = reiniciar_matriz()
        tarifas = configurar_tarifas_hotel(len(hotel))
        huespedes = []

    ejecutar_menu_hotel(hotel, huespedes, tarifas)


if __name__ == "__main__":
    menu_principal()

