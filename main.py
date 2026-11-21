
from logger import LoggerSistema
from excepciones import ErrorSistemaFJ
from modelos import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva
)


class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = LoggerSistema()

    def registrar_cliente(self, id_c, nombre, correo):
        try:
            cliente = Cliente(id_c, nombre, correo)
            self.clientes.append(cliente)

        except ErrorSistemaFJ as e:
            self.logger.registrar_evento(
                "ERROR",
                f"Registro cliente fallido ({id_c}): {e}"
            )
            print(f"[X] Error registrando cliente: {e}")

        else:
            self.logger.registrar_evento(
                "INFO",
                f"Cliente registrado: {cliente.nombre} ({cliente.id})"
            )
            print(
                f"[OK] Cliente '{cliente.nombre}' "
                "registrado con éxito."
            )

        finally:
            print("    -> Finalizó intento de registro de cliente.\n")

    def registrar_servicio(self, servicio_obj):
        self.servicios.append(servicio_obj)

        self.logger.registrar_evento(
            "INFO",
            f"Servicio agregado: {servicio_obj.describir_servicio()}"
        )

        print(
            f"[OK] Servicio registrado: "
            f"{servicio_obj.describir_servicio()}\n"
        )

    def crear_y_confirmar_reserva(
        self,
        id_r,
        cliente,
        servicio,
        duracion,
        impuesto=0.19,
        descuento=0.0
    ):
        try:
            reserva = Reserva(
                id_r,
                cliente,
                servicio,
                duracion
            )

            reserva.procesar_y_confirmar(
                impuesto=impuesto,
                descuento=descuento
            )

            self.reservas.append(reserva)

        except ErrorSistemaFJ as e:
            causa = (
                f" | Causa original: {e.__cause__}"
                if e.__cause__
                else ""
            )

            self.logger.registrar_evento(
                "ERROR",
                f"Reserva {id_r} fallida: {e}{causa}"
            )

            print(
                f"[X] Error en reserva {id_r}: "
                f"{e}{causa}"
            )

        else:
            self.logger.registrar_evento(
                "INFO",
                f"Reserva {id_r} confirmada. "
                f"Total: ${reserva.costo_total}"
            )

            print(
                f"[OK] Reserva {id_r} CONFIRMADA "
                f"para {cliente.nombre}. "
                f"Total: ${reserva.costo_total}"
            )

        finally:
            print("    -> Transacción de reserva finalizada.\n")


def demostrar_variantes_calculo(servicio):
    print("\n=== DEMOSTRACIÓN DE VARIANTES DE CÁLCULO ===")

    try:
        # Variante 1: cálculo con duración y valores predeterminados
        costo_basico = servicio.calcular_costo(2)

        print(
            f"1. Cálculo básico (2 unidades): "
            f"${costo_basico}"
        )

        # Variante 2: cálculo con impuesto personalizado
        costo_impuesto = servicio.calcular_costo(2, 0.16)

        print(
            f"2. Cálculo con impuesto del 16%: "
            f"${costo_impuesto}"
        )

        # Variante 3: cálculo con impuesto y descuento
        costo_descuento = servicio.calcular_costo(
            2,
            0.19,
            20.0
        )

        print(
            f"3. Cálculo con impuesto del 19% "
            f"y descuento de $20: ${costo_descuento}"
        )

        print("Demostración de variantes completada.\n")

    except ErrorSistemaFJ as e:
        print(f"[X] Error en la demostración: {e}")


def ejecutar_simulacion():
    sistema = GestorSoftwareFJ()

    print(
        "=== INICIANDO SIMULACIÓN DE 10 OPERACIONES "
        "- SOFTWARE FJ ===\n"
    )

    # Operación 1: Registro válido de cliente
    sistema.registrar_cliente(
        "C01",
        "Laura Gómez",
        "laura.gomez@empresa.com"
    )

    # Operación 2: Registro inválido de cliente
    sistema.registrar_cliente(
        "C02",
        "Carlos Ruiz",
        "://empresa.com"
    )

    # Operación 3: Registro válido de segundo cliente
    sistema.registrar_cliente(
        "C03",
        "Andrés Mejía",
        "andres@tech.co"
    )

    # Operación 4: Creación válida de sala
    try:
        sala1 = ReservaSala(
            "S01",
            "Sala Juntas Norte",
            50.0,
            capacidad=12
        )

        sistema.registrar_servicio(sala1)

    except ErrorSistemaFJ as e:
        sistema.logger.registrar_evento(
            "ERROR",
            f"Error creando sala: {e}"
        )
        print(f"[X] Error creando sala: {e}")

    # Operación 5: Creación inválida de equipo
    try:
        equipo_malo = AlquilerEquipo(
            "E99",
            "Proyector 4K",
            -30.0,
            "Audiovisual"
        )

        sistema.registrar_servicio(equipo_malo)

    except ErrorSistemaFJ as e:
        sistema.logger.registrar_evento(
            "ERROR",
            f"Creación de servicio fallida (E99): {e}"
        )
        print(f"[X] Error creando servicio E99: {e}\n")

    # Operación 6: Creación válida de equipo y asesoría
    equipo1 = AlquilerEquipo(
        "E01",
        "Servidor Portátil",
        80.0,
        "Cómputo"
    )

    asesoria1 = AsesoriaEspecializada(
        "A01",
        "Arquitectura Cloud",
        100.0,
        "Infraestructura"
    )

    sistema.registrar_servicio(equipo1)
    sistema.registrar_servicio(asesoria1)

    # Demostración de las variantes de cálculo
    demostrar_variantes_calculo(sala1)

    # Operación 7: Reserva exitosa de sala
    sistema.crear_y_confirmar_reserva(
        "R01",
        sistema.clientes[0],
        sala1,
        duracion=3
    )

    # Operación 8: Intento de reservar sala ocupada
    sistema.crear_y_confirmar_reserva(
        "R02",
        sistema.clientes[1],
        sala1,
        duracion=2
    )

    # Operación 9: Reserva fallida por descuento excesivo
    sistema.crear_y_confirmar_reserva(
        "R03",
        sistema.clientes[1],
        equipo1,
        duracion=1,
        descuento=500.0
    )

    # Operación 10: Reserva exitosa con descuento
    sistema.crear_y_confirmar_reserva(
        "R04",
        sistema.clientes[1],
        asesoria1,
        duracion=6,
        descuento=30.0
    )

    # Cancelación de la reserva R04
    try:
        reserva_a_cancelar = next(
            (
                reserva for reserva in sistema.reservas
                if reserva.id == "R04"
            ),
            None
        )

        if reserva_a_cancelar is not None:
            reserva_a_cancelar.cancelar()

            sistema.logger.registrar_evento(
                "INFO",
                f"Reserva {reserva_a_cancelar.id} "
                "cancelada por el usuario."
            )

            print(
                f"[OK] Reserva {reserva_a_cancelar.id} "
                "cancelada correctamente. Servicio liberado.\n"
            )

        else:
            print(
                "[!] No se pudo cancelar R04 "
                "porque no fue confirmada.\n"
            )

    except ErrorSistemaFJ as e:
        sistema.logger.registrar_evento(
            "ERROR",
            f"Error al cancelar: {e}"
        )

        print(f"[X] Error al cancelar: {e}")

    print("=== SIMULACIÓN COMPLETADA SIN INTERRUPCIONES ===")

    print(
        "Revisa el archivo "
        "'sistema_software_fj.log' generado "
        "en la carpeta del proyecto."
    )


if __name__ == "__main__":
    ejecutar_simulacion()
