"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina
Version: Revision Final - Primera Entrega

Descripcion del archivo: 
En este archivo creamos la logica de objetos (POO).
Aqui estan las clases base, el Cliente, el Servicio y la Reserva.
Tambien hacemos validaciones para que los datos sean correctos.
"""
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from excepciones import DatosInvalidosError

class EntidadSistema(ABC):
    """Clase abstracta base para todas las entidades del sistema."""
    def __init__(self):
        self._id = str(uuid.uuid4())[:8]
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

class Cliente(EntidadSistema):
    """Clase Cliente con encapsulación y validaciones estrictas."""
    def __init__(self, identificacion, nombre, email):
        super().__init__()
        self.identificacion = identificacion
        self.nombre = nombre
        self.email = email

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not str(valor).isalnum():
            raise DatosInvalidosError("La identificación del cliente debe ser alfanumérica y no estar vacía.")
        self._identificacion = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in str(valor) or "." not in str(valor):
            raise DatosInvalidosError("El email proporcionado no es válido.")
        self._email = valor

    def __str__(self):
        return f"Cliente[{self.identificacion} - {self.nombre}]"


class Servicio(EntidadSistema):
    """Clase abstracta Servicio."""
    def __init__(self, nombre, costo_base):
        super().__init__()
        if costo_base < 0:
            raise DatosInvalidosError("El costo base del servicio no puede ser negativo.")
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método abstracto polimórfico y preparado para sobrecarga (opcionales)."""
        pass

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"

class Reserva(EntidadSistema):
    """Clase para gestionar reservas entre clientes y servicios."""
    def __init__(self, cliente: Cliente, servicio: Servicio):
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def confirmar(self, costo_calculado):
        self.estado = "CONFIRMADA"
        self.costo_total = costo_calculado

    def cancelar(self):
        self.estado = "CANCELADA"

    def __str__(self):
        return f"Reserva[{self.id}] - {self.cliente.nombre} -> {self.servicio.nombre} ({self.estado})"

# --- Subclases de Servicio (Polimorfismo) ---

class ServicioReservaSala(Servicio):
    def __init__(self, nombre="Reserva de Sala", costo_base=50.0):
        super().__init__(nombre, costo_base)

    def calcular_costo(self, horas, incluye_proyector=False):
        if horas <= 0:
            raise DatosInvalidosError("Las horas de reserva de sala deben ser mayores a cero.")
        costo = self.costo_base * horas
        if incluye_proyector:
            costo += 20.0
        return costo

class ServicioAlquilerEquipo(Servicio):
    def __init__(self, nombre="Alquiler de Equipo Informático", costo_base=30.0):
        super().__init__(nombre, costo_base)

    def calcular_costo(self, dias, requiere_seguro=True):
        if dias <= 0:
            raise DatosInvalidosError("Los días de alquiler deben ser mayores a cero.")
        costo = self.costo_base * dias
        if requiere_seguro:
            costo += 15.0 * dias  # $15 adicionales por día de seguro
        return costo

class ServicioAsesoria(Servicio):
    def __init__(self, nombre="Asesoría Especializada", costo_base=100.0):
        super().__init__(nombre, costo_base)

    def calcular_costo(self, nivel_experto="Junior"):
        multiplicadores = {"Junior": 1.0, "Semi-Senior": 1.5, "Senior": 2.5}
        nivel = nivel_experto.capitalize()
        if nivel not in multiplicadores:
            raise DatosInvalidosError(f"Nivel de experto '{nivel_experto}' no reconocido.")
        
        return self.costo_base * multiplicadores[nivel]
