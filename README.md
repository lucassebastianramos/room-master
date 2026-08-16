# Room Master - Sistema de Control Hotelero 🏨

Sistema de gestión hotelera por consola desarrollado en Python para la materia **Programación 1 / Algoritmo y Estructura de Datos 1 (UADE)**.

## 👥 Integrantes
- **Menendez Mojana, Tiara** (Referente del grupo)
- **Ramos, Lucas Sebastián**
- **Iglesias, Luca**
- **Rueda, Leandro Nicolás**

---

## 📌 Requisitos Técnicos del Proyecto
- **Estructuras Bidimensionales:** Matrices para el estado de pisos y habitaciones ("L", "O", "S", "M").
- **Listas Avanzadas:** Registros de huéspedes delimitados por strings.
- **Expresiones Regulares (`re`):** Validación estricta de DNI, email, teléfono y datos de entrada.
- **Programación Funcional:** Uso de funciones de orden superior (`map`, `filter`, `reduce`) junto con expresiones `lambda`.
- **Restricción Estricta:** Paradigma procedural/estructurado puro. Queda prohibido el uso de Clases (POO) o librerías externas no autorizadas.

---

## 🌿 Flujo de Trabajo en Git
- `main`: Rama de producción final y código testeado.
- `develop`: Rama de integración para el equipo.
- `feature/<nombre-tarea>`: Ramas individuales de cada integrante.

### Comandos para comenzar a trabajar:
```bash
# 1. Traer cambios y pararse en develop
git checkout develop
git pull origin develop

# 2. Crear tu rama de trabajo
git checkout -b feature/nombre-de-tu-modulo

# 3. Guardar cambios y subir tu rama
git add .
git commit -m "feat: descripcion del avance"
git push -u origin feature/nombre-de-tu-modulo
