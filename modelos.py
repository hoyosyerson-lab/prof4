
from abc import ABC, abstractmethod
import math

from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError
)


# 1. Clase abstracta para las entidades generales
class EntidadBase(ABC):

    def __init__(self, id_entidad: str):
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise DatoInvalidoError(
                "El ID debe ser una cadena de texto no vacía."
            )

        self._id = id_entidad.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def validar_datos(self):
        pass


# 2. Clase Cliente
class Cliente(EntidadBase):

    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.validar_datos()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(
                "El nombre debe tener al menos 3 caracteres."
            )
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise DatoInvalidoError("El correo debe ser texto.")

        valor = valor.strip()

        if (
            not valor
            or valor.count("@") != 1
            or " " in valor
            or "." not in valor.split("@")[1]
            or valor.startswith("@")
            or valor.endswith("@")
        ):
            raise DatoInvalidoError(
                f"El correo '{valor}' no tiene un formato válido."
            )

        self._correo = valor

    def validar_datos(self):
        if not self._id or not self._nombre or not self._correo:
            raise DatoInvalidoError(
                "Todos los datos del cliente son obligatorios."
            )


# 3. Clase abstracta Servicio
class Servicio(EntidadBase, ABC):

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True
    ):
        super().__init__(id_servicio)

        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        self.validar_datos()

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise DatoInvalidoError(
                "La disponibilidad debe ser True o False."
            )
        self._disponible = estado

    def validar_datos(self):
        if not isinstance(self._nombre, str) or len(self._nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio es inválido.")

        if (
            isinstance(self._tarifa_base, bool)
            or not isinstance(self._tarifa_base, (int, float))
            or not math.isfinite(self._tarifa_base)
            or self._tarifa_base <= 0
        ):
            raise DatoInvalidoError(
                "La tarifa base debe ser un número mayor a cero."
            )

        if not isinstance(self._disponible, bool):
            raise DatoInvalidoError(
                "La disponibilidad debe ser True o False."
            )

        self._nombre = self._nombre.strip()

    def validar_parametros_calculo(self, duracion, impuesto, descuento):
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, int)
            or duracion <= 0
        ):
            raise DatoInvalidoError(
                "La duración debe ser un número entero mayor a cero."
            )

        for valor, nombre in (
            (impuesto, "impuesto"),
            (descuento, "descuento")
        ):
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not math.isfinite(valor)
                or valor < 0
            ):
                raise DatoInvalidoError(
                    f"El valor del {nombre} debe ser un número válido y no negativo."
                )

    @abstractmethod
    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0
    ) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


# 4. Servicio de reserva de salas
class ReservaSala(Servicio):

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponible: bool = True
    ):
        self.capacidad = capacidad
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()

        if (
            isinstance(self.capacidad, bool)
            or not isinstance(self.capacidad, int)
            or self.capacidad <= 0
        ):
            raise DatoInvalidoError(
                "La capacidad de la sala debe ser un entero mayor a cero."
            )

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0
    ) -> float:

        self.validar_parametros_calculo(duracion, impuesto, descuento)

        subtotal = self._tarifa_base * duracion
        total = (subtotal - descuento) * (1 + impuesto)

        if total <= 0 or not math.isfinite(total):
            raise CalculoInconsistenteError(
                "El costo total de la sala no es válido."
            )

        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Sala '{self._nombre}' "
            f"(Capacidad: {self.capacidad} pers.) "
            f"- Base: ${self._tarifa_base}/h"
        )


# 5. Servicio de alquiler de equipos
class AlquilerEquipo(Servicio):

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        categoria: str,
        disponible: bool = True
    ):
        self.categoria = categoria
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()

        if not isinstance(self.categoria, str) or not self.categoria.strip():
            raise DatoInvalidoError(
                "La categoría del equipo es obligatoria."
            )

        self.categoria = self.categoria.strip()

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0
    ) -> float:

        self.validar_parametros_calculo(duracion, impuesto, descuento)

        seguro_equipo = 15.0
        subtotal = (self._tarifa_base * duracion) + seguro_equipo
        total = (subtotal - descuento) * (1 + impuesto)

        if total <= 0 or not math.isfinite(total):
            raise CalculoInconsistenteError(
                "El costo total del alquiler no es válido."
            )

        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Equipo '{self._nombre}' [{self.categoria}] "
            f"- Base: ${self._tarifa_base}/día (+ seguro)"
        )


# 6. Servicio de asesoría especializada
class AsesoriaEspecializada(Servicio):

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        disponible: bool = True
    ):
        self.especialidad = especialidad
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()

        if (
            not isinstance(self.especialidad, str)
            or not self.especialidad.strip()
        ):
            raise DatoInvalidoError(
                "La especialidad de la asesoría es obligatoria."
            )

        self.especialidad = self.especialidad.strip()

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0
    ) -> float:

        self.validar_parametros_calculo(duracion, impuesto, descuento)

        subtotal = self._tarifa_base * duracion

        if duracion > 5:
            descuento += 20.0

        total = (subtotal - descuento) * (1 + impuesto)

        if total <= 0 or not math.isfinite(total):
            raise CalculoInconsistenteError(
                "El cálculo de la asesoría no es válido."
            )

        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Asesoría '{self._nombre}' "
            f"(Área: {self.especialidad}) "
            f"- Base: ${self._tarifa_base}/h"
        )


# 7. Clase Reserva
class Reserva(EntidadBase):

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int
    ):
        super().__init__(id_reserva)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

        self._estado = "PENDIENTE"
        self._costo_total = 0.0

        self.validar_datos()

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def validar_datos(self):
        if not isinstance(self.cliente, Cliente):
            raise DatoInvalidoError(
                "La reserva requiere un objeto Cliente válido."
            )

        if not isinstance(self.servicio, Servicio):
            raise DatoInvalidoError(
                "La reserva requiere un objeto Servicio válido."
            )

        if (
            isinstance(self.duracion, bool)
            or not isinstance(self.duracion, int)
            or self.duracion <= 0
        ):
            raise DatoInvalidoError(
                "La duración de la reserva debe ser un entero positivo."
            )

    def procesar_y_confirmar(
        self,
        impuesto: float = 0.19,
        descuento: float = 0.0
    ):
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' no está disponible."
            )

        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )

        try:
            costo = self.servicio.calcular_costo(
                self.duracion,
                impuesto,
                descuento
            )

            self._costo_total = costo
            self._estado = "CONFIRMADA"
            self.servicio.disponible = False

        except CalculoInconsistenteError as e:
            raise OperacionNoPermitidaError(
                "Fallo al procesar el cobro de la reserva."
            ) from e

    def cancelar(self):
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas confirmadas."
            )

        self._estado = "CANCELADA"
        self.servicio.disponible = True
