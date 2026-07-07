"""
---------------------------------------------------------
Módulo: estadisticas.py
Proyecto: SoftwareFJ
Autor: Roger Arenas Peláez

Descripción:
Este módulo permite obtener estadísticas básicas del sistema
sin modificar el funcionamiento del proyecto principal.
---------------------------------------------------------
"""


class Estadisticas:
    """Clase encargada de generar estadísticas del sistema."""

    @staticmethod
    def total_clientes(clientes):
        """Retorna el número total de clientes."""
        return len(clientes)

    @staticmethod
    def total_servicios(servicios):
        """Retorna el número total de servicios."""
        return len(servicios)

    @staticmethod
    def total_reservas(reservas):
        """Retorna el número total de reservas."""
        return len(reservas)

    @staticmethod
    def reservas_confirmadas(reservas):
        """Cuenta las reservas confirmadas."""
        return sum(
            1
            for reserva in reservas
            if getattr(reserva, "estado", "").lower() == "confirmada"
        )

    @staticmethod
    def reservas_canceladas(reservas):
        """Cuenta las reservas canceladas."""
        return sum(
            1
            for reserva in reservas
            if getattr(reserva, "estado", "").lower() == "cancelada"
        )

    @staticmethod
    def porcentaje_confirmadas(reservas):
        """Calcula el porcentaje de reservas confirmadas."""
        if not reservas:
            return 0

        confirmadas = Estadisticas.reservas_confirmadas(reservas)
        return round((confirmadas / len(reservas)) * 100, 2)

    @staticmethod
    def porcentaje_canceladas(reservas):
        """Calcula el porcentaje de reservas canceladas."""
        if not reservas:
            return 0

        canceladas = Estadisticas.reservas_canceladas(reservas)
        return round((canceladas / len(reservas)) * 100, 2)