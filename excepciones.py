"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina
Version: Revision Final - Primera Entrega

Descripcion del archivo: 
Este archivo contiene las clases de errores personalizados. 
Nos ayuda a atrapar errores especificos en vez de que el programa falle por completo.
"""

class SistemaGestionError(Exception):
    """Clase base para todas las excepciones del sistema."""
    pass

class DatosInvalidosError(SistemaGestionError):
    """Excepción lanzada cuando los datos ingresados no cumplen con las validaciones."""
    pass

class ClienteNoEncontradoError(SistemaGestionError):
    """Excepción lanzada cuando se intenta operar con un cliente que no existe."""
    pass

class ServicioNoDisponibleError(SistemaGestionError):
    """Excepción lanzada cuando se intenta solicitar o utilizar un servicio inválido."""
    pass

class ReservaInvalidaError(SistemaGestionError):
    """Excepción lanzada por errores lógicos en el manejo de reservas (ej. cancelar ya cancelada)."""
    pass
