# Room Master - Sistema de Gestión Hotelera 🏨

Sistema de control y gestión hotelera desarrollado por consola en Python para la materia **Programación 1 / Algoritmo y Estructura de Datos 1 (UADE)**.  
**Docente:** Lic. Gustavo E. Escandell  
**Entrega:** Modularización del Código por Archivos (Fase 2)

---

## 👥 Integrantes del Equipo
- **Menendez Mojana, Tiara** (Referente del grupo)
- **Ramos, Lucas Sebastián**
- **Iglesias, Luca**
- **Rueda, Leandro Nicolás**

---

## 🚀 Modularización del Proyecto

Para la Fase 2, el sistema ha sido reorganizado respetando la lógica acordada por el equipo, dividiendo el código en módulos temáticos desacoplados para mejorar la mantenibilidad, escalabilidad y trabajo colaborativo:

1. **`validaciones.py`**:
   - Centralización de expresiones regulares (`re`): validación de DNIs (7 u 8 dígitos numéricos), nombres (solo caracteres alfabéticos y espacios), enteros positivos y dimensiones.
   - Función `validar_generico` para asegurar entradas limpias con reintento automático.
   - Función `solicitar_dimension_valida` para dimensiones de la matriz del hotel.

2. **`hotel.py`**:
   - Inicialización de la matriz bidimensional del hotel con estado Libre (`[L]`).
   - Conversión de coordenadas entre índices de matriz `(piso, habitacion)` y número comercial `(piso + 1) * 100 + (habitacion + 1)` (ej: piso 0, hab 0 $\rightarrow$ 101).
   - Renderizado visual en consola con formato de grilla alineada.
   - Verificación de disponibilidad y prevención de bucles infinitos en hoteles completos.

3. **`tarifas.py`**:
   - Configuración dinámica de tarifas por piso.
   - Sobretasa para pisos superiores (habitaciones de lujo/suites).
   - Función `obtener_tarifa_habitacion` para consultar el precio por noche según el piso.

4. **`huespedes.py`**:
   - **Check-in (`realizar_checkin`):** Registro de nuevo huésped y ocupación de habitación (`[O]`).
   - **Estructura del registro:** Diccionario con tupla inmutable para identidad `{"identidad": (dni, nombre), "dias": n, "ubicacion": [p, h, num]}`.
   - **Validación DNI y unicidad (`validar_dni`, `dni_ya_registrado`):** Búsqueda y validación $O(1)$ con conjuntos (`set`).
   - **Búsqueda (`buscar_huesped_por_dni`):** Búsqueda secuencial exhaustiva por DNI.
   - **Búsqueda funcional (`buscar_huespedes_por_nombre`):** Uso de `filter` y `lambda` para aislar huéspedes por coincidencia parcial de nombre.
   - **Check-out (`realizar_checkout`):** Liberación de habitación, pase a estado Sucio (`[S]`) para limpieza y cálculo de liquidación.
   - **Reubicación / Swap (`reubicar_huesped_swap`):** Traslado de un huésped a una habitación libre y actualización de coordenadas.
   - **Restablecer limpieza (`restablecer_limpieza`):** Transición de habitación de estado Sucio (`[S]`) a Libre (`[L]`).

5. **`reportes.py`**:
   - **Reporte de ocupación (`generar_reporte_ocupacion`):** Conteo de habitaciones ocupadas y porcentaje global de ocupación utilizando `functools.reduce`.
   - **Cálculo de subtotal (`calcular_subtotal`):** Cálculo del costo de estadía con bonificación del 10% mediante función `lambda` para estadías superiores a 7 noches.
   - **Recaudación total (`calcular_recaudacion_total`):** Programación funcional pura mediante `map` y `functools.reduce` para proyectar los ingresos totales.
   - **Disponibilidad (`reporte_habitaciones_libres`):** Cálculo de habitaciones disponibles mediante operaciones de conjuntos (`set`).

6. **`main.py`**:
   - Punto de entrada principal con menú interactivo por consola (Opciones 1 a 8 y 0 para salir).
   - Importación y orquestación limpia de los módulos anteriores.

---

## 📁 Estructura de Archivos

```text
room-master/
│
├── main.py               # Menú principal y flujo de ejecución
├── hotel.py              # Gestión de matrices, renderizado y coordenadas
├── huespedes.py          # Check-in, Check-out, Swap, búsqueda y limpieza
├── tarifas.py            # Matriz y cálculo de tarifas por piso
├── reportes.py           # Programación funcional (map, filter, reduce, lambda)
├── validaciones.py       # Expresiones regulares y validación de entradas
│
├── tests.py              # Suite de pruebas unitarias con doctest (sin clases)
└── README.md             # Documentación del proyecto
```

---

## 🧪 Pruebas Unitarias Automatizadas (doctest - Sin Clases)

El archivo [tests.py](tests.py) y los módulos del proyecto implementan pruebas unitarias usando **`doctest`**, la biblioteca integrada en el estándar de Python, cumpliendo la restricción estricta de **no utilizar clases**:

1. **`prueba_01_inicializacion_matriz_hotel`**: Inicialización con dimensiones y estado `[L]`.
2. **`prueba_02_conversion_coordenadas_comerciales`**: Biyección matemática entre índices de matriz y números comerciales.
3. **`prueba_03_obtener_tarifa_habitacion`**: Obtención correcta de precios por noche según el piso.
4. **`prueba_04_calcular_subtotal_sin_descuento`**: Liquidación a tarifa plena (estadías $\le 7$ noches).
5. **`prueba_05_calcular_subtotal_con_descuento_larga_estadia`**: Bonificación del 10% con lambda ($> 7$ noches).
6. **`prueba_06_calcular_subtotal_casos_limites`**: Límite de 7 noches (sin descuento) y estadía de 0 noches.
7. **`prueba_07_validar_dni_con_conjunto_set`**: Validación de DNI único y detección de repetidos mediante conjuntos (`set`).
8. **`prueba_08_recaudacion_total_programacion_funcional`**: Cálculo acumulativo con `map` y `functools.reduce`.
9. **`prueba_09_buscar_huespedes_por_nombre_filter_lambda`**: Búsqueda funcional con `filter` y `lambda`.
10. **`prueba_10_mover_huesped_swap`**: Reubicación de huésped (Swap) y actualización de estados en la matriz.

### Para ejecutar las pruebas:

```bash
python tests.py
```

O para verificar cualquier módulo individual:

```bash
python hotel.py
python tarifas.py
python reportes.py
python huespedes.py
```

---

## 🌿 Flujo de Trabajo en Git

- `main`: Código final y estable.
- `develop`: Rama común de integración.
- `feature/<modulo>`: Ramas específicas de trabajo de cada integrante.

```bash
# 1. Traer la última versión de develop
git checkout develop
git pull origin develop

# 2. Cambiar a la rama de trabajo
git checkout feature/tu-rama
git merge develop

# 3. Subir avances
git add .
git commit -m "feat: descripcion del cambio"
git push origin feature/tu-rama
```
