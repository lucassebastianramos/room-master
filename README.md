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

## 🚀 Arquitectura Simplificada: Vista Única y Persistencia JSON

Siguiendo los requerimientos unificados del equipo de trabajo, el sistema cuenta con una arquitectura simplificada, desacoplada y directa:

1. **Vista Única de Administración:** Se eliminó la diferenciación por roles y pantallas de inicio de sesión (`auth.py`). El sistema arranca directamente en el panel de gestión integral con todas las operaciones del hotel disponibles.
2. **Ciclo Completo de Gestión Hotelera:**
   - **Alta (Check-in):** Asignación de habitación libre con confirmación previa y validación de DNI único mediante conjuntos (`set`).
   - **Baja (Check-out):** Liquidación con desglose de estadía, bonificación del 10% para estadías mayores a 7 noches, imputación de consumos adicionales (minibar/servicios) y liberación a estado de limpieza (`[S]`).
   - **Modificación:** Reubicación de habitación (**Swap**), carga de consumos extras y extensión de días de estadía sin reingresar datos.
   - **Consulta:** Búsqueda rápida de huésped por DNI mediante conjuntos (`set`) en tiempo $O(1)$ y filtrado funcional por piso mediante `filter` y `lambda`.
   - **Mantenimiento y Limpieza:** Estados de habitación `[L]` Libre, `[O]` Ocupada, `[S]` Sucia/Limpieza y `[M]` Mantenimiento/Fuera de servicio.
   - **Reportes Analíticos:** Desglose porcentual de ocupación y cálculo de facturación proyectada mediante programación funcional (`map`, `filter`, `functools.reduce` y `lambda`).
3. **Estructuras de Datos Nativas:**
   - **Tuplas (`tuple`):** Empleadas estrictamente para datos inmutables:
     - Identidad del huésped: `(dni, nombre)`
     - Configuración fija de habitación: `(piso, habitacion, num_comercial)`
     - Coordenadas de matriz: `(piso, habitacion)`
     - Estados válidos de habitación: `("L", "O", "S", "M")`
   - **Conjuntos (`set`):** Empleados para búsquedas en tiempo constante $O(1)$ y validación de unicidad:
     - Conjunto de DNIs activos: evita duplicados en check-in y acelera la búsqueda.
     - Conjunto de habitaciones ocupadas y por estado (`obtener_habitaciones_por_estado`).
     - Conjunto total de habitaciones para validación rápida.
4. **Persistencia en JSON:** Módulo `persistencia.py` que serializa y recupera el estado completo del hotel (`hotel`, `huespedes`, `tarifas`) en `datos/hotel_data.json` con reconstrucción explícita de tuplas inmutables y control robusto de excepciones (`FileNotFoundError`, `JSONDecodeError`, `OSError`).
5. **Restricciones Académicas:**
   - ❌ Sin Clases / POO en la lógica de negocio (diseño puramente modular y funcional).
   - ❌ Sin librerías externas: exclusivamente módulos estándar de Python (`re`, `functools`, `json`, `os`, `unittest`).

---

## 📁 Estructura Modular del Proyecto

```text
room-master/
│
├── main.py               # Punto de entrada y panel interactivo unificado de administración
├── hotel.py              # Matrices bidimensionales, conversión de coordenadas, estados (L, O, S, M) y sets
├── huespedes.py          # Check-in, Check-out con liquidación, Swap, extras, extensiones y búsqueda O(1)
├── tarifas.py            # Tarifas por piso y segmentación de suites de lujo
├── reportes.py           # Métricas analíticas y facturación (map, filter, reduce y lambdas)
├── persistencia.py       # Almacenamiento y recuperación en archivos JSON (datos/hotel_data.json)
├── validaciones.py       # Expresiones regulares genéricas y cancelación segura (0)
│
├── datos/
│   └── hotel_data.json   # Archivo de persistencia de datos del hotel
│
├── test_hotel.py         # Suite de 10 pruebas unitarias con unittest estándar
└── README.md             # Documentación integral del proyecto
```

---

## 🧪 Pruebas Unitarias Automatizadas

El proyecto incluye 10 pruebas unitarias automatizadas en [test_hotel.py](test_hotel.py) que validan:
1. Inicialización de matriz y estados `[L]`.
2. Biyección matemática y coordenadas inmutables en tuplas.
3. Expresiones regulares de validación (DNI, Nombres, Números).
4. Estructuras de datos: Tuplas inmutables y Conjuntos (`set`) para búsquedas $O(1)$.
5. Ciclo de mantenimiento y recuperación de habitaciones.
6. Cálculo de subtotal con bonificación funcional (10% en > 7 noches).
7. Consumos adicionales y liquidación de extras.
8. Recaudación total proyectada mediante `map` y `functools.reduce`.
9. Prevención de bucles infinitos ante hotel 100% completo.
10. Persistencia JSON: serialización, deserialización y restauración de tuplas inmutables.

Para ejecutar la suite de pruebas:
```bash
python -m unittest test_hotel.py -v
```

---

## 🌿 Flujo de Trabajo en Git

- `main`: Código final testeado y entregable.
- `develop`: Rama de integración común.
- `feature/fase2-<nombre>`: Ramas de trabajo del equipo.

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
