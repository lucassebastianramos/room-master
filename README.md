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
| **`admin`** | `admin` | `admin` | Administrador del Hotel | `11111111` | Acceso irrestricto: gestión de usuarios y roles, reglas de negocio (oferta/demanda), redimensionamiento y reportes. |
| **`recepcion`** | `1234` | `admin` | Recepcionista de Turno | `22222222` | Operaciones hoteleras: Check-in, Check-out, Swap, restablecer limpieza y facturación. |
| **`cliente`** | `1234` | `huesped` | Huésped Frecuente | `33333333` | Portal del huésped: ver disponibilidad, reservar habitación (titular o terceros) y consultar estadía. |

> **Nota:** También es posible crear nuevos usuarios con roles diferenciados desde el Panel de Administración o registrarse libremente como huésped desde la pantalla de inicio de sesión.

---

## 🚀 Fase 2: Ampliación, Modularización y Persistencia

Habiendo completado satisfactoriamente la Fase 1, el proyecto evoluciona hacia una arquitectura modular robusta que incorpora los nuevos conceptos de la materia:

### 📌 Contenidos y Reglas de Negocio Incorporados:
1. **Modularización:** División del monolito en módulos con responsabilidades claras, parámetros y valores de retorno (sin variables globales descontroladas).
2. **Autenticación y Roles:** Sistema de inicio de sesión con roles diferenciados:
   - **Administrador:** Gestión total del hotel, tarifas, reglas de negocio, redimensionamiento, reportes y auditoría.
   - **Huésped / Usuario:** Consulta de disponibilidad, reserva de habitación (propia o terceros) y consulta de estadía.
3. **Modos Operativos del Hotel:** Configuración de modo Híbrido (portal online abierto) o Modo Recepción Exclusiva (solo mostrador registra).
4. **Estados de Habitación Ampliados:** Matriz con estados `[L]` Libre, `[O]` Ocupada, `[S]` Sucia/Limpieza y `[M]` Mantenimiento/Fuera de servicio.
5. **Cargos Extras y Extensión de Estadía:** Carga de consumos adicionales (Minibar, Cochera, Servicios) y posibilidad de extender noches sin reingresar.
6. **Diccionarios (`dict`):** Gestión de usuarios, credenciales y perfiles (`auth.py`) y reglas de negocio configurables (`tarifas.py`).
7. **Tuplas (`tuple`):** Representación inmutable de la sesión activa `(username, rol, nombre, dni)` y coordenadas de habitación `(piso, hab)`.
8. **Conjuntos (`set`):** Control de pertenencia de permisos por rol (`PERMISOS_ADMIN`, `PERMISOS_HUESPED`).
9. **Manejo de Excepciones (`try / except`):** Control preventivo en acceso a diccionarios, conversiones de datos y búsquedas seguras.
10. **Persistencia en JSON (`.json`) y Texto (`.txt`):** Estado general en JSON y bitácora cronológica con timestamps en `auditoria.txt`.
11. **Pruebas Unitarias (`unittest`):** Suite automatizada de pruebas unitarias distribuidas en funciones críticas.
12. **Restricciones Técnicas Estrictas:**
    - ❌ Prohibido el uso de Clases / Programación Orientada a Objetos (POO).
    - ❌ Prohibido el uso de bases de datos (SQL, etc.).
    - ❌ Prohibido el uso de librerías externas no vistas en la materia (únicamente librerías estándar: `re`, `json`, `functools`, `unittest`, `datetime`).

---

## 📁 Estructura Modular del Proyecto

```text
room-master/
│
├── main.py               # Punto de entrada: inicialización, login y menú según rol
├── auth.py               # Módulo de usuarios, contraseñas y roles (Dicts y Tuplas)
├── hotel.py              # Matriz de habitaciones, visualización y control de hotel lleno
├── tarifas.py            # Matriz de tarifas por piso y segmentación de suites
├── huespedes.py          # Check-in, Check-out, búsquedas secuenciales y Swap
├── reportes.py           # Reportes de ocupación y facturación (map, filter, reduce)
├── persistencia.py       # Carga y guardado en JSON y logs en TXT (try/except)
├── validaciones.py       # Expresiones regulares genéricas y validación de entradas
│
├── test_hotel.py         # Suite de 10 pruebas unitarias con unittest
├── datos/                # Directorio de persistencia
│   ├── hotel_data.json   # Archivo JSON con la información del hotel
│   └── auditoria.txt     # Archivo TXT con la bitácora de transacciones
└── README.md             # Documentación del proyecto
```

---

## 🌿 Flujo de Trabajo en Git (Fase 2)

- `main`: Código final testeado y entregable.
- `develop`: Rama de integración donde se unen las características de la Fase 2.
- `feature/fase2-<nombre>`: Ramas de trabajo asignadas a cada integrante.

### 📋 Asignación de Ramas por Integrante:
| Integrante | Rama Asignada | Responsabilidades Principales |
| :--- | :--- | :--- |
| **Lucas** | `feature/fase2-auth-roles` | `auth.py`: Login, diccionarios de usuarios, tuplas de sesión, bifurcación de menús (Admin/Huésped). |
| **Tiara** | `feature/fase2-hotel-disponibilidad` | `hotel.py` y `validaciones.py`: Desacople de matriz, solución del bucle infinito ante hotel lleno y cancelación con 0. |
| **Luca** | `feature/fase2-operaciones-txt` | `huespedes.py`: Check-in, check-out, swap y escritura de bitácora en `auditoria.txt`. |
| **Leandro** | `feature/fase2-persistencia-json-tests` | `persistencia.py`: Carga y guardado de `hotel_data.json` con `try/except`, y suite `test_hotel.py` con `unittest`. |

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
