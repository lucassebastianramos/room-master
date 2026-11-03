# Documento Explicativo y Técnico - Fase 2
## Sistema de Gestión Hotelera: Room Master

**Materia:** Algoritmo y Estructura de Datos 1 / Programación 1  
**Carrera:** Licenciatura en Gestión de Tecnología de la Información / Ingeniería en Informática  
**Institución:** Universidad Argentina de la Empresa (UADE) — Año: 2026  
**Docente Titular:** Lic. Gustavo E. Escandell  
**Integrantes:**
* Menendez Mojana, Tiara (Referente)
* Ramos, Lucas Sebastián
* Iglesias, Luca
* Rueda, Leandro Nicolás

---

## 1. Descripción de las Mejoras Respecto a la Primera Parte (Ítem a)

En esta segunda etapa, el sistema evolucionó desde un prototipo monolítico elemental basado en listas anidadas hacia una **arquitectura de software profesional, modularizada y desacoplada** estructurada en 7 archivos temáticos:

1. **Modularización Estricta:** Descomposición funcional en `hotel.py`, `tarifas.py`, `huespedes.py`, `reportes.py`, `validaciones.py`, `archivos.py` y `main.py`.
2. **Reubicación de Huéspedes (Swap):** Implementación de la operación de traslado entre habitaciones libres actualizando matrices y listas en tiempo real.
3. **Restablecimiento y Ciclo de Limpieza:** Introducción del estado intermedio Sucio (`[S]`) tras el Check-out, obligando a una acción explícita de desinfección/limpieza para regresar a Libre (`[L]`).
4. **Búsquedas Avanzadas con Programación Funcional:** Incorporación de búsquedas secuenciales y filtrados avanzados con `filter` y expresiones `lambda` (por DNI, por coincidencia parcial de nombre y por número comercial de habitación).
5. **Esquema Tarifario Dinámico:** Configuración porcentual diferenciada de tarifas para pisos de suites/lujo y liquidación automática en Check-out con bonificación del 10% para estadías prolongadas.
6. **Validación Robusta de Entradas:** Centralización de expresiones regulares (`re`) con control de cancelación universal (`-1`).

---

## 2. Estructuras de Datos y Justificación Técnica (Ítem b)

### 2.1. Conjuntos (`set`)
* **Ubicación en el sistema:** 
  1. `huespedes.py` (función `validar_dni`): Control de duplicados en el registro de huéspedes.
  2. `reportes.py` (función `reporte_habitaciones_libres`): Cálculo de ocupación y disponibilidad.
* **Justificación técnica:** 
  * Los conjuntos están implementados en Python sobre **tablas hash**, lo que permite verificar la pertenencia de un elemento (`dni in dnis_registrados`) en tiempo constante promedio **$O(1)$**, a diferencia de una lista donde la búsqueda es secuencial $O(n)$.
  * Se aplica **álgebra de conjuntos**: la diferencia matemática (`habitaciones_totales - habitaciones_ocupadas`) determina de forma instantánea y sin bucles anidados las habitaciones libres del hotel, mientras que la intersección (`todas & ocupadas`) valida consistencia.

### 2.2. Tuplas (`tuple`)
* **Ubicación en el sistema:** 
  1. `huespedes.py` (clave `"identidad"` del registro de huésped): Almacena la pareja inmutable `(DNI, Nombre)`.
  2. `hotel.py` (funciones `obtener_indices_matriz`, `solicitar_habitacion_libre`): Retorno múltiple empaquetado de coordenadas `(piso, habitacion)`.
* **Justificación técnica:** 
  * Las tuplas garantizan **inmutabilidad** e integridad referencial. El DNI y nombre de un huésped constituyen datos de identidad legal que no deben sufrir modificaciones accidentales durante la estadía ni durante operaciones de Swap o traslados.

### 2.3. Diccionarios (`dict`)
* **Ubicación en el sistema:** 
  1. `huespedes.py`: Cada huésped se almacena como una estructura asociativa con claves semánticas descriptivas:
     ```python
     datos_huesped = {
         "identidad": (dni, nombre),      # Tupla inmutable
         "dias": dias,                    # Entero
         "ubicacion": [piso, hab, num]    # Lista mutable (permite Swap)
     }
     ```
  2. `archivos.py`: Diccionario raíz contenedor del estado del hotel para persistencia serializada.
* **Justificación técnica:** 
  * Acceso directo por clave en tiempo **$O(1)$** sin depender de índices posicionales rígidos (ej: `huesped["dias"]` en lugar de `huesped[2]`), lo que elimina errores de desplazamiento y mejora la legibilidad y mantenibilidad del código.

---

## 3. Persistencia de Datos (Ítem c)

El sistema implementa tres mecanismos complementarios de persistencia para satisfacer los requerimientos operativos y administrativos:

| Tipo de Archivo | Formato | Propósito en el Sistema | Modo de Apertura |
| :--- | :---: | :--- | :---: |
| **JSON** | `hotel_data.json` | **Copia de seguridad y estado estructural:** Guarda las dimensiones del hotel, la matriz de tarifas vigentes y la nómina completa de huéspedes activos para restaurar la sesión al reiniciar el programa. | `'r'` (lectura) / `'w'` (escritura) |
| **Texto Plano** | `operaciones.txt` | **Bitácora de auditoría continua:** Registra cronológicamente cada transacción de Check-out (fecha/hora simulada, huésped, habitación liberada, subtotal facturado y descuentos). | `'a'` (append) |
| **CSV** | `reporte_facturacion.csv` | **Exportación administrativa:** Estructura los cobros en filas y columnas separadas por comas para su apertura y análisis financiero en Microsoft Excel o Google Sheets. | `'w'` (escritura) con `csv.writer` |

### Flujo de Persistencia y Recuperación:
1. **Al iniciar el programa:** Se invoca `cargar_datos_hotel()` desde `archivos.py`. Si `hotel_data.json` existe, reconstruye la matriz, las tarifas y la lista de diccionarios de huéspedes sin necesidad de configuración manual inicial.
2. **Durante la operación diaria:** Cada Check-out realizado añade una línea a la bitácora `operaciones.txt` con modo de apertura `"a"` (append). Esta técnica permite registrar transacciones en tiempo real sin tener que reescribir ni cargar todo el historial previo en memoria RAM.
3. **Al solicitar exportación gerencial:** El sistema toma los registros acumulados y genera `reporte_facturacion.csv` utilizando la librería estándar `csv`, permitiendo al área contable realizar balances y gráficos externos.
4. **Al cerrar el sistema:** Se invoca `guardar_datos_hotel()` para serializar el estado íntegro actualizado en formato JSON estructurado con `indent=4`.

---

## 4. Manejo de Excepciones (Ítem d)

En cumplimiento de las pautas de la cátedra, el manejo de excepciones mediante bloques `try / except / else / finally` se aplica **exclusivamente ante situaciones de riesgo concreto de fallo en tiempo de ejecución**, evitando el uso indiscriminado de excepciones para controlar flujo lógico ordinario:

1. **Acceso y Manejo de Archivos (`archivos.py`):**
   * `FileNotFoundError`: Controla la ausencia del archivo `hotel_data.json` en la primera ejecución, inicializando el hotel en modo limpio sin detener el programa.
   * `PermissionError`: Captura intentos de lectura o escritura en directorios protegidos o bloqueados por el sistema operativo.
   * `json.JSONDecodeError` / `ValueError`: Controla casos donde el archivo JSON esté corrupto o contenga sintaxis inválida.
   * `finally`: Asegura el cierre obligatorio del descriptor de archivo (`archivo.close()`) en caso de no utilizar gestor de contexto `with`.
2. **Conversiones Numéricas e Interfaces de Entrada (`validaciones.py`):**
   * `ValueError`: Detección de ingresos no numéricos al solicitar dimensiones, días o tarifas.
3. **Límites de Búsqueda y Navegación:**
   * `IndexError`: Control de accesos a pisos o habitaciones que exceden el tamaño de la matriz bidimensional.

---

## 5. Pruebas Unitarias Automatizadas (Ítem e)

La suite implementada en [tests.py](tests.py) cumple con la totalidad de los requisitos de la **Sección 9**, ejecutándose de manera autónoma sin dependencias externas y **sin emplear clases**:

### Distribución Oficial de las 10 Pruebas:
* **4 Casos Válidos:**
  1. `test_01_inicializacion_matriz_valida`: Creación de matriz bidimensional con dimensiones correctas y estado `[L]`.
  2. `test_02_obtener_tarifa_piso_existente`: Consulta de tarifa correspondiente a un piso configurado.
  3. `test_03_calcular_subtotal_estadia_corta`: Liquidación a tarifa plena (estadias $\le 7$ noches, sin bonificación).
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
* **Con Python nativo:** `python tests.py` (emite el reporte formal de los 5 puntos: Función, Datos, Esperado, Obtenido y Veredicto).
* **Con PyTest:** `python -m pytest tests.py -v` (ejecución mediante aserciones nativas `assert`, 100% aprobadas).

---

## 6. Cuadro Comparativo: Fase 1 vs. Fase 2 (Ítem f)

| Dimensión | Primera Entrega (Fase 1) | Segunda Entrega (Fase 2) |
| :--- | :--- | :--- |
| **Estructura del Proyecto** | Archivo monolítico | Arquitectura modular desacoplada en 7 módulos especializados |
| **Entidad Huésped** | Sublistas por posición `[nom, dni, dias, ...]` | Diccionario asociativo `dict` con tupla inmutable de identidad `tuple` |
| **Control de Duplicados** | Búsqueda secuencial lineal $O(n)$ | Búsqueda en tiempo constante $O(1)$ mediante conjuntos `set` |
| **Disponibilidad de Habitaciones** | Recorrido manual con bucles anidados | Álgebra de conjuntos (operación diferencia `todas - ocupadas`) |
| **Persistencia** | Datos volátiles en memoria RAM | Triple persistencia: JSON (`hotel_data.json`), TXT (`operaciones.txt`) y CSV |
| **Manejo de Errores** | Validaciones simples por consola | Excepciones estructuradas con bloques `try / except / else / finally` |
| **Pruebas de Software** | Verificación manual por teclado | Suite automatizada de 10 pruebas unitarias con aserciones nativas |
| **Paradigma** | Procedural básico | Programación funcional (`map`, `filter`, `functools.reduce`, `lambda`) sin clases |
