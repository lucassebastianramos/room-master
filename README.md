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
   - **Validación DNI y unicidad (`validar_dni`):** Búsqueda y validación de duplicados con conjuntos (`set`).
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
├── tests.py              # Suite de 10 pruebas unitarias automatizadas (compatible con PyTest)
└── README.md             # Documentación del proyecto
```

---

## 🧪 Pruebas Unitarias Automatizadas

El archivo [tests.py](tests.py) implementa la suite oficial de 10 pruebas unitarias exigidas para la Fase 2, estructuradas con funciones puras `def` y aserciones nativas (`assert`) **sin utilizar clases**, distribuidas en 4 categorías:

### 1. Casos Válidos (4 pruebas)
* **`test_01_inicializacion_matriz_valida`**: Inicialización correcta de la matriz con estado Libre (`[L]`).
* **`test_02_obtener_tarifa_piso_existente`**: Consulta exitosa de la tarifa configurada para un piso.
* **`test_03_calcular_subtotal_estadia_corta`**: Liquidación a tarifa plena para estadías cortas ($\le 7$ noches).
* **`test_04_calcular_subtotal_estadia_larga_con_descuento`**: Aplicación de la bonificación del 10% mediante función lambda ($> 7$ noches).

### 2. Casos Inválidos (3 pruebas)
* **`test_05_deteccion_dni_duplicado_con_conjunto`**: Detección de DNI repetido mediante conjuntos (`set`).
* **`test_06_habitacion_inexistente_fuera_de_rango`**: Validación de habitación en coordenadas fuera de rango en la matriz.
* **`test_07_busqueda_huesped_habitacion_vacia`**: Búsqueda en una habitación donde no hay ningún huésped alojado.

### 3. Casos Límite (2 pruebas)
* **`test_08_calcular_subtotal_limite_exacto_7_noches`**: Límite exacto de 7 noches (frontera donde aún no corresponde descuento).
* **`test_09_inicializacion_matriz_dimension_minima`**: Creación de matriz con dimensiones mínimas permitidas (hotel 1x1).

### 4. Caso Adicional Relevante (1 prueba)
* **`test_10_busqueda_parcial_nombre_filter_lambda`**: Búsqueda parcial de huéspedes por nombre con `filter` y `lambda`.

---

### 💻 Formas de Ejecución de las Pruebas

El archivo soporta **ejecución dual**:

#### Opción 1: Ejecución directa con Python estándar (Sin instalar nada)
Ejecuta la suite y muestra en consola el informe detallado con los 5 puntos exigidos en la Sección 9 (Función, Datos, Esperado, Obtenido y Veredicto):
```bash
python tests.py
```

#### Opción 2: Ejecución mediante PyTest
Aprovecha el autodescubrimiento y reportes de PyTest:
```bash
python -m pytest tests.py -v
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
