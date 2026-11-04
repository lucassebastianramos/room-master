# =============================================================================
# SISTEMA DE GESTIÓN HOTELERA: ROOM MASTER (main.py)
# =============================================================================
# Materia: Algoritmos y Estructura de Datos 1 / Programación 1
# Cátedra: Lic. Gustavo E. Escandell
# Integrantes y Legajos:
#   - Menendez Mojana, Tiara (Legajo: 1226578)
#   - Ramos, Lucas Sebastián (Legajo: 1235407)
#   - Iglesias, Luca (Legajo: 1226578)
#   - Rueda, Leandro Nicolás (Legajo: 1231246)
# =============================================================================

from hotel import (
    inicializar_hotel,
    reiniciar_matriz,
    redimensionar_hotel,
    renderizar_hotel
)
from tarifas import (
    configurar_tarifas_hotel
)
from huespedes import (
    realizar_checkin,
    realizar_checkout,
    reubicar_huesped_swap,
    buscar_huesped_por_dni,
    buscar_huespedes_por_nombre,
    buscar_huesped_por_habitacion,
    restablecer_limpieza
)
from reportes import (
    generar_reporte_ocupacion,
    calcular_recaudacion_total
)
from validaciones import (
    validar_generico,
    PATRON_DNI_VALIDO,
    ERROR_DNI,
    PATRON_TEXTO_VALIDO,
    ERROR_TEXTO,
    PATRON_NUMERO_VALIDO,
    ERROR_NUMERO
)
from archivos import (
    cargar_datos_hotel,
    guardar_datos_hotel,
    leer_y_procesar_facturacion_txt,
    historial_huesped,
    exportar_facturacion_a_csv,
    inicializar_archivo_txt
)

NOMBRE_ARCHIVO_JSON = "hotel_data.json"


def menu_busquedas(lista_huespedes):
    """Submenú de búsquedas de huéspedes."""
    ejecutando = True
    while ejecutando:
        print("\n--- BÚSQUEDAS ---")
        print("1. Buscar huésped por DNI")
        print("2. Buscar huésped por nombre")
        print("3. Buscar huésped por habitación")
        print("0. Volver al menú principal")
        print("==============================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            dni_busqueda = validar_generico("Ingrese el DNI a buscar (-1 para cancelar): ", PATRON_DNI_VALIDO, ERROR_DNI)
            if dni_busqueda == "-1":
                print("Búsqueda cancelada.")
            else:
                buscar_huesped_por_dni(lista_huespedes, dni_busqueda)
        elif opcion == "2":
            texto = validar_generico("Ingrese parte del nombre a buscar (-1 para cancelar): ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
            if texto == "-1":
                print("Búsqueda cancelada.")
            else:
                resultados = buscar_huespedes_por_nombre(lista_huespedes, texto)
                if resultados:
                    for huesped in resultados:
                        print(huesped["identidad"][1], "-", "DNI:", huesped["identidad"][0], "- Hab:", huesped["ubicacion"][2])
                else:
                    print("No se encontraron huéspedes con ese nombre.")
        elif opcion == "3":
            num_texto = validar_generico("Ingrese el número de habitación (-1 para cancelar): ", PATRON_NUMERO_VALIDO, ERROR_NUMERO)
            if num_texto == "-1":
                print("Búsqueda cancelada.")
            else:
                resultados = buscar_huesped_por_habitacion(lista_huespedes, int(num_texto))
                if resultados:
                    for huesped in resultados:
                        print(huesped["identidad"][1], "-", "DNI:", huesped["identidad"][0])
                else:
                    print("No hay huésped en esa habitación.")
        elif opcion == "0":
            ejecutando = False
        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")


def menu_principal():
    print("\nIniciando sistema Room Master... verificando archivo JSON...")
    inicializar_archivo_txt()
    # Carga de datos al inicio (Deserialización)[cite: 53, 56, 57]
    datos_cargados = cargar_datos_hotel(NOMBRE_ARCHIVO_JSON)

    if datos_cargados is not None and datos_cargados["pisos"] != -1:
        print(f"¡Datos cargados con éxito! Hotel de {datos_cargados['pisos']} pisos x {datos_cargados['habitaciones']} habs.")
        pisos = datos_cargados["pisos"]
        habitaciones = datos_cargados["habitaciones"]
        huespedes = datos_cargados["huespedes"]
        tarifas = datos_cargados["tarifas"]

        hotel = inicializar_hotel(pisos, habitaciones)
        for h in huespedes:
            hotel[h["ubicacion"][0]][h["ubicacion"][1]] = "O"
    else:
        print("No se encontraron datos previos. Se procederá a la inicialización manual.")
        hotel = reiniciar_matriz()
        pisos = len(hotel)
        habitaciones = len(hotel[0])
        tarifas = configurar_tarifas_hotel(pisos)
        huespedes = []
        guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)

    ejecutando = True

    while ejecutando:
        print("\nROOM MASTER - MENÚ PRINCIPAL\n")
        print("1. Visualizar estado del hotel")
        print("2. Check-in (Nuevo huésped)")
        print("3. Check-out (Liberar habitación)")
        print("4. Reubicar huésped (Swap)")
        print("5. Búsquedas")
        print("6. Reportes y Facturación proyectada")
        print("7. Auditoría histórica de facturación (Desde archivo .TXT)")
        print("8. Exportar facturación a formato CSV (Archivo .CSV)")
        print("9. Redimensionar hotel")
        print("10. Restablecer habitación en limpieza")
        print("11. Historial de huésped (por DNI)")
        print("0. Salir")
        print("==============================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            renderizar_hotel(hotel)

        elif opcion == "2":  # Check-in
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes)
            guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)

        elif opcion == "3":
            exito = realizar_checkout(hotel, huespedes, tarifas)
            if exito:
                guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)

        elif opcion == "4":  # Swap
            reubicar_huesped_swap(hotel, huespedes)
            guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)

        elif opcion == "5":
            menu_busquedas(huespedes)

        elif opcion == "6":
            generar_reporte_ocupacion(hotel, huespedes)
            calcular_recaudacion_total(huespedes, tarifas)

        elif opcion == "7":  # Auditoría TXT
            leer_y_procesar_facturacion_txt()

        elif opcion == "8":  # Exportación a CSV
            exportar_facturacion_a_csv()

        elif opcion == "9":  # Redimensionar hotel
            nuevo_hotel = redimensionar_hotel()
            if nuevo_hotel == -1:
                print("Redimensionamiento cancelado. Se mantienen los datos actuales.")
            else:
                print("\nDebe configurar las nuevas tarifas para el hotel redimensionado.")
                hotel = nuevo_hotel
                pisos = len(hotel)
                habitaciones = len(hotel[0])
                tarifas = configurar_tarifas_hotel(pisos)
                huespedes.clear()
                guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)
                print("Hotel redimensionado y configurado con éxito.")

        elif opcion == "10":
            print("\n--- RESTABLECER HABITACIÓN A LIBRE [L] ---")
            restablecer_limpieza(hotel)
            guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)

        elif opcion == "11":
            dni_hist = validar_generico("Ingrese el DNI del huésped: ", PATRON_DNI_VALIDO, ERROR_DNI)
            historial_huesped(dni_hist)
            input("\nPresione [Enter] para continuar...")

        elif opcion == "0":
            print("Guardando datos y saliendo del sistema Room Master...")
            guardar_datos_hotel(NOMBRE_ARCHIVO_JSON, pisos, habitaciones, huespedes, tarifas)
            ejecutando = False

        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")


if __name__ == "__main__":
    menu_principal()