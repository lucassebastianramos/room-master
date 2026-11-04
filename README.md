<div align="center">

# 🏨 Room Master

### Sistema de Gestión Hotelera por Consola en Python

*Habitaciones en matriz, huéspedes en diccionarios, identidad en tuplas, unicidad con conjuntos,*
*reportes con programación funcional y triple persistencia en archivos (JSON, TXT y CSV).*
*Sin clases. Sin bases de datos.*

<br>

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Pruebas-10%2F10%20aprobadas-2EA44F?style=for-the-badge&logo=pytest&logoColor=white)
![Clases](https://img.shields.io/badge/Clases-0-8A2BE2?style=for-the-badge)
![Bases de datos](https://img.shields.io/badge/Bases%20de%20datos-0-8A2BE2?style=for-the-badge)
![UADE](https://img.shields.io/badge/UADE-2026-C8102E?style=for-the-badge)

**[📄 Documentación oficial (PDF)](Documentacion_Fase2.pdf)** ·
**[🚀 Inicio rápido](#-inicio-rápido)** ·
**[🏗️ Arquitectura](#️-arquitectura)** ·
**[🧪 Pruebas](#-pruebas-unitarias)** ·
**[🎓 Guía de defensa](#-conceptos-de-la-cátedra-y-dónde-encontrarlos)**

</div>

---

## 📑 Tabla de contenidos

1. [Sobre el proyecto](#-sobre-el-proyecto)
2. [Vista rápida](#-vista-rápida)
3. [Funcionalidades](#-funcionalidades)
4. [Inicio rápido](#-inicio-rápido)
5. [Uso del sistema](#️-uso-del-sistema)
6. [Arquitectura](#️-arquitectura)
7. [Modelo de datos](#-modelo-de-datos)
8. [Ciclo de vida de una habitación](#-ciclo-de-vida-de-una-habitación)
9. [Reglas de negocio](#-reglas-de-negocio)
10. [Triple persistencia](#-triple-persistencia)
11. [Manejo de excepciones](#️-manejo-de-excepciones)
12. [Pruebas unitarias](#-pruebas-unitarias)
13. [Conceptos de la cátedra y dónde encontrarlos](#-conceptos-de-la-cátedra-y-dónde-encontrarlos)
14. [Restricciones técnicas](#️-restricciones-técnicas)
15. [Hoja de ruta](#️-hoja-de-ruta)
16. [Flujo de trabajo en Git](#-flujo-de-trabajo-en-git)
17. [Equipo](#-equipo)

---

## 📌 Sobre el proyecto

**Room Master** es el Trabajo Práctico Integrador de **Algoritmos y Estructura de Datos 1 / Programación 1** (UADE, 2.º cuatrimestre 2026, cátedra del **Lic. Gustavo E. Escandell**).

Resuelve el día a día de la recepción de un hotel: saber qué habitaciones están libres, ocupadas o en limpieza; registrar el ingreso y la salida de huéspedes; mover a un huésped de habitación; cobrar según el piso y la duración de la estadía; auditar cobros en tiempo real; exportar reportes contables y ver indicadores de ocupación y recaudación. Todo queda guardado entre ejecuciones.

| Métrica | Valor |
| :--- | :--- |
| Módulos del sistema | **7** (`main`, `hotel`, `huespedes`, `tarifas`, `reportes`, `validaciones`, `archivos`) |
| Funciones del sistema | **45** (más 12 en `tests.py`) |
| Pruebas unitarias | **10 / 10 aprobadas** (4 válidas · 3 inválidas · 2 límite · 1 adicional) |
| Clases (`class`) | **0** |
| Dependencias externas para ejecutar | **0** (`pytest` es opcional y solo para correr las pruebas) |

---

## 👀 Vista rápida

```text
ROOM MASTER - MENÚ PRINCIPAL

1. Visualizar estado del hotel
2. Check-in (Nuevo huésped)
3. Check-out (Liberar habitación)
4. Reubicar huésped (Swap)
5. Búsquedas
6. Reportes y Facturación proyectada
7. Auditoría histórica de facturación (Desde archivo .TXT)
8. Exportar facturación a formato CSV (Archivo .CSV)
9. Redimensionar hotel
10. Restablecer habitación en limpieza
0. Salir
==============================
Seleccione una opción: 1

--- ESTADO ACTUAL DEL HOTEL ---
Estados: [L] Libre | [O] Ocupada | [S] Sucia

Piso 3:
[301: L]  [302: O]  [303: L]  [304: L]

Piso 2:
[201: O]  [202: S]  [203: L]  [204: O]

Piso 1:
[101: L]  [102: L]  [103: O]  [104: L]
```

```text
================ CHECK-OUT EXITOSO ================
Huésped:             Juan Perez
Habitación liberada: 201
TOTAL A COBRAR:      $108,000.00
===================================================
[Info] Factura registrada en el historial de facturación (.txt)
```

> Piso 2 configurado como *suite* con +20 % sobre una base de \$10.000 → \$12.000 por noche. 10 noches = \$120.000, menos 10 % por estadía larga = **\$108.000**. Comprobante añadido automáticamente a `facturacion.txt` en modo append `"a"`.

---

## ✨ Funcionalidades

<table>
<tr>
<td width="50%" valign="top">

**🛏️ Operación diaria**
- Grilla visual del hotel por piso con numeración comercial (`101`, `102`, …).
- **Check-in** con validación de habitación, nombre, DNI y días.
- **Check-out** con liquidación automática, pase a estado *Sucia* y guardado en bitácora TXT.
- **Reubicación (Swap)** de un huésped a otra habitación libre.
- **Restablecer habitación** de *Sucia* a *Libre* después de la limpieza.
- **Redimensionar** el hotel (con advertencia y opción de cancelar).

</td>
<td width="50%" valign="top">

**🔎 Búsquedas, reportes y auditoría**
- Por **DNI** (secuencial), por **nombre parcial** y por **habitación** (`filter` + `lambda`).
- **Ocupación**: total, ocupadas y porcentaje (`map` + `reduce`).
- **Habitaciones libres** por diferencia de conjuntos (`todas - ocupadas`).
- **Recaudación proyectada** (`map` + `reduce` sobre los huéspedes).
- **Auditoría histórica** desde `facturacion.txt` con acumulador contable.
- **Exportación CSV** estructurada con `csv.writer` para Excel o Google Sheets.

</td>
</tr>
<tr>
<td valign="top">

**💲 Tarifas**
- Precio base por noche configurable.
- Pisos *Suite / Lujo* opcionales con recargo porcentual.
- 10 % de descuento para estadías de más de 7 noches.

</td>
<td valign="top">

**🛡️ Robustez y persistencia**
- Validación con expresiones regulares en todas las entradas.
- Cancelación con `-1` en cualquier operación.
- DNI duplicado bloqueado con un `set` en tiempo constante $O(1)$.
- Triple persistencia desacoplada: JSON (estado), TXT (bitácora `"a"`), CSV (reportes).
- Manejo de excepciones en archivos con `try / except / else / finally`.

</td>
</tr>
</table>

---

## 🚀 Inicio rápido

**Requisitos:** Python 3.8 o superior (probado en Python 3.14). No hace falta instalar nada para usar el sistema.

```bash
# 1. Clonar el repositorio
git clone https://github.com/lucassebastianramos/room-master.git
cd room-master

# 2. Ejecutar el sistema
python main.py

# 3. Ejecutar las pruebas (sin instalar nada)
python tests.py

# 4. (Opcional) Ejecutar las pruebas con PyTest
python -m pip install pytest
python -m pytest tests.py -v
```

> [!TIP]
> En Windows, si `pytest` muestra *"no se reconoce como cmdlet"*, usá `python -m pytest`. Pasa porque `pip` instala el ejecutable en una carpeta que no está en el `PATH`.

---

## 🕹️ Uso del sistema

### Primer arranque

Si no existe `hotel_data.json`, el sistema pide la configuración inicial y la guarda:

1. Cantidad de **pisos** (1 a 99) y de **habitaciones por piso** (1 a 99).
2. **Precio base** por noche (mayor a 0).
3. Si el hotel tiene más de un piso: si querés **pisos de lujo**, desde qué piso y con qué recargo.

En los arranques siguientes, el hotel se **reconstruye solo** a partir del archivo.

### Menú principal

| Opción | Acción | Qué hace |
| :---: | :--- | :--- |
| `1` | Visualizar estado | Muestra la grilla del piso más alto al más bajo. Salto de línea cada 10 habitaciones. |
| `2` | Check-in | Pide habitación libre, nombre, DNI (no repetido) y días. Marca la habitación `O`. |
| `3` | Check-out | Busca por DNI, liquida monto, marca la habitación `S`, registra el cobro en `facturacion.txt` y libera el huésped. |
| `4` | Reubicar (Swap) | Mueve al huésped de una habitación a otra libre: origen `L`, destino `O`. |
| `5` | Búsquedas | Submenú interactivo: por DNI, por nombre parcial (`filter`+`lambda`) o por habitación. |
| `6` | Reportes proyectados | Ocupación global, habitaciones libres/ocupadas (conjuntos) y recaudación proyectada (`map`+`reduce`). |
| `7` | Auditoría histórica (.TXT) | Lee y procesa `facturacion.txt` secuencialmente mostrando cada comprobante y calculando el total histórico. |
| `8` | Exportar a CSV (.CSV) | Lee `facturacion.txt` y genera `facturacion.csv` mediante `csv.writer` para Microsoft Excel o Google Sheets. |
| `9` | Redimensionar hotel | Crea un hotel nuevo. ⚠️ Borra a los huéspedes y pide tarifas nuevas (con opción de cancelar). |
| `10` | Restablecer habitación | Pasa una habitación desocupada de `S` (limpieza) a `L` (libre). |
| `0` | Salir | Guarda los datos estructurales en JSON y finaliza la ejecución. |

> [!NOTE]
> **Cancelación universal:** en cualquier pedido de datos podés ingresar `-1` para volver atrás sin modificar el estado del hotel.

---

## 🏗️ Arquitectura

El programa principal **solo coordina**: muestra el menú, llama a las funciones de cada módulo y guarda después de cada operación. La lógica está repartida en módulos con una responsabilidad cada uno. El estado (matriz, huéspedes, tarifas) **viaja por parámetros**, no hay variables globales.

```mermaid
flowchart TD
    MAIN["main.py<br/>Menú y coordinación general"]

    HUE["huespedes.py<br/>Check-in · Check-out · Swap · Búsquedas"]
    REP["reportes.py<br/>map · filter · reduce · lambda · set"]
    ARC["archivos.py<br/>Persistencia JSON · Bitácora TXT · Exportación CSV"]
    HOT["hotel.py<br/>Matriz de habitaciones y coordenadas"]
    TAR["tarifas.py<br/>Precios y recargos por piso"]
    VAL["validaciones.py<br/>Regex, límites y control con -1"]

    MAIN --> HUE
    MAIN --> REP
    MAIN --> ARC
    MAIN --> HOT
    MAIN --> TAR
    MAIN --> VAL

    HUE --> HOT
    HUE --> TAR
    HUE --> REP
    HUE --> VAL
    HUE --> ARC
    REP --> TAR
    HOT --> VAL
    TAR --> VAL
```

| Módulo | Responsabilidad | Funciones | Biblioteca estándar |
| :--- | :--- | :---: | :--- |
| [`main.py`](main.py) | Menú principal (10 opciones), submenú de búsquedas, carga inicial y persistencia | 2 | — |
| [`hotel.py`](hotel.py) | Crear la matriz, convertir índices ↔ número comercial, mostrar la grilla, verificar disponibilidad | 9 | — |
| [`huespedes.py`](huespedes.py) | Check-in, check-out con facturación, swap, búsquedas funcionales, unicidad de DNI, limpieza | 14 | — |
| [`tarifas.py`](tarifas.py) | Configurar y consultar el precio por piso y recargos de lujo | 7 | — |
| [`reportes.py`](reportes.py) | Ocupación, subtotal con descuento, recaudación proyectada, habitaciones libres | 4 | `functools` |
| [`validaciones.py`](validaciones.py) | Patrones regex, validación genérica, rangos, confirmación s/n y cancelación `-1` | 3 | `re` |
| [`archivos.py`](archivos.py) | Persistencia JSON, auditoría TXT en modo `"a"` y exportación CSV con `csv.writer` | 6 | `json`, `csv` |
| [`tests.py`](tests.py) | 10 pruebas unitarias (PyTest y Python puro sin clases) | 12 | — |

<details>
<summary><b>📁 Estructura del repositorio</b></summary>

```text
room-master/
├── main.py                    # Punto de entrada: menú y coordinación (10 opciones)
├── hotel.py                   # Matriz de habitaciones y numeración comercial
├── huespedes.py               # Operaciones sobre huéspedes y enlace con facturación
├── tarifas.py                 # Esquema de precios por piso
├── reportes.py                # Reportes con programación funcional y conjuntos
├── validaciones.py            # Validaciones con expresiones regulares
├── archivos.py                # Persistencia JSON, auditoría TXT y exportación CSV
├── tests.py                   # Suite de 10 pruebas unitarias oficiales
├── Documentacion_Fase2.pdf    # Documento explicativo formal en PDF (Sección 15)
├── DOCUMENTACION_FASE2.md     # Mismo documento técnico, legible en GitHub
├── documentacion_fase2.html   # Fuente imprimible del PDF institucional
└── README.md
```

`hotel_data.json`, `facturacion.txt` y `facturacion.csv` se generan durante la ejecución del sistema y están protegidos en `.gitignore`.

</details>

---

## 🧬 Modelo de datos

Cada estructura se eligió por lo que tiene que hacer el dato, no para cumplir un requisito:

```python
# MATRIZ DEL HOTEL: lista de listas. hotel[piso][habitacion] da el estado en tiempo constante O(1).
hotel = [
    ["L", "O", "L", "L"],   # piso 1 → habitaciones 101..104
    ["O", "S", "L", "O"],   # piso 2 → habitaciones 201..204
]

# HUÉSPED: diccionario (acceso semántico por clave) que combina tupla inmutable y lista mutable.
huesped = {
    "identidad": ("40123456", "Juan Perez"),   # tupla: DNI y nombre no cambian nunca durante la estadía
    "dias": 10,                                # entero positivo
    "ubicacion": [1, 0, 201],                  # lista: cambia en el Swap [piso, hab, número comercial]
}

# TARIFAS: matriz [piso_comercial, precio_por_noche]
tarifas = [[1, 10000.0], [2, 12000.0]]

# CONJUNTOS: se arman dinámicamente para resolver consultas críticas
dnis_registrados = {"40123456", "38999111"}       # ¿el DNI ya existe? → O(1) promedio por hashing
libres = todas - ocupadas                         # ¿qué habitaciones quedan? → diferencia de conjuntos
```

---

## 🔄 Ciclo de vida de una habitación

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Libre : inicializar_hotel()
    Libre --> Ocupada : Check-in / Swap (destino)
    Ocupada --> Libre : Swap (origen)
    Ocupada --> Sucia : Check-out (registra en facturacion.txt)
    Sucia --> Libre : Restablecer habitación (opción 10)
```

El estado **Sucia (`S`)** impide volver a alquilar una habitación recién liberada hasta que el personal confirma el proceso sanitario de limpieza.

---

## 📐 Reglas de negocio

| Regla | Fórmula / criterio | Dónde |
| :--- | :--- | :--- |
| Número comercial | `(piso + 1) * 100 + (habitacion + 1)` → índices `(0, 0)` = **101** | `hotel.obtener_numero_comercial` |
| Número → índices | `piso = n // 100 - 1`, `habitacion = n % 100 - 1` | `hotel.obtener_indices_matriz` |
| Precio de un piso de lujo | `base × (1 + recargo / 100)`, redondeado a 2 decimales | `tarifas.generar_dict_tarifas` |
| Subtotal de estadía | `precio_noche × días` | `reportes.calcular_subtotal` |
| Descuento por estadía larga | `días > 7` → `subtotal × 0.9` (bonificación 10% con `lambda`) | `reportes.calcular_subtotal` |
| Dimensiones válidas | 1 a 99 pisos y 1 a 99 habitaciones por piso | `hotel.reiniciar_matriz` |
| DNI válido y único | 7 u 8 dígitos numéricos (`^\d{7,8}$`) y no registrado previamente | `validaciones` + `huespedes.validar_dni` |
| Nombre válido | solo letras (con tildes y eñes) y espacios | `validaciones.PATRON_TEXTO_VALIDO` |

---

## 💾 Triple persistencia

El sistema implementa tres niveles de persistencia independientes sin requerir bases de datos:

| Archivo | Formato | Qué guarda | Cuándo | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `hotel_data.json` | JSON | Dimensiones, tarifas y lista de huéspedes alojados | Al configurar, tras cada operación y al salir | ✅ Implementado |
| `facturacion.txt` | Texto plano | Una línea por check-out (`dni;nombre;monto`), apertura en modo `"a"` | En cada check-out | ✅ Implementado |
| `facturacion.csv` | CSV | Historial de facturación con encabezados (`DNI,Huesped,Monto_Cobrado`) para Excel / Sheets (`csv.writer`) | A pedido (opción 8), leyendo el `.txt` | ✅ Implementado |

### 1. Estado estructural en JSON (`hotel_data.json`)
```json
{
    "pisos": 2,
    "habitaciones": 4,
    "huespedes": [
        {
            "identidad": ["40123456", "Juan Perez"],
            "dias": 10,
            "ubicacion": [1, 0, 201]
        }
    ],
    "tarifas": [[1, 10000.0], [2, 12000.0]]
}
```
* **Recuperación:** al iniciar, `cargar_datos_hotel()` lee el JSON. Si existen registros, `main.py` reconstruye la matriz edilicia con `inicializar_hotel()` y asigna `"O"` a las coordenadas de cada huésped. Si no existe, lanza la configuración inicial sin errores.

### 2. Bitácora transaccional en Texto Plano (`facturacion.txt`)
* Cada Check-out invoca `registrar_factura_txt(dni, nombre, monto)` con modo agregado (`"a"`).
* Permite acumular comprobantes de forma permanente e inmediata sin necesidad de reescribir ni cargar todo el archivo en memoria.
* La opción 7 del menú (`leer_y_procesar_facturacion_txt`) procesa secuencialmente cada línea (`linea.split(";")`) y acumula la recaudación histórica real.

### 3. Exportación a Planillas de Cálculo (`facturacion.csv`)
* La opción 8 del menú (`exportar_facturacion_a_csv`) lee el archivo de texto y escribe un documento CSV con la librería estándar `csv` (`csv.writer`).
* Formato estandarizado:
```csv
DNI,Huesped,Monto_Cobrado
40123456,Juan Perez,108000.00
```
* Compatible con Microsoft Excel y Google Sheets para balances contables, tablas dinámicas y gráficos gerenciales.

---

## 🛡️ Manejo de excepciones

`try / except / else / finally` se utiliza con criterio técnico en situaciones donde el fallo **depende del entorno de archivos** y no del código. Las entradas de usuario se filtran **antes** con expresiones regulares:

| Situación | Excepción | Respuesta del sistema |
| :--- | :--- | :--- |
| Primera ejecución, no hay archivo | `FileNotFoundError` | Avisa cordialmente e inicia la configuración inicial |
| Sin permisos sobre el archivo | `PermissionError` | Informa la falta de permisos sin interrumpir el programa |
| JSON dañado o registros truncados | `ValueError` / `IndexError` | Informa que el archivo contiene registros incorrectos |
| Datos con tipos incompatibles con JSON | `TypeError` / `ValueError` | Informa el fallo de serialización y devuelve `guardado = False` |
| Error de E/S o disco lleno | `OSError` | Muestra el detalle del error del sistema operativo |
| Bloque de cierre de descriptores | `finally` | Ejecuta `archivo.close()` garantizando la liberación del recurso |

---

## 🧪 Pruebas unitarias

[`tests.py`](tests.py) cumple estrictamente con la distribución exigida por la **Sección 9**: 10 pruebas sobre **6 funciones distintas** de 4 módulos. Pueden ejecutarse sin abrir el programa principal.

| # | Tipo | Función probada | Situación evaluada | Esperado |
| :---: | :--- | :--- | :--- | :--- |
| 01 | ✅ Válido | `hotel.inicializar_hotel` | Hotel de 2 pisos × 3 habitaciones | Matriz 2×3 con `"L"` |
| 02 | ✅ Válido | `tarifas.obtener_tarifa_habitacion` | Precio del piso 2 configurado | `12000.0` |
| 03 | ✅ Válido | `reportes.calcular_subtotal` | 5 noches a \$10.000 (estadía corta) | `50000.0` |
| 04 | ✅ Válido | `reportes.calcular_subtotal` | 10 noches a \$10.000 (10% descuento con `lambda`) | `90000.0` |
| 05 | ❌ Inválido | Detección con `set` (lógica de `validar_dni`) | DNI que ya está en el conjunto registrado | `True` (duplicado) |
| 06 | ❌ Inválido | `hotel.habitacion_existe` | Consulta de piso 5 en hotel de 2×2 | `False` |
| 07 | ❌ Inválido | `huespedes.buscar_huesped_por_habitacion` | Habitación 999 sin huéspedes alojados | `[]` |
| 08 | ⚠️ Límite | `reportes.calcular_subtotal` | Exactamente 7 noches (frontera estricta sin descuento) | `70000.0` |
| 09 | ⚠️ Límite | `hotel.inicializar_hotel` | Hotel en dimensión mínima permitida ($1 \times 1$) | `[["L"]]` |
| 10 | ⭐ Adicional | `huespedes.buscar_huespedes_por_nombre` | Búsqueda parcial insensible a mayúsculas (`"juan"`) | `[Juan Perez, Juana Garcia]` |

```text
$ python -m pytest tests.py -v
tests.py::test_01_inicializacion_matriz_valida PASSED                    [ 10%]
...
tests.py::test_10_busqueda_parcial_nombre_filter_lambda PASSED           [100%]
============================= 10 passed in 0.08s ==============================
```

Con `python tests.py`, cada prueba imprime en consola los **5 puntos formales exigidos**: función, datos, resultado esperado, resultado obtenido y veredicto.

```text
Prueba [04] - CASO VÁLIDO
  1. Función:   reportes.calcular_subtotal
  2. Datos:     huesped={'dias': 10, 'piso': 0 (Piso 1)}, tarifa=$10000.0 (10% desc. > 7 días)
  3. Esperado:  90000.0
  4. Obtenido:  90000.0
  5. Resultado: [APROBADO]
```

---

## 🎓 Conceptos de la cátedra y dónde encontrarlos

Guía completa para la **defensa oral presencial**:

| Concepto | Dónde | Para qué se usa en el sistema |
| :--- | :--- | :--- |
| **Matrices** (listas anidadas) | `hotel.inicializar_hotel` | Representar la estructura física de pisos × habitaciones con acceso directo $O(1)$ |
| **Diccionarios** | `huespedes.realizar_checkin`, `archivos.guardar_datos_hotel` | Registro semántico de cada huésped y estructura raíz del archivo JSON |
| **Tuplas** | `"identidad": (dni, nombre)`, retornos de coordenadas | Datos inmutables de identificación legal y retornos múltiples empaquetados |
| **Conjuntos** | `huespedes.validar_dni`, `reportes.generar_reporte_ocupacion` | Control de unicidad de DNI en $O(1)$; cálculo algebraico de libres (`-`) y ocupadas (`&`) |
| **`lambda`** | `reportes.calcular_subtotal` | Regla concisa de descuento por estadía larga ($> 7$ noches) |
| **`filter`** | `huespedes.buscar_huespedes_por_nombre` / `_por_habitacion` | Búsquedas funcionales sin bucles explícitos sobre la lista de huéspedes |
| **`map`** | `reportes.calcular_recaudacion_total`, `generar_reporte_ocupacion` | Transformar huéspedes en montos y pisos en cantidades ocupadas |
| **`reduce`** | `reportes` (3 usos) | Acumular total de habitaciones, cantidad ocupada y recaudación proyectada |
| **Expresiones regulares** | `validaciones.py` | Validar formato estricto de DNI (`^\d{7,8}$`), nombres, números y días |
| **Excepciones** | `archivos.py` (6 funciones) | Control estructurado con `try / except / else / finally` en JSON, TXT y CSV |
| **Archivos JSON** | `archivos.py` + `main.py` | Guardar y recuperar el estado integral del hotel entre sesiones |
| **Archivos de texto (.txt)** | `archivos.py` (`facturacion.txt`) | Bitácora de auditoría en modo append `"a"`, lectura secuencial y acumulador |
| **Archivos CSV (.csv)** | `archivos.py` (`facturacion.csv`) | Exportación tabular con `csv.writer` para Microsoft Excel o Google Sheets |
| **Pruebas unitarias** | `tests.py` | Suite automatizada de 10 pruebas sobre 6 funciones sin utilizar clases |
| **Modularización** | 7 módulos | Separación rigurosa de responsabilidades; paso de parámetros sin variables globales |

---

## ⚖️ Restricciones técnicas

| Restricción (Sección 12) | Cumplimiento |
| :--- | :--- |
| 12.1 · Sin clases | ✅ No hay `class`, objetos propios, herencia, métodos de clase ni constructores. |
| 12.2 · Sin bases de datos | ✅ La persistencia se realiza exclusivamente mediante archivos (`.json`, `.txt` y `.csv`). |
| 12.3 · Solo librerías vistas en clase | ✅ `re`, `json`, `functools`, `csv` (estándar de Python). `pytest` autorizado por la cátedra para testing. |
| 12.4 · Código explicable | ✅ Sin decoradores, generadores, list comprehensions anidadas ni trucos fuera del programa. |

---

## 🗺️ Hoja de ruta

- [x] Modularización desacoplada en 7 módulos especializados
- [x] Huésped modelado como diccionario asociativo con tupla inmutable de identidad
- [x] Conjuntos hash para unicidad de DNI en $O(1)$ y álgebra de habitaciones libres
- [x] Persistencia y recuperación estructural en JSON (`hotel_data.json`)
- [x] Bitácora de auditoría continua en texto plano con modo append `"a"` (`facturacion.txt`)
- [x] Exportación formal a planillas de cálculo con `csv.writer` (`facturacion.csv`)
- [x] Manejo estructurado de excepciones con `try / except / else / finally` en todos los archivos
- [x] Suite de 10 pruebas unitarias con compatibilidad dual (Python nativo y PyTest)
- [x] Control universal de cancelación mediante `-1` y validaciones con Regex

---

## 🌿 Flujo de trabajo en Git

```mermaid
flowchart LR
    F["feature/nombre-de-rama<br/>rama de cada integrante"] -->|Pull Request| D["develop<br/>integración"]
    D -->|Pull Request| M["main<br/>versión estable"]
```

```bash
git checkout develop && git pull origin develop    # traer lo último
git checkout feature/mi-rama && git merge develop  # actualizar mi rama
git add . && git commit -m "feat: descripción del cambio"
git push origin feature/mi-rama                    # y abrir un Pull Request a develop
```

`main` está protegida: solo recibe cambios aprobados mediante Pull Request.

---

## 👥 Equipo

<div align="center">

| Integrante | Legajo | Rol |
| :--- | :---: | :--- |
| **Menendez Mojana, Tiara** | 1226578 | Referente del grupo |
| **Ramos, Lucas Sebastián** | 1235407 | Desarrollo |
| **Iglesias, Luca** | 1226578 | Desarrollo |
| **Rueda, Leandro Nicolás** | 1231246 | Desarrollo |

**Universidad Argentina de la Empresa (UADE)** · Algoritmos y Estructura de Datos 1 / Programación 1
Docente: **Lic. Gustavo E. Escandell** · 2.º cuatrimestre 2026

</div>
