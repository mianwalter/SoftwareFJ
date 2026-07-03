"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina
Version: Revision Final - Primera Entrega

Descripcion del archivo: 
Aqui configuramos el sistema que guarda todos los movimientos y errores en un archivo de texto (sistema.log).
De esta manera queda un registro de todo lo que pasa sin detener el sistema.
"""
import logging

def configurar_logger():
    """Configura y retorna el logger principal del sistema."""
    logger = logging.getLogger('SoftwareFJ')
    logger.setLevel(logging.DEBUG)

    # Evitar que se añadan múltiples handlers si se llama varias veces
    if not logger.handlers:
        # File handler para guardar logs
        file_handler = logging.FileHandler('sistema.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Formato del log
        formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formato)

        logger.addHandler(file_handler)

    return logger

# Instancia global del logger
log = configurar_logger()
