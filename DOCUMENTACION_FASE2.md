# Documento Explicativo y Técnico — Fase 2
## Sistema de Gestión Hotelera: Room Master

**Materia:** Algoritmos y Estructura de Datos 1 / Programación 1  
**Carrera:** Licenciatura en Gestión de Tecnología de la Información / Ingeniería en Informática  
**Institución:** Universidad Argentina de la Empresa (UADE) — Año: 2026  
**Docente Titular:** Lic. Gustavo E. Escandell  
**Fecha de Entrega:** 05/11/2026  
**Integrantes y Legajos:**
* **Menendez Mojana, Tiara** (Referente) — Legajo: 1226578
* **Ramos, Lucas Sebastián** — Legajo: 1235407
* **Iglesias, Luca** — Legajo: 1226578
* **Rueda, Leandro Nicolás** — Legajo: 1231246

---

## 1. Descripción de las Mejoras Respecto a la Primera Parte (Ítem a)

En esta segunda entrega, el sistema **Room Master** evolucionó desde un prototipo funcional monolítico basado en memoria volátil hacia una **arquitectura de software profesional, modularizada y desacoplada** estructurada en 7 archivos temáticos:

1. **Modularización Estricta:** División en módulos con responsabilidades únicas: `hotel.py`, `tarifas.py`, `huespedes.py`, `reportes.py`, `validaciones.py`, `archivos.py` y `main.py`. El archivo principal actúa exclusivamente como coordinador del flujo sin acumular lógica de negocio.
2. **Reubicación de Huéspedes (Swap):** Función interactiva para trasladar huéspedes entre habitaciones desocupadas, actualizando atómicamente la matriz física y el registro de ubicación en memoria. Se modularizó en subfunciones para validar viabilidad (`puede_reubicar`), capturar datos y ejecutar el movimiento.
3. **Ciclo Sanitario de Habitaciones:** Introducción del estado intermedio Sucio (`[S]`) tras el Check-out. Impide que una habitación desocupada vuelva automáticamente a estar disponible (`[L]`) sin una confirmación explícita de desinfección mediante la opción de restablecimiento.
4. **Búsquedas Funcionales Avanzadas:** Submenú con tres modalidades de localización: por DNI (búsqueda secuencial exhaustiva), por coincidencia parcial de nombre (utilizando `filter` y `lambda`, insensible a mayúsculas/minúsculas) y por número de habitación comercial.
5. **Esquema Tarifario Dinámico y Descuentos:** Parametrización de sobretasas para suites/pisos de lujo y liquidación automatizada con bonificación del 10% mediante expresiones `lambda` para estadías superiores a 7 noches. Las tarifas se almacenan como **diccionario `{piso: precio}`** para consulta en tiempo constante $O(1)$.
6. **Triple Persistencia Desacoplada:** Implementación integral de persistencia sin bases de datos mediante JSON (`hotel_data.json`), bitácora transaccional en texto plano con apertura append `"a"` (`facturacion.txt`) y exportación gerencial tabular (`facturacion.csv`).
7. **Control Universal de Cancelación:** Posibilidad de abortar cualquier operación ingresando `-1` en los pedidos de datos, evitando bloqueos por errores de digitación del usuario.
8. **Historial de Huésped:** Consulta de todas las estadías registradas de un huésped por DNI, leyendo directamente el archivo `facturacion.txt` (sin estructuras en memoria), con total histórico acumulado.
9. **Reporte Integrado de Ocupación:** El reporte de ocupación incorpora habitaciones libres/ocupadas y porcentaje en un único bloque, mostrando mensajes claros en lugar de conjuntos vacíos.

---

## 2. Estructuras de Datos y Justificación Técnica (Ítem b)

### 2.1. Conjuntos (`set`)
* **Ubicación en el sistema:**
  1. `huespedes.py` (función `validar_dni`): Control de unicidad de DNI.
  2. `reportes.py` (función `reporte_habitaciones_libres`): Cálculo algebraico de disponibilidad edilicia.
* **Justificación técnica:**
  * **Control de duplicados en $O(1)$:** En lugar de recorrer linealmente la lista de huéspedes con un bucle $O(n)$, se vuelcan los DNIs en una tabla hash (`set`), verificando la existencia (`dni in dnis`) en tiempo constante promedio.
  * **Álgebra de conjuntos:** Se modela el total de habitaciones y las habitaciones ocupadas como conjuntos. La disponibilidad se obtiene de forma directa mediante la **diferencia de conjuntos** (`libres = todas - ocupadas`) y la consistencia con la **intersección** (`comunes = todas & ocupadas`), evitando bucles anidados manuales.

### 2.2. Tuplas (`tuple`)
* **Ubicación en el sistema:** 
  1. `huespedes.py` (clave `"identidad"` del registro de huésped): Almacena la pareja inmutable `(DNI, Nombre)`.
  2. `hotel.py` (funciones `obtener_indices_matriz`, `solicitar_habitacion_libre`): Retorno múltiple empaquetado de coordenadas `(piso, habitacion)`.
  3. `huespedes.py` (función `pedir_habitacion_destino`): Retorno empaquetado del destino del swap `(piso, habitacion, numero)`.
* **Justificación técnica:** 
  * Las tuplas garantizan **inmutabilidad** e integridad referencial. El DNI y nombre constituyen datos de identificación legal que bajo ninguna circunstancia deben alterarse accidentalmente durante la estadía ni durante operaciones de Swap. Si un proceso intentara modificar `huesped["identidad"][0]`, el intérprete de Python lanzará un error protegiendo el dato.

### 2.3. Diccionarios (`dict`)
* **Ubicación en el sistema:** 
  1. `huespedes.py`: Cada huésped se representa como una entidad asociativa estructurada:
     ```python
     datos_huesped = {
         "identidad": (dni, nombre),      # Tupla inmutable
         "dias": dias,                    # Entero positivo
         "ubicacion": [piso, hab, num]    # Lista mutable (permite Swap)
     }
     ```
  2. `tarifas.py`: Esquema de precios por piso almacenado como **diccionario `{piso: precio}`**, permitiendo consulta en tiempo constante $O(1)$ sin recorrer listas.
  3. `archivos.py`: Estructura raíz serializada en JSON con claves `"pisos"`, `"habitaciones"`, `"huespedes"` y `"tarifas"`.
* **Justificación técnica:** 
  * Acceso asociativo por clave semántica en tiempo **$O(1)$** (ej: `huesped["dias"]` en lugar de `huesped[2]`), eliminando la fragilidad de índices posicionales rígidos que generaban fallos al modificar columnas en las listas de la Fase 1.

---

## 3. Persistencia de Datos (Ítem c)

En estricto cumplimiento de la consigna que prohíbe el uso de bases de datos (Sección 12.2), el sistema implementa un modelo de **triple persistencia desacoplada**:

| Tipo de Archivo | Formato | Nombre | Modo Apertura | Propósito en el Sistema |
| :--- | :---: | :--- | :---: | :--- |
| **JSON** | Estructurado | `hotel_data.json` | `'r'` / `'w'` | **Estado estructural del hotel:** Guarda dimensiones, tarifas por piso y la lista completa de diccionarios de huéspedes activos para reanudar el programa sin perder la ocupación. |
| **Texto Plano** | Secuencial | `facturacion.txt` | `'a'` (append) / `'r'` | **Bitácora de auditoría continua:** Registra cronológicamente cada comprobante de Check-out (`dni;nombre;habitacion;piso;dias;monto`) en tiempo real sin sobrescribir ni leer todo el archivo. |
| **CSV** | Tabular | `facturacion.csv` | `'w'` con `csv.writer` | **Exportación gerencial:** Transforma el historial del archivo `.txt` en filas y columnas estandarizadas con encabezados para planillas de cálculo (Microsoft Excel / Google Sheets). |

### Flujo Operativo de Persistencia y Recuperación:
1. **Inicio del sistema:** `main.py` invoca `inicializar_archivo_txt()` para asegurar la existencia del archivo de bitácora y `cargar_datos_hotel()` para deserializar `hotel_data.json`. Si el archivo existe, reconstruye automáticamente la matriz y asigna `"O"` a las coordenadas de cada huésped activo. Si no existe (`FileNotFoundError`), lanza la configuración inicial guiada.
2. **Check-out y facturación:** Cada Check-out exitoso invoca `registrar_factura_txt(dni, nombre, habitacion, piso, dias, monto)` en modo append `"a"`, asentando la transacción en disco inmediatamente con los 6 campos (DNI, nombre, habitación, piso, días, monto).
3. **Auditoría histórica (Opción 7):** `leer_y_procesar_facturacion_txt()` recorre secuencialmente `facturacion.txt`, parsea cada línea con `split(";")` y totaliza la recaudación acumulada histórica.
4. **Historial de Huésped (Opción 11):** `historial_huesped(dni)` lee `facturacion.txt` directamente y filtra por DNI, mostrando todas las estadías registradas y el total histórico, sin estructuras en memoria.
5. **Exportación a planilla (Opción 8):** `exportar_facturacion_a_csv()` procesa `facturacion.txt` y escribe `facturacion.csv` utilizando el módulo estándar `csv` (`csv.writer`) con los 6 campos.

---

## 4. Manejo Estructurado de Excepciones (Ítem d)

Se adoptó un criterio de ingeniería riguroso: **validar preventivamente las entradas del usuario con expresiones regulares y reservar bloques `try / except / else / finally` para contingencias del sistema de archivos y del entorno del sistema operativo**:

| Situación de Riesgo | Excepción Capturada | Módulo y Función | Tratamiento y Respuesta |
| :--- | :--- | :--- | :--- |
| Ausencia del archivo en la primera ejecución | `FileNotFoundError` | `archivos.py`<br>`cargar_datos_hotel`<br>`leer_y_procesar_facturacion_txt` | Informa que el archivo no existe, retorna estructura por defecto y permite continuar con la inicialización manual. |
| Restricciones de permisos del sistema operativo | `PermissionError` | `archivos.py`<br>(Todas las funciones de archivo) | Advierte claramente sobre la falta de permisos sin abortar abruptamente el sistema. |
| Archivo JSON dañado o registros truncados | `(ValueError, IndexError)`<br>`(ValueError, TypeError)` | `archivos.py`<br>`cargar_datos_hotel`<br>`guardar_datos_hotel` | `json.JSONDecodeError` hereda de `ValueError`. Se captura e informa que el archivo contiene registros incorrectos. |
| Fallas de disco, ruta o hardware | `OSError` | `archivos.py`<br>(Todas las funciones) | Captura general como clase padre para registrar el mensaje nativo del sistema operativo. |
| Cierre garantizado de descriptores de archivo | Bloque `finally` | `archivos.py`<br>(Todas las funciones) | Garantiza la ejecución de `archivo.close()` liberando el recurso de memoria aunque ocurra un error intermedio. |

---

## 5. Pruebas Unitarias Automatizadas (Ítem e)

La suite implementada en `tests.py` satisface el 100% de los requisitos formales de la **Sección 9**: 10 pruebas unitarias sobre **6 funciones diferentes**, desarrolladas mediante funciones puras y aserciones nativas `assert` (sin clases).

### Distribución Oficial de las 10 Pruebas:
* **4 Casos Válidos:**
  1. `test_01_inicializacion_matriz_valida`: Creación de matriz bidimensional con dimensiones correctas y estado `[L]`.
  2. `test_02_obtener_tarifa_piso_existente`: Consulta de tarifa correspondiente a un piso configurado.
  3. `test_03_calcular_subtotal_estadia_corta`: Liquidación a tarifa plena (estadías $\le 7$ noches, sin bonificación).
  4. `test_04_calcular_subtotal_estadia_larga_con_descuento`: Liquidación con 10% de descuento vía lambda ($> 7$ noches).
* **3 Casos Inválidos:**
  5. `test_05_deteccion_dni_duplicado_con_conjunto`: Detección en $O(1)$ de DNI ya registrado mediante conjuntos (`set`).
  6. `test_06_habitacion_inexistente_fuera_de_rango`: Detección de fallo al consultar coordenadas fuera de la matriz.
  7. `test_07_busqueda_huesped_habitacion_vacia`: Búsqueda en habitación sin huésped alojado (retorna lista vacía con `filter`).
* **2 Casos Límite:**
  8. `test_08_calcular_subtotal_limite_exacto_7_noches`: Frontera crítica de 7 noches para asegurar que no se aplique descuento indebido.
  9. `test_09_inicializacion_matriz_dimension_minima`: Matriz mínima permitida de $1 \times 1$.
* **1 Caso Adicional:**
  10. `test_10_busqueda_parcial_nombre_filter_lambda`: Búsqueda funcional por coincidencia parcial insensible a mayúsculas.

### Compatibilidad Dual de Ejecución:
* **Con Python nativo:** `python tests.py` (emite el reporte formal de los 5 puntos exigidos: Función, Datos, Esperado, Obtenido y Veredicto `[APROBADO]`).
* **Con PyTest:** `python -m pytest tests.py -v` (ejecución automática de pruebas, 10/10 passed en 0.06s sin warnings).

---

## 6. Cuadro Comparativo: Fase 1 vs. Fase 2 (Ítem f)

| Dimensión | Primera Entrega (Fase 1) | Segunda Entrega (Fase 2) |
| :--- | :--- | :--- |
| **Estructura del Proyecto** | Archivo monolítico | Arquitectura modular desacoplada en 7 módulos especializados |
| **Entidad Huésped** | Sublistas por posición `[nom, dni, dias, ...]` | Diccionario asociativo `dict` con tupla inmutable de identidad `tuple` |
| **Tarifas por Piso** | Lista de pares `[piso, precio]` | Diccionario `{piso: precio}` para consulta en $O(1)$ |
| **Control de Duplicados** | Búsqueda secuencial lineal $O(n)$ | Búsqueda en tiempo constante $O(1)$ mediante conjuntos `set` |
| **Disponibilidad de Habitaciones** | Recorrido manual con bucles anidados | Álgebra de conjuntos (operación diferencia `todas - ocupadas`) |
| **Persistencia de Datos** | Inexistente (datos volátiles en memoria RAM) | Triple persistencia: JSON (`hotel_data.json`), TXT (`facturacion.txt`) y CSV (`facturacion.csv`) |
| **Manejo de Errores** | Validaciones simples por consola | Excepciones estructuradas con bloques `try / except / else / finally` |
| **Pruebas de Software** | Verificación manual por teclado | Suite automatizada de 10 pruebas unitarias con aserciones nativas |
| **Paradigma** | Procedural básico | Programación funcional (`map`, `filter`, `functools.reduce`, `lambda`) sin clases |
| **Opciones de Menú** | 8 opciones básicas | 11 opciones coordinadas con auditoría TXT, exportación CSV e historial por DNI |

---

## 7. Cumplimiento de Restricciones Técnicas (Sección 12)

* ❌ **Cero Clases:** No se utiliza la palabra reservada `class`, objetos propios, constructores ni herencia.
* ❌ **Cero Bases de Datos:** No se emplean bases SQL, SQLite, NoSQL ni ORMs.
* ❌ **Cero Librerías No Vistas:** Solo se utilizan las librerías del estándar vistas en clase (`json`, `re`, `functools`, `csv`) y el runner de pruebas `pytest` autorizado por la cátedra.
* ❌ **Cero Código Complejo No Explicable:** El software está desarrollado bajo principios de legibilidad, modularidad y solidez conceptual para su defensa oral.
