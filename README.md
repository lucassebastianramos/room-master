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

## 🚀 Fase 2: Ampliación, Modularización y Persistencia

Habiendo completado satisfactoriamente la Fase 1, el proyecto evoluciona hacia una arquitectura modular robusta que incorpora los nuevos conceptos de la materia:

### 📌 Contenidos Obligatorios Incorporados:
1. **Modularización:** División del monolito en módulos con responsabilidades claras, parámetros y valores de retorno (sin variables globales descontroladas).
2. **Autenticación y Roles:** Sistema de inicio de sesión con roles diferenciados:
   - **Administrador:** Gestión total del hotel, tarifas, redimensionamiento, reportes y auditoría.
   - **Huésped / Usuario:** Consulta de habitaciones disponibles, reserva de habitación y consulta de estadía.
3. **Diccionarios (`dict`):** Gestión de usuarios, credenciales y roles (`auth.py`) y estructuración de datos para persistencia.
4. **Tuplas (`tuple`):** Representación inmutable de la sesión activa `(username, rol)` y coordenadas de habitación `(piso, hab)`.
5. **Conjuntos (`set`):** Control de unicidad de DNIs registrados y filtrado eficiente de estados de habitaciones.
6. **Manejo de Excepciones (`try / except`):** Control preventivo en carga/guardado de archivos (`FileNotFoundError`, `JSONDecodeError`), conversiones de datos y búsquedas seguras.
7. **Persistencia en JSON (`.json`):** Almacenamiento y recuperación completa del estado del hotel, tarifas, huéspedes y usuarios al iniciar/cerrar el sistema.
8. **Persistencia en Texto (`.txt`):** Registro de auditoría cronológica (`auditoria.txt`) con timestamp para cada check-in, check-out o swap.
9. **Pruebas Unitarias (`unittest`):** Suite automatizada de al menos 10 pruebas unitarias distribuidas en 5 funciones (casos válidos, inválidos, límite y dominio).
10. **Restricciones Técnicas Estrictas:**
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
