# =============================================================================
# MÓDULO DE AUTENTICACIÓN Y CONTROL DE ROLES (auth.py)
# =============================================================================
# Responsabilidad: Gestión de seguridad, control de accesos por rol (RBAC),
# perfiles de usuarios en memoria (Diccionarios), sesiones activas (Tuplas),
# permisos por rol (Conjuntos) y gestión integral de usuarios por el administrador.
# =============================================================================

import re
from validaciones import (
    validar_generico_con_cancelacion,
    confirmar_accion,
    PATRON_DNI_VALIDO,
    PATRON_TEXTO_VALIDO,
    ERROR_DNI,
    ERROR_TEXTO
)

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
    "restablecer",
    "gestionar_usuarios",
    "gestionar_reglas"
}

PERMISOS_HUESPED = {
    "ver_hotel",
    "reservar",
    "consultar_estadia",
    "ver_tarifas"
}

# Base de datos inicial en memoria usando Diccionarios (dict)
USUARIOS_DEFAULT = {
    "admin": {
        "password": "admin",
        "rol": "admin",
        "nombre": "Administrador del Hotel",
        "dni": "11111111"
    },
    "recepcion": {
        "password": "1234",
        "rol": "admin",
        "nombre": "Recepcionista de Turno",
        "dni": "22222222"
    },
    "cliente": {
        "password": "1234",
        "rol": "huesped",
        "nombre": "Huésped Frecuente",
        "dni": "33333333"
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


def tiene_permiso(rol, permiso):
    """
    Determina si un rol posee autorización para ejecutar una acción específica.
    Consulta la pertenencia en el conjunto (set) de permisos correspondiente.
    """
    permisos = obtener_permisos_por_rol(rol)
    return permiso in permisos


def verificar_credenciales(diccionario_usuarios, username, password):
    """
    Verifica si el usuario y contraseña coinciden en el diccionario de usuarios.
    Utiliza manejo de excepciones (KeyError / TypeError) para acceso seguro.
    Retorna una Tupla (username, rol, nombre, dni) si es válido, o None si no coincide.
    """
    try:
        usuario_data = diccionario_usuarios[username]
        if usuario_data["password"] == password:
            # Retorna una Tupla inmutable que representa la sesión activa
            sesion = (
                username,
                usuario_data["rol"],
                usuario_data["nombre"],
                usuario_data.get("dni", "")
            )
            return sesion
        return None
    except KeyError:
        return None
    except TypeError:
        return None


def registrar_nuevo_usuario(diccionario_usuarios, username, password, nombre, dni="", rol="huesped"):
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

        diccionario_usuarios[username_limpio] = {
            "password": password.strip(),
            "rol": rol,
            "nombre": nombre.strip(),
            "dni": str(dni).strip()
        }
        return True
    except (AttributeError, TypeError) as error:
        print(f"Error al registrar usuario: formato de datos inválido ({error}).")
        return False


def listar_usuarios(diccionario_usuarios):
    """
    Muestra la lista de usuarios formateada en consola.
    """
    print("\n" + "=" * 65)
    print("                USUARIOS REGISTRADOS EN EL SISTEMA               ")
    print("=" * 65)
    print(f"{'Usuario':<14} | {'Rol':<9} | {'DNI':<10} | {'Nombre y Apellido'}")
    print("-" * 65)
    for user_key, datos in diccionario_usuarios.items():
        dni_mostrar = datos.get("dni", "N/A")
        print(f"{user_key:<14} | {datos['rol'].upper():<9} | {dni_mostrar:<10} | {datos['nombre']}")
    print("=" * 65)


def crear_usuario_por_admin(diccionario_usuarios):
    """
    Permite al administrador crear un nuevo usuario definiendo usuario,
    contraseña, nombre, DNI y asignándole el rol que desee ('admin' o 'huesped').
    """
    print("\n--- CREACIÓN DE NUEVO USUARIO (ADMIN) ---")
    nuevo_user = input("Nombre de usuario (o 0 para cancelar): ").strip().lower()
    if nuevo_user in ["0", "cancelar"]:
        print("[Operación cancelada] Regresando...")
        return

    if nuevo_user in diccionario_usuarios:
        print(f"Error: El usuario '{nuevo_user}' ya existe.")
        return

    if len(nuevo_user) < 3:
        print("Error: El usuario debe tener al menos 3 caracteres.")
        return

    nueva_pass = input("Contraseña (o 0 para cancelar): ").strip()
    if nueva_pass in ["0", "cancelar"]:
        print("[Operación cancelada] Regresando...")
        return

    if len(nueva_pass) < 3:
        print("Error: La contraseña debe tener al menos 3 caracteres.")
        return

    nombre = validar_generico_con_cancelacion("Nombre y Apellido (o 0 para cancelar): ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
    if nombre is None:
        return

    dni = validar_generico_con_cancelacion("DNI (o 0 para cancelar): ", PATRON_DNI_VALIDO, ERROR_DNI)
    if dni is None:
        return

    print("\nSeleccione el rol del usuario:")
    print("1. Administrador (admin)")
    print("2. Huésped / Cliente (huesped)")
    rol_opcion = input("Opción (1 o 2, o 0 para cancelar): ").strip()

    if rol_opcion == "1":
        rol_elegido = "admin"
    elif rol_opcion == "2":
        rol_elegido = "huesped"
    else:
        print("[Operación cancelada] No se seleccionó rol.")
        return

    print("\n=== RESUMEN DE USUARIO A CREAR ===")
    print(f"Usuario:  {nuevo_user}")
    print(f"Rol:      {rol_elegido.upper()}")
    print(f"Nombre:   {nombre}")
    print(f"DNI:      {dni}")
    print("==================================")

    if confirmar_accion("¿Confirma la creación del usuario? (s/n): "):
        exito = registrar_nuevo_usuario(diccionario_usuarios, nuevo_user, nueva_pass, nombre, dni, rol_elegido)
        if exito:
            print(f"\n[Éxito] Usuario '{nuevo_user}' creado exitosamente con rol [{rol_elegido.upper()}].")
    else:
        print("\n[Operación cancelada] No se creó el usuario.")


def modificar_rol_usuario(diccionario_usuarios, sesion_actual):
    """
    Permite al administrador cambiar el rol de un usuario existente.
    """
    admin_user = sesion_actual[0]
    print("\n--- MODIFICAR ROL DE USUARIO ---")
    listar_usuarios(diccionario_usuarios)

    usuario_target = input("\nIngrese el nombre de usuario a modificar (o 0 para cancelar): ").strip().lower()
    if usuario_target in ["0", "cancelar"]:
        print("[Operación cancelada] Regresando...")
        return

    if usuario_target not in diccionario_usuarios:
        print(f"Error: El usuario '{usuario_target}' no existe.")
        return

    if usuario_target == admin_user:
        print("Aviso: No puede modificar su propio rol de administrador activo.")
        return

    rol_actual = diccionario_usuarios[usuario_target]["rol"]
    nuevo_rol = "huesped" if rol_actual == "admin" else "admin"

    print(f"\nEl usuario '{usuario_target}' actualmente tiene rol [{rol_actual.upper()}].")
    print(f"Se cambiará su rol a: [{nuevo_rol.upper()}].")

    if confirmar_accion(f"¿Confirma el cambio de rol para '{usuario_target}'? (s/n): "):
        diccionario_usuarios[usuario_target]["rol"] = nuevo_rol
        print(f"\n[Éxito] El rol de '{usuario_target}' ahora es [{nuevo_rol.upper()}].")
    else:
        print("\n[Operación cancelada] No se modificó el rol.")


def eliminar_usuario(diccionario_usuarios, sesion_actual):
    """
    Permite al administrador dar de baja a un usuario del sistema.
    """
    admin_user = sesion_actual[0]
    print("\n--- ELIMINAR USUARIO DEL SISTEMA ---")
    usuario_target = input("Ingrese el nombre de usuario a eliminar (o 0 para cancelar): ").strip().lower()

    if usuario_target in ["0", "cancelar"]:
        print("[Operación cancelada] Regresando...")
        return

    if usuario_target not in diccionario_usuarios:
        print(f"Error: El usuario '{usuario_target}' no existe.")
        return

    if usuario_target == admin_user:
        print("Error: No puede eliminar su propia cuenta de administrador en sesión.")
        return

    if confirmar_accion(f"¿Está seguro de eliminar definitivamente a '{usuario_target}'? (s/n): "):
        del diccionario_usuarios[usuario_target]
        print(f"\n[Éxito] Usuario '{usuario_target}' eliminado del sistema.")
    else:
        print("\n[Operación cancelada] No se eliminó al usuario.")


def menu_gestion_usuarios(diccionario_usuarios, sesion_actual):
    """
    Submenú interactivo para la gestión completa de usuarios por parte del Administrador.
    """
    ejecutando = True
    while ejecutando:
        print("\n" + "=" * 50)
        print("         GESTIÓN DE USUARIOS Y ROLES (ADMIN)       ")
        print("=" * 50)
        print("1. Listar usuarios registrados")
        print("2. Crear nuevo usuario con rol (Admin/Huésped)")
        print("3. Cambiar rol de un usuario existente")
        print("4. Eliminar usuario")
        print("0. Volver al panel de administración")
        print("=" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_usuarios(diccionario_usuarios)
        elif opcion == "2":
            crear_usuario_por_admin(diccionario_usuarios)
        elif opcion == "3":
            modificar_rol_usuario(diccionario_usuarios, sesion_actual)
        elif opcion == "4":
            eliminar_usuario(diccionario_usuarios, sesion_actual)
        elif opcion == "0":
            ejecutando = False
        else:
            print("Opción inválida. Intente nuevamente.")

        if opcion != "0":
            input("\nPresione [Enter] para continuar...")


def flujo_login(diccionario_usuarios, reglas_negocio=None):
    """
    Gestiona la pantalla interactiva de inicio de sesión o registro.
    Respeta la política de autoregistro configurada por la administración.
    Retorna la Tupla de sesión (username, rol, nombre, dni) al loguearse con éxito,
    o None si el usuario decide salir del sistema.
    """
    sesion_iniciada = None

    while sesion_iniciada is None:
        permitir_autoregistro = True if reglas_negocio is None else reglas_negocio.get("permitir_autoregistro", True)

        print("\n" + "=" * 52)
        print("           ROOM MASTER - INICIO DE SESIÓN           ")
        print("=" * 52)
        print("1. Iniciar sesión con usuario existente")
        if permitir_autoregistro:
            print("2. Registrarse como nuevo huésped")
        else:
            print("2. Registrarse como nuevo huésped (SOLO RECEPCIÓN)")
        print("0. Salir de la aplicación")
        print("=" * 52)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- INGRESO DE CREDENCIALES ---")
            usuario = input("Usuario (o 0 para volver): ").strip().lower()
            if usuario in ["0", "cancelar"]:
                continue
            password = input("Contraseña: ").strip()

            sesion = verificar_credenciales(diccionario_usuarios, usuario, password)
            if sesion is not None:
                user, rol, nombre, dni = sesion
                print("\n==================================================")
                print(f"¡Bienvenido/a, {nombre}!")
                print(f"Sesión iniciada con rol: [{rol.upper()}]")
                print("==================================================")
                return sesion
            else:
                print("\n[Error] Usuario o contraseña incorrectos. Intente nuevamente.")

        elif opcion == "2":
            if not permitir_autoregistro:
                print("\n[Aviso] El autorregistro online se encuentra DESHABILITADO por la administración.")
                print("Este establecimiento opera bajo la modalidad de RECEPCIÓN EXCLUSIVA.")
                print("Por favor, acérquese a la ventanilla para que el personal de recepción registre su estadía.")
                continue

            print("\n--- REGISTRO DE NUEVO HUÉSPED ---")
            nuevo_user = input("Elija un nombre de usuario (o 0 para cancelar): ").strip().lower()
            if nuevo_user in ["0", "cancelar"]:
                continue

            nueva_pass = input("Elija su contraseña (mínimo 3 caracteres): ").strip()
            if not nueva_pass or len(nueva_pass) < 3:
                print("Error: La contraseña debe tener al menos 3 caracteres.")
                continue

            nombre_real = validar_generico_con_cancelacion("Ingrese su nombre y apellido: ", PATRON_TEXTO_VALIDO, ERROR_TEXTO)
            if nombre_real is None:
                continue

            dni_nuevo = validar_generico_con_cancelacion("Ingrese su DNI: ", PATRON_DNI_VALIDO, ERROR_DNI)
            if dni_nuevo is None:
                continue

            exito = registrar_nuevo_usuario(
                diccionario_usuarios,
                nuevo_user,
                nueva_pass,
                nombre_real,
                dni_nuevo,
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
