"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina
Version: Revision Final - Primera Entrega

Descripcion del archivo: 
Este es el archivo principal que simula que el programa esta funcionando.
Hace 10 operaciones de prueba, algunas buenas y otras malas a proposito
para demostrar que el programa no se cae cuando hay fallas.
"""
import traceback
from gestor import GestorEmpresa
from logger_config import log
from excepciones import (
    SistemaGestionError, DatosInvalidosError, ClienteNoEncontradoError
)

def simular_operaciones():
    print("Iniciando simulacion de operaciones del Sistema Software FJ...")
    log.info("--- INICIO DE SIMULACION DE 10 OPERACIONES ---")
    gestor = GestorEmpresa()

    # Operacion 1: Registro de cliente valido
    print("\n[1] Registrando cliente valido...")
    log.info("OPERACION 1: Registro de cliente valido (Juan Perez)")
    try:
        c1 = gestor.registrar_cliente("12345", "Juan Perez", "juan@correo.com")
        print(f"Exito: {c1}")
    except SistemaGestionError as e:
        print(f"Error esperado: {e}")

    # Operacion 2: Registro de cliente invalido (nombre corto)
    print("\n[2] Registrando cliente con nombre invalido...")
    log.info("OPERACION 2: Intento de registro con nombre invalido (nombre muy corto)")
    try:
        gestor.registrar_cliente("67890", "A", "correo@correo.com")
    except SistemaGestionError as e:
        print(f"Error manejado sin detener ejecucion: {e}")

    # Operacion 3: Registro de cliente con email invalido
    print("\n[3] Registrando cliente con email invalido...")
    log.info("OPERACION 3: Intento de registro con email invalido (sin arroba)")
    try:
        gestor.registrar_cliente("11111", "Maria Lopez", "correo_sin_arroba.com")
    except SistemaGestionError as e:
        print(f"Error manejado: {e}")

    # Operacion 4: Creacion de servicio valido (Sala)
    print("\n[4] Creando servicio de sala...")
    log.info("OPERACION 4: Creacion de servicio valido (Reserva de Sala)")
    try:
        s_sala = gestor.crear_servicio("sala", costo_base=50.0)
        print(f"Exito: {s_sala}")
    except SistemaGestionError as e:
        print(f"Error esperado: {e}")

    # Operacion 5: Creacion de servicio valido (Asesoria)
    print("\n[5] Creando servicio de asesoria...")
    log.info("OPERACION 5: Creacion de servicio valido (Asesoria Especializada)")
    try:
        s_asesoria = gestor.crear_servicio("asesoria", costo_base=120.0)
        print(f"Exito: {s_asesoria}")
    except SistemaGestionError as e:
        print(f"Error esperado: {e}")

    # Operacion 6: Creacion de servicio con costo negativo (Invalido)
    print("\n[6] Creando servicio con costo negativo...")
    log.info("OPERACION 6: Intento de creacion de servicio con costo negativo")
    try:
        gestor.crear_servicio("equipo", costo_base=-10.0)
    except SistemaGestionError as e:
        print(f"Error manejado: {e}")

    # Operacion 7: Reserva exitosa (Sala por 4 horas con proyector)
    print("\n[7] Realizando reserva exitosa (Sala)...")
    log.info("OPERACION 7: Creacion de reserva exitosa para servicio de sala")
    try:
        reserva1 = gestor.crear_reserva("12345", s_sala, horas=4, incluye_proyector=True)
        print(f"Exito: {reserva1} - Costo: ${reserva1.costo_total}")
    except SistemaGestionError as e:
        print(f"Error esperado: {e}")

    # Operacion 8: Reserva fallida (Cliente inexistente)
    print("\n[8] Reserva con cliente inexistente...")
    log.info("OPERACION 8: Intento de reserva con cliente no registrado")
    try:
        gestor.crear_reserva("99999", s_sala, horas=2)
    except SistemaGestionError as e:
        print(f"Error manejado: {e}")

    # Operacion 9: Reserva fallida (Calculo de costo con datos invalidos, ej. horas negativas)
    print("\n[9] Reserva con parametros de costo invalidos...")
    log.info("OPERACION 9: Intento de reserva con parametros de calculo invalidos (horas negativas)")
    try:
        gestor.crear_reserva("12345", s_sala, horas=-5)
    except SistemaGestionError as e:
        print(f"Error manejado: {e}")

    # Operacion 10: Reserva exitosa (Asesoria nivel Senior)
    print("\n[10] Realizando reserva exitosa (Asesoria Senior)...")
    log.info("OPERACION 10: Creacion de reserva exitosa para servicio de asesoria nivel Senior")
    try:
        reserva2 = gestor.crear_reserva("12345", s_asesoria, nivel_experto="Senior")
        print(f"Exito: {reserva2} - Costo: ${reserva2.costo_total}")
    except SistemaGestionError as e:
        print(f"Error esperado: {e}")
    
    # Resumen Final
    gestor.mostrar_resumen()
    log.info("--- FIN DE SIMULACION ---")
    print("Simulacion finalizada. Todos los errores han sido manejados y registrados en 'sistema.log'.")

if __name__ == "__main__":
    # Si se importa o se llama directamente, podemos abrir la interfaz grafica.
    # Pero mantenemos la simulacion automatica tambien si se quiere.
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--consola":
        try:
            simular_operaciones()
        except Exception as fatal_e:
            print("Ocurrio un error no controlado en el sistema principal.")
            log.critical("Fallo catastrofico global.", exc_info=True)
    else:
        try:
            import tkinter as tk
            from gui import AppSoftwareFJ
            root = tk.Tk()
            app = AppSoftwareFJ(root)
            root.mainloop()
        except Exception as gui_e:
            print("No se pudo iniciar la interfaz grafica, corriendo en modo consola...")
            log.warning("No se pudo iniciar la interfaz grafica, corriendo en modo consola...", exc_info=True)
            simular_operaciones()

