# Room Master - Sistema de Gestión Hotelera 🏨

Sistema de control y gestión hotelera desarrollado por consola en Python para la materia **Programación 1 / Algoritmo y Estructura de Datos 1 (UADE)**.  
**Docente:** Lic. Gustavo E. Escandell  
**Fecha de entrega Fase 2:** 05/11/2026  

---

## 👥 Integrantes del Equipo
- **Menendez Mojana, Tiara** (Referente del grupo)
- **Ramos, Lucas Sebastián**
- **Iglesias, Luca**
- **Rueda, Leandro Nicolás**

---

## 🔑 Usuarios y Credenciales por Defecto

Para probar el sistema y evaluar los roles de acceso (RBAC), se dispone de los siguientes usuarios preconfigurados:

| Usuario | Contraseña | Rol | Nombre y Apellido | DNI | Alcance y Permisos |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`admin`** | `admin` | `admin` | Administrador del Hotel | `11111111` | Acceso irrestricto: gestión de usuarios y roles, reglas de negocio (oferta/demanda), redimensionamiento de matriz, tarifas y reportes. |
| **`recepcion`** | `1234` | `recepcion` | Recepcionista de Turno | `22222222` | Operaciones hoteleras en mostrador: Check-in, Check-out con liquidación y consumos extras, Swap, extensión de noches, limpieza [S], mantenimiento [M] y reportes (sin redimensionar ni alterar reglas de negocio). |
| **`cliente`** | `1234` | `huesped` | Huésped Frecuente | `33333333` | Portal de autoservicio: ver disponibilidad, reservar habitación online (titular o terceros), extender estadía y consultar estadía por DNI. |

> **Nota:** También es posible crear nuevos usuarios con roles diferenciados desde el Panel de Administración o registrarse libremente como huésped desde la pantalla de inicio de sesión (cuando el modo online está activo).

---

## 🚀 Fase 2: Modularización, RBAC y Arquitectura en Memoria

Habiendo completado satisfactoriamente la Fase 1, el proyecto evoluciona hacia una arquitectura modular robusta que incorpora los nuevos conceptos de la materia:

### 📌 Contenidos y Reglas de Negocio Incorporados:
1. **Modularización:** División del monolito en 6 módulos cohesivos con responsabilidades claras, parámetros y valores de retorno (sin variables globales descontroladas).
2. **Autenticación y Roles (RBAC):** Sistema de control de accesos con tres roles estrictamente diferenciados:
   - **Administrador (`admin`):** Gestión total del hotel, tarifas, reglas de negocio, redimensionamiento, reportes ejecutivos y administración de cuentas.
   - **Recepción (`recepcion`):** Personal de mostrador. Gestión operativa del ciclo del huésped (Check-in, Check-out con liquidación, Swap, consumos extras, extensión, mantenimiento y reportes) respetando el Principio de Menor Privilegio.
   - **Huésped / Usuario (`huesped`):** Portal de cliente: consulta de disponibilidad, reserva de habitación (propia o terceros) y consulta de estadía.
3. **Modos Operativos del Hotel:** Configuración de modo Híbrido (portal online abierto) o Modo Recepción Exclusiva (solo mostrador registra).
4. **Estados de Habitación Ampliados:** Matriz con estados `[L]` Libre, `[O]` Ocupada, `[S]` Sucia/Limpieza y `[M]` Mantenimiento/Fuera de servicio.
5. **Cargos Extras y Extensión de Estadía:** Carga de consumos adicionales (Minibar, Cochera, Servicios) y posibilidad de extender noches sin reingresar.
6. **Diccionarios (`dict`):** Gestión de usuarios, credenciales y perfiles (`auth.py`) y reglas de negocio configurables (`tarifas.py`).
7. **Tuplas (`tuple`):** Representación inmutable de la sesión activa `(username, rol, nombre, dni)` y coordenadas de habitación `(piso, hab)`.
8. **Conjuntos (`set`):** Control de pertenencia de permisos por rol (`PERMISOS_ADMIN`, `PERMISOS_RECEPCION`, `PERMISOS_HUESPED`).
9. **Manejo de Excepciones (`try / except`):** Control preventivo en acceso a diccionarios, conversiones de datos y búsquedas seguras.
10. **Almacenamiento Estricto en Memoria (RAM):** Cumplimiento total de la restricción académica: todo el estado se mantiene exclusivamente en estructuras nativas de memoria (sin persistencia en archivos externos ni bases de datos).
11. **Pruebas Unitarias (`unittest`):** Suite automatizada de 10 pruebas unitarias distribuidas en funciones críticas (`test_hotel.py`).
12. **Restricciones Técnicas Estrictas:**
    - ❌ Prohibido el uso de Clases / Programación Orientada a Objetos (POO) en la lógica de negocio.
    - ❌ Prohibido el uso de persistencia de datos o bases de datos (SQL, etc.): todo en memoria RAM.
    - ❌ Prohibido el uso de librerías externas no vistas en la materia (únicamente librerías estándar: `re`, `functools`, `unittest`).

---

## 📁 Estructura Modular del Proyecto

```text
room-master/
│
├── main.py               # Punto de entrada: inicialización, login y menús según rol (Admin/Recepción/Huésped)
├── auth.py               # Módulo de usuarios, contraseñas y roles RBAC (Dicts, Tuplas y Conjuntos)
├── hotel.py              # Matriz de habitaciones, visualización, estados (L, O, S, M) y control anti-bucle
├── tarifas.py            # Matriz de tarifas por piso, suites de lujo, precios dinámicos y reglas
├── huespedes.py          # Check-in, Check-out con liquidación, consumos extras, extensión y Swap
├── reportes.py           # Reportes de ocupación y facturación (map, filter, reduce y lambdas)
├── validaciones.py       # Expresiones regulares genéricas y validación con cancelación segura (0)
│
├── test_hotel.py         # Suite de 10 pruebas unitarias con unittest estándar
└── README.md             # Documentación integral del proyecto
```

---

## 🌿 Flujo de Trabajo en Git (Fase 2)

- `main`: Código final testeado y entregable.
- `develop`: Rama de integración donde se unen las características de la Fase 2.
- `feature/fase2-<nombre>`: Ramas de trabajo asignadas a cada integrante.

### 📋 Asignación de Ramas por Integrante:
| Integrante | Rama Asignada | Responsabilidades Principales |
| :--- | :--- | :--- |
| **Lucas** | `feature/fase2-auth-roles` | `auth.py`: Login, diccionarios de usuarios, tuplas de sesión, modelo RBAC (Admin/Recepción/Huésped). |
| **Tiara** | `feature/fase2-hotel-disponibilidad` | `hotel.py` y `validaciones.py`: Desacople de matriz, solución del bucle infinito ante hotel lleno y cancelación con 0. |
| **Luca** | `feature/fase2-operaciones-txt` | `huespedes.py`: Check-in, check-out con liquidación, consumos extras, extensión y swap. |
| **Leandro** | `feature/fase2-persistencia-json-tests` | `tarifas.py`, `reportes.py` y suite `test_hotel.py` con `unittest`. |

---

### 💻 Guía Rápida para el Equipo:

```bash
# 1. Asegurarse de traer todos los cambios de develop
git checkout develop
git pull origin develop

# 2. Cambiarse a tu rama asignada
git checkout feature/fase2-tu-rama
git pull origin feature/fase2-tu-rama

# 3. Trabajar en tu módulo, guardar cambios y subir a GitHub
git add .
git commit -m "feat(fase2): descripcion del avance"
git push origin feature/fase2-tu-rama

# 4. Crear Pull Request hacia 'develop' para revisión y aprobación
```
