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
   - **Estructura del registro:** Sublista `[nombre, dni, dias, piso, habitacion, num_comercial]`.
   - **Búsqueda (`buscar_huesped_por_dni`):** Búsqueda secuencial exhaustiva por DNI.
   - **Filtro funcional (`filtrar_huespedes_por_piso`):** Uso de `filter` y `lambda` para aislar huéspedes alojados en un piso determinado.
   - **Check-out (`realizar_checkout`):** Liberación de habitación, pase a estado Sucio (`[S]`) para limpieza y cálculo de liquidación.
   - **Reubicación / Swap (`reubicar_huesped_swap`):** Traslado de un huésped a una habitación libre o intercambio de habitaciones entre huéspedes.
   - **Restablecer limpieza (`restablecer_limpieza`):** Transición de habitación de estado Sucio (`[S]`) a Libre (`[L]`).

5. **`reportes.py`**:
   - **Reporte de ocupación (`generar_reporte_ocupacion`):** Conteo de habitaciones ocupadas y porcentaje global de ocupación utilizando `functools.reduce`.
   - **Cálculo de subtotal (`calcular_subtotal`):** Cálculo del costo de estadía con bonificación del 10% mediante función `lambda` para estadías superiores a 7 noches.
   - **Recaudación total (`calcular_recaudacion_total`):** Programación funcional pura mediante `map` y `functools.reduce` para proyectar los ingresos totales.

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
├── test_hotel.py         # Suite de 10 pruebas unitarias automatizadas
└── README.md             # Documentación del proyecto
```

---

## 🧪 Pruebas Unitarias Automatizadas

El archivo [test_hotel.py](test_hotel.py) implementa una suite de 10 pruebas con el módulo estándar `unittest` de Python, asegurando el correcto funcionamiento de cada componente:

1. **`test_01_inicializacion_matriz_hotel`**: Inicialización con dimensiones y estado `[L]`.
2. **`test_02_conversion_coordenadas_comerciales`**: Biyección matemática entre índices de matriz y números comerciales.
3. **`test_03_validaciones_expresiones_regulares`**: Regex de DNI, texto, números enteros y días.
4. **`test_04_obtener_tarifa_habitacion`**: Obtención correcta de precios por noche por piso.
5. **`test_05_registro_huesped_formato`**: Estructura de sublista `[nombre, dni, dias, piso, hab, num]`.
6. **`test_06_calculo_subtotal_estadia_corta`**: Liquidación a tarifa plena (estadias $\le 7$ noches).
7. **`test_07_calculo_subtotal_con_descuento_larga_estadia`**: Bonificación del 10% con lambda ($> 7$ noches).
8. **`test_08_recaudacion_total_programacion_funcional`**: Cálculo acumulativo con `map` y `functools.reduce`.
9. **`test_09_filtrar_huespedes_por_piso`**: Filtrado funcional de huéspedes por piso con `filter` y `lambda`.
10. **`test_10_restablecer_limpieza_habitacion`**: Transición de estado `[S]` a `[L]`.

Para ejecutar las pruebas:
```bash
python -m unittest test_hotel.py -v
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
