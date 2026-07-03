"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina
Version: Revision Final - Primera Entrega

Descripcion del archivo: 
Este es el administrador del sistema. 
Se encarga de crear clientes, servicios y hacer las reservas.
Atrapa los errores y usa el logger para dejar registro de lo que sale mal.
"""
from excepciones import (
    DatosInvalidosError, ClienteNoEncontradoError, 
    ServicioNoDisponibleError, ReservaInvalidaError
)
from logger_config import log
from modelos import (
    Cliente, ServicioReservaSala, ServicioAlquilerEquipo, 
    ServicioAsesoria, Reserva
)

class GestorEmpresa:
    """Clase principal que gestiona las operaciones de Software FJ."""
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, identificacion, nombre, email):
        log.info(f"Intentando registrar cliente: {nombre}")
        try:
            nuevo_cliente = Cliente(identificacion, nombre, email)
            self.clientes.append(nuevo_cliente)
        except DatosInvalidosError as e:
            log.error(f"Error al registrar cliente '{nombre}': {e}")
            raise  # Relanzamos la excepción si es necesario que el nivel superior la maneje
        except Exception as e:
            log.critical(f"Error inesperado al registrar cliente: {e}")
            raise
        else:
            log.info(f"Cliente '{nombre}' registrado exitosamente con ID {nuevo_cliente.id}")
            return nuevo_cliente

    def buscar_cliente(self, identificacion):
        for c in self.clientes:
            if c.identificacion == identificacion:
                return c
        raise ClienteNoEncontradoError(f"No existe un cliente con identificación {identificacion}")

    def crear_servicio(self, tipo_servicio, **kwargs):
        log.info(f"Intentando crear servicio de tipo: {tipo_servicio}")
        try:
            if tipo_servicio == "sala":
                servicio = ServicioReservaSala(**kwargs)
            elif tipo_servicio == "equipo":
                servicio = ServicioAlquilerEquipo(**kwargs)
            elif tipo_servicio == "asesoria":
                servicio = ServicioAsesoria(**kwargs)
            else:
                raise ServicioNoDisponibleError(f"El tipo de servicio '{tipo_servicio}' no es válido.")
            
            self.servicios.append(servicio)
        except (DatosInvalidosError, ServicioNoDisponibleError) as e:
            log.error(f"Error de validación al crear servicio: {e}")
            raise
        except Exception as e:
            log.critical(f"Error catastrófico al crear servicio: {e}")
            raise
        else:
            log.info(f"Servicio '{servicio.nombre}' creado exitosamente con ID {servicio.id}")
            return servicio

    def crear_reserva(self, id_cliente, servicio, **parametros_costo):
        """
        Crea una reserva integrando el cliente y el servicio, 
        y calculando el costo con los parámetros variables mediante polimorfismo.
        """
        log.info(f"Intentando crear reserva para cliente con ID {id_cliente}")
        try:
            cliente = self.buscar_cliente(id_cliente)
            
            if servicio not in self.servicios:
                raise ServicioNoDisponibleError("El servicio solicitado no está en el catálogo de la empresa.")
            
            reserva = Reserva(cliente, servicio)
            
            # Polimorfismo en acción: cada servicio calcula de manera distinta
            costo = servicio.calcular_costo(**parametros_costo)
            
            reserva.confirmar(costo)
            self.reservas.append(reserva)

        except ClienteNoEncontradoError as e:
            log.error(f"Fallo al reservar: {e}")
            raise
        except DatosInvalidosError as e:
            log.error(f"Fallo al calcular costos de reserva: {e}")
            raise
        except ServicioNoDisponibleError as e:
            log.error(f"Fallo de disponibilidad: {e}")
            raise
        except Exception as e:
            # Aquí aplicamos encadenamiento de excepciones (raise from)
            log.critical(f"Error desconocido procesando reserva para cliente {id_cliente}")
            raise ReservaInvalidaError("La reserva no pudo procesarse debido a un error interno del sistema.") from e
        else:
            log.info(f"Reserva creada exitosamente: {reserva}")
            return reserva
        finally:
            log.debug(f"Proceso de creación de reserva finalizado para cliente {id_cliente}")

    def mostrar_resumen(self):
        print("\n=== RESUMEN DEL SISTEMA ===")
        print(f"Total Clientes: {len(self.clientes)}")
        print(f"Total Servicios: {len(self.servicios)}")
        print(f"Total Reservas: {len(self.reservas)}")
        print("===========================\n")
