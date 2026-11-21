
# Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Fase 4 – Componente práctico: Prácticas simuladas**

## 1. Descripción del proyecto

El proyecto consiste en desarrollar un sistema de gestión para Software FJ, utilizando el lenguaje de programación Python y los principios de la programación orientada a objetos.

El sistema permite registrar clientes, administrar diferentes tipos de servicios, crear y confirmar reservas, calcular costos, cancelar reservas y registrar eventos y errores mediante un archivo de logs.

## 2. Objetivo

Desarrollar una aplicación que permita gestionar clientes, servicios y reservas mediante clases, objetos, herencia, encapsulamiento, abstracción y polimorfismo, aplicando también validaciones y manejo de excepciones.

## 3. Funcionalidades principales

- Registro y validación de clientes.
- Administración de servicios.
- Reserva de salas.
- Alquiler de equipos.
- Gestión de asesorías especializadas.
- Cálculo de costos con impuestos y descuentos.
- Confirmación y cancelación de reservas.
- Control de disponibilidad de servicios.
- Manejo de excepciones personalizadas.
- Registro de eventos y errores en un archivo de logs.
- Simulación de operaciones válidas e inválidas.

## 4. Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Contiene el gestor principal y la simulación de operaciones. |
| `modelos.py` | Contiene las clases de entidades, clientes, servicios y reservas. |
| `excepciones.py` | Define las excepciones personalizadas del sistema. |
| `logger.py` | Gestiona el registro de eventos y errores. |
| `README.md` | Contiene la documentación del proyecto. |

## 5. Conceptos de programación orientada a objetos aplicados

- **Abstracción:** mediante clases abstractas para definir estructuras generales.
- **Encapsulamiento:** mediante atributos protegidos y propiedades.
- **Herencia:** mediante clases especializadas que heredan de clases generales.
- **Polimorfismo:** mediante la implementación de métodos específicos para cada tipo de servicio.
- **Variantes de cálculo:** el cálculo de costos permite utilizar valores predeterminados o personalizados para impuestos y descuentos.

## 6. Manejo de excepciones y registros

El sistema utiliza excepciones personalizadas para controlar errores relacionados con datos inválidos, servicios no disponibles, operaciones no permitidas y cálculos inconsistentes.

Los eventos y errores se registran en el archivo:

`sistema_software_fj.log`

Este archivo se genera automáticamente durante la ejecución del programa.

## 7. Requisitos para ejecutar el proyecto

- Tener Python 3 instalado.
- Contar con los archivos del proyecto en una misma carpeta.
- Utilizar una terminal o un editor de código compatible con Python.

## 8. Ejecución del programa

Desde la terminal, ubicarse en la carpeta del proyecto y ejecutar el siguiente comando:

```bash
python main.py
```

El programa ejecutará una simulación de operaciones válidas e inválidas, mostrando los resultados en la terminal.

## 9. Resultados de la simulación

Durante las pruebas se verificó:

- Registro correcto de clientes.
- Rechazo de datos inválidos.
- Creación de diferentes tipos de servicios.
- Validación de disponibilidad.
- Confirmación de reservas.
- Rechazo de cálculos inconsistentes.
- Aplicación de impuestos y descuentos.
- Cancelación de reservas.
- Generación del archivo de registros.

## 10. Conclusión

El desarrollo del proyecto permitió aplicar los conceptos de programación orientada a objetos en una situación práctica de gestión de clientes, servicios y reservas. Además, se implementaron validaciones, excepciones personalizadas y registros de eventos para mejorar el control y funcionamiento del sistema.
