# =============================================================================
# SISTEMA DE GESTIÓN HOTELERA: ROOM MASTER (main.py)
# =============================================================================
# Materia: Algoritmos y Estructura de Datos 1 / Programación 1
# Cátedra: Lic. Gustavo E. Escandell
# Integrantes:
#   - Menendez Mojana, Tiara
#   - Ramos, Lucas Sebastián
#   - Iglesias, Luca
#   - Rueda, Leandro Nicolás
# =============================================================================

from hotel import (
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
    calcular_recaudacion_total,
    reporte_habitaciones_libres
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
    hotel = reiniciar_matriz()

    # Matriz de tarifas dinámica: [ [Piso, Precio por noche], ... ]
    tarifas = configurar_tarifas_hotel(len(hotel))

    # Registro de huéspedes (Formato: [nombre, dni, dias, piso, habitacion, num_comercial])
    huespedes = []

    ejecutando = True

    while ejecutando:
        print("\nROOM MASTER - MENÚ PRINCIPAL\n")
        print("1. Visualizar estado del hotel")
        print("2. Check-in (Nuevo huésped)")
        print("3. Check-out (Liberar habitación)")
        print("4. Reubicar huésped (Swap)")
        print("5. Búsquedas")
        print("6. Reportes y Facturación")
        print("7. Redimensionar hotel")
        print("8. Restablecer habitacion")
        print("0. Salir")
        print("==============================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            menu_busquedas(huespedes)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            reporte_habitaciones_libres(hotel, huespedes)
            calcular_recaudacion_total(huespedes, tarifas)
        elif opcion == "7":
            nuevo_hotel = redimensionar_hotel()
            
            if nuevo_hotel == -1:
                print("Redimensionamiento cancelado. Se mantienen los datos actuales.")
            else:
                # Si aceptó cambiar la matriz, DEBE configurar las tarifas para el nuevo tamaño
                print("\nDebe configurar las nuevas tarifas para el hotel redimensionado.")
                hotel = nuevo_hotel
                tarifas = configurar_tarifas_hotel(len(hotel))
                huespedes.clear()
                print("Hotel redimensionado y configurado con éxito.")
        elif opcion == "8":
            print("\n--- RESTABLECER HABITACIÓN A LIBRE [L] ---")
            restablecer_limpieza(hotel)
        elif opcion == "0":
            print("Saliendo del sistema Room Master...")
            ejecutando = False  # Sale del bucle
        else:
            print("Opción inválida. Intente nuevamente.")

        # Muestra el resultado del menu de opciones hasta accion del usuario
        if opcion != "0":
            input("\nPresione [Enter] para continuar...")


# Ejecución
if __name__ == "__main__":
    menu_principal()


