# =============================================================================
# MÓDULO DE AUTENTICACIÓN Y CONTROL DE ROLES (Lucas - Fase 2)
# =============================================================================
# Aplica:
# - Diccionarios (dict): Estructura de credenciales y datos de usuarios.
# - Tuplas (tuple): Sesión inmutable activa (username, rol, nombre) y constantes.
# - Conjuntos (set): Conjuntos de permisos para validación de acceso por rol.
# - Excepciones (try/except): Manejo seguro de búsquedas y validación de tipos.
# =============================================================================

import re

# Constantes inmutables representadas mediante Tuplas
ROLES_VALIDOS = ("admin", "huesped")

# Permisos definidos mediante Conjuntos (set) para verificar accesos
PERMISOS_ADMIN = {
    "ver_hotel",
    "checkin",
    "checkout",
    "swap",
    "buscar_dni",
    "reportes",
    "redimensionar",
    "restablecer"
}

PERMISOS_HUESPED = {
    "ver_hotel",
    "reservar",
    "consultar_estadia"
}

# Base de datos inicial en memoria usando Diccionarios (dict)
USUARIOS_DEFAULT = {
    "admin": {
        "password": "admin",
        "rol": "admin",
        "nombre": "Administrador del Hotel"
    },
    "recepcion": {
        "password": "1234",
        "rol": "admin",
        "nombre": "Recepcionista de Turno"
    },
    "cliente": {
        "password": "1234",
        "rol": "huesped",
        "nombre": "Huésped Frecuente"
    }
}


def obtener_permisos_por_rol(rol):
    """
    Retorna el conjunto (set) de permisos habilitados según el rol del usuario.
    Demuestra el uso de conjuntos para verificar pertenencia y reglas de seguridad.
    """
    if rol == "admin":
        return PERMISOS_ADMIN.copy()
    elif rol == "huesped":
        return PERMISOS_HUESPED.copy()
    return set()


def verificar_credenciales(diccionario_usuarios, username, password):
    """
    Verifica si el usuario y contraseña coinciden en el diccionario de usuarios.
    Utiliza manejo de excepciones (KeyError / TypeError) para acceso seguro.
    Retorna una Tupla (username, rol, nombre) si es válido, o None si no coincide.
    """
    try:
        usuario_data = diccionario_usuarios[username]
        if usuario_data["password"] == password:
            # Retorna una Tupla inmutable que representa la sesión activa
            sesion = (username, usuario_data["rol"], usuario_data["nombre"])
            return sesion
        return None
    except KeyError:
        # El nombre de usuario no existe en el diccionario
        return None
    except TypeError:
        # El diccionario recibido o los datos tienen un formato no esperado
        return None


def registrar_nuevo_usuario(diccionario_usuarios, username, password, nombre, rol="huesped"):
    """
    Registra un nuevo usuario en el diccionario.
    Valida que el nombre de usuario no exista y que el rol sea válido.
    Retorna True si fue exitoso, False en caso contrario.
    """
    try:
        username_limpio = username.strip().lower()
        if not username_limpio or len(username_limpio) < 3:
            print("Error: El nombre de usuario debe tener al menos 3 caracteres.")
            return False

        if username_limpio in diccionario_usuarios:
            print(f"Error: El usuario '{username_limpio}' ya se encuentra registrado.")
            return False

        if rol not in ROLES_VALIDOS:
            print(f"Error: El rol '{rol}' no es válido.")
            return False

        # Asignación segura en el diccionario
        diccionario_usuarios[username_limpio] = {
            "password": password.strip(),
            "rol": rol,
            "nombre": nombre.strip()
        }
        return True
    except (AttributeError, TypeError) as error:
        print(f"Error al registrar usuario: formato de datos inválido ({error}).")
        return False


def flujo_login(diccionario_usuarios):
    """
    Gestiona la pantalla interactiva de inicio de sesión o registro.
    Retorna la Tupla de sesión (username, rol, nombre) al loguearse con éxito,
    o None si el usuario decide salir del sistema.
    """
    sesion_iniciada = None

    while sesion_iniciada is None:
        print("\n" + "=" * 50)
        print("          ROOM MASTER - INICIO DE SESIÓN          ")
        print("=" * 50)
        print("1. Iniciar sesión con usuario existente")
        print("2. Registrarse como nuevo huésped")
        print("0. Salir de la aplicación")
        print("=" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- INGRESO DE CREDENCIALES ---")
            usuario = input("Usuario: ").strip().lower()
            password = input("Contraseña: ").strip()

            sesion = verificar_credenciales(diccionario_usuarios, usuario, password)
            if sesion is not None:
                # Desempaquetado seguro de la Tupla
                user, rol, nombre = sesion
                print("\n==================================================")
                print(f"¡Bienvenido/a, {nombre}!")
                print(f"Sesión iniciada con rol: [{rol.upper()}]")
                print("==================================================")
                return sesion
            else:
                print("\n[Error] Usuario o contraseña incorrectos. Intente nuevamente.")

        elif opcion == "2":
            print("\n--- REGISTRO DE NUEVO HUÉSPED ---")
            nuevo_user = input("Elija un nombre de usuario (mínimo 3 letras): ").strip().lower()
            nueva_pass = input("Elija su contraseña: ").strip()
            nombre_real = input("Ingrese su nombre y apellido: ").strip()

            if not nueva_pass or len(nueva_pass) < 3:
                print("Error: La contraseña debe tener al menos 3 caracteres.")
            elif not nombre_real:
                print("Error: Debe ingresar su nombre real.")
            else:
                exito = registrar_nuevo_usuario(
                    diccionario_usuarios,
                    nuevo_user,
                    nueva_pass,
                    nombre_real,
                    rol="huesped"
                )
                if exito:
                    print(f"\n[Éxito] Cuenta creada con éxito para '{nuevo_user}'. Ya puede iniciar sesión.")

        elif opcion == "0":
            print("\nSaliendo de Room Master...")
            return None
        else:
            print("\nOpción inválida. Ingrese 1, 2 o 0.")

    return sesion_iniciada
