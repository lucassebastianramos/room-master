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
    restablecer_limpieza
)
from reportes import (
    generar_reporte_ocupacion,
    calcular_recaudacion_total
)
from validaciones import (
    validar_generico,
    PATRON_DNI_VALIDO,
    ERROR_DNI
)


def menu_principal():
    # Inicializa matriz (reiniciar_matriz() se reutiliza para redimensionar el hotel)
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
        print("5. Buscar huésped por DNI")
        print("6. Reportes y Facturación")
        print("7. Redimensionar hotel")
        print("8. Restablecer habitacion")
        print("0. Salir")
        print("==============================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Configuración de la vista del hotel")
            renderizar_hotel(hotel)
        elif opcion == "2":
            renderizar_hotel(hotel)
            hotel = realizar_checkin(hotel, huespedes)
        elif opcion == "3":
            realizar_checkout(hotel, huespedes, tarifas)
        elif opcion == "4":
            reubicar_huesped_swap(hotel, huespedes)
        elif opcion == "5":
            dni_busqueda = validar_generico("Ingrese el DNI a buscar: ", PATRON_DNI_VALIDO, ERROR_DNI)
            buscar_huesped_por_dni(huespedes, dni_busqueda)
        elif opcion == "6":
            generar_reporte_ocupacion(hotel)
            calcular_recaudacion_total(huespedes, tarifas)
        elif opcion == "7":
            hotel = reiniciar_matriz()
            tarifas = configurar_tarifas_hotel(len(hotel))
            huespedes.clear()
            print("Hotel redimensionado y reiniciado con éxito")
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


