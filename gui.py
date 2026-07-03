"""
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programacion
Integrante: Miguel Angel Walteros Rodriguez
Grupo: 213023_13
Tutor: Jorge Eduardo Ospina

Descripcion del archivo: 
Interfaz grafica construida con Tkinter. 
Permite registrar clientes, crear reservas de servicios de forma visual, 
ver el log en tiempo real y correr la simulacion automatica de las 10 operaciones.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from gestor import GestorEmpresa
from logger_config import log
from excepciones import SistemaGestionError
import os

class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema de Gestion de Reservas")
        self.root.geometry("700x650")
        
        self.gestor = GestorEmpresa()
        self.crear_servicios_iniciales()
        
        # Titulo Principal
        titulo = tk.Label(root, text="Sistema de Gestion Software FJ", font=("Arial", 16, "bold"), fg="#004488")
        titulo.pack(pady=10)
        
        # Panel de Pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Pestaña 1: Registro de Clientes
        self.tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clientes, text="Clientes")
        self.crear_interfaz_clientes()
        
        # Pestaña 2: Crear Reservas
        self.tab_reservas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.crear_interfaz_reservas()
        
        # Pestaña 3: Logs y Simulacion
        self.tab_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_logs, text="Logs y Simulacion")
        self.crear_interfaz_logs()
        
        # Cargar los logs iniciales
        self.actualizar_logs()

    def crear_servicios_iniciales(self):
        # Creamos los servicios base requeridos para que esten listos para reservar
        try:
            self.gestor.crear_servicio("sala", costo_base=50.0)
            self.gestor.crear_servicio("equipo", costo_base=30.0)
            self.gestor.crear_servicio("asesoria", costo_base=100.0)
        except Exception as e:
            log.error(f"Error al crear servicios iniciales: {e}")

    # --- INTERFAZ PESTAÑA CLIENTES ---
    def crear_interfaz_clientes(self):
        frame = tk.LabelFrame(self.tab_clientes, text=" Registrar Nuevo Cliente ", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame, text="Identificacion (Alfanumerica):").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_id = tk.Entry(frame)
        self.ent_id.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(frame, text="Nombre completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nombre = tk.Entry(frame)
        self.ent_nombre.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_email = tk.Entry(frame)
        self.ent_email.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        btn_registrar = tk.Button(frame, text="Registrar Cliente", command=self.registrar_cliente, bg="#4CAF50", fg="black")
        btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Lista para ver clientes registrados
        frame_lista = tk.LabelFrame(self.tab_clientes, text=" Clientes Registrados ", padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.txt_clientes = tk.Text(frame_lista, height=10)
        self.txt_clientes.pack(fill="both", expand=True)
        self.actualizar_lista_clientes()

    def registrar_cliente(self):
        ide = self.ent_id.get().strip()
        nom = self.ent_nombre.get().strip()
        ema = self.ent_email.get().strip()
        
        try:
            cliente = self.gestor.registrar_cliente(ide, nom, ema)
            messagebox.showinfo("Exito", f"Cliente {cliente.nombre} registrado con exito.")
            self.ent_id.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_email.delete(0, tk.END)
            self.actualizar_lista_clientes()
            self.actualizar_logs()
        except SistemaGestionError as e:
            messagebox.showerror("Error de Validacion", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))

    def actualizar_lista_clientes(self):
        self.txt_clientes.delete("1.0", tk.END)
        if not self.gestor.clientes:
            self.txt_clientes.insert(tk.END, "No hay clientes registrados todavia.")
            return
        for c in self.gestor.clientes:
            self.txt_clientes.insert(tk.END, f"- ID: {c.identificacion} | Nombre: {c.nombre} | Email: {c.email}\n")

    # --- INTERFAZ PESTAÑA RESERVAS ---
    def crear_interfaz_reservas(self):
        frame = tk.LabelFrame(self.tab_reservas, text=" Crear Nueva Reserva ", padx=10, pady=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Identificacion del Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_res_id_cliente = tk.Entry(frame)
        self.ent_res_id_cliente.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(frame, text="Seleccione el Servicio:").grid(row=1, column=0, sticky="w", pady=5)
        self.cmb_servicio = ttk.Combobox(frame, values=["Reserva de Sala", "Alquiler de Equipo Informatico", "Asesoria Especializada"], state="readonly")
        self.cmb_servicio.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.cmb_servicio.bind("<<ComboboxSelected>>", self.on_servicio_cambiado)
        
        # Panel de parametros dinamicos
        self.frame_parametros = tk.LabelFrame(frame, text=" Parametros del Servicio Seleccionado ", padx=10, pady=10)
        self.frame_parametros.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.lbl_param1 = tk.Label(self.frame_parametros, text="Parametro:")
        self.lbl_param1.grid(row=0, column=0, sticky="w", pady=5)
        self.ent_param1 = tk.Entry(self.frame_parametros)
        self.ent_param1.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        self.var_chk = tk.BooleanVar()
        self.chk_param2 = tk.Checkbutton(self.frame_parametros, text="Opcion adicional", variable=self.var_chk)
        self.chk_param2.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        # Ocultar campos de parametros al inicio
        self.frame_parametros.grid_remove()
        
        btn_reservar = tk.Button(frame, text="Confirmar Reserva", command=self.crear_reserva, bg="#004488", fg="black")
        btn_reservar.grid(row=3, column=0, columnspan=2, pady=10)

    def on_servicio_cambiado(self, event):
        seleccion = self.cmb_servicio.get()
        self.frame_parametros.grid()
        self.ent_param1.delete(0, tk.END)
        self.var_chk.set(False)
        
        if seleccion == "Reserva de Sala":
            self.lbl_param1.configure(text="Horas de reserva (Entero):")
            self.chk_param2.configure(text="Incluye Proyector ($20 adicionales)")
            self.ent_param1.grid()
            self.chk_param2.grid()
        elif seleccion == "Alquiler de Equipo Informatico":
            self.lbl_param1.configure(text="Dias de alquiler (Entero):")
            self.chk_param2.configure(text="Requiere Seguro ($15 por dia)")
            self.ent_param1.grid()
            self.chk_param2.grid()
        elif seleccion == "Asesoria Especializada":
            self.lbl_param1.configure(text="Nivel de experto (Junior / Semi-Senior / Senior):")
            self.ent_param1.grid()
            self.chk_param2.grid_remove() # No aplica seguro para asesoria

    def crear_reserva(self):
        id_cl = self.ent_res_id_cliente.get().strip()
        tipo_srv = self.cmb_servicio.get()
        
        if not id_cl or not tipo_srv:
            messagebox.showerror("Error", "Debe ingresar el ID del cliente y seleccionar un servicio.")
            return
            
        try:
            # Buscar el servicio correspondiente en la lista del gestor
            servicio_obj = None
            for s in self.gestor.servicios:
                if tipo_srv == "Reserva de Sala" and s.__class__.__name__ == "ServicioReservaSala":
                    servicio_obj = s
                elif tipo_srv == "Alquiler de Equipo Informatico" and s.__class__.__name__ == "ServicioAlquilerEquipo":
                    servicio_obj = s
                elif tipo_srv == "Asesoria Especializada" and s.__class__.__name__ == "ServicioAsesoria":
                    servicio_obj = s
            
            if not servicio_obj:
                raise SistemaGestionError("El servicio no esta disponible en el sistema.")
            
            # Recolectar parametros
            parametros = {}
            if tipo_srv == "Reserva de Sala":
                try:
                    parametros['horas'] = int(self.ent_param1.get())
                except ValueError:
                    raise SistemaGestionError("Las horas deben ser un numero entero.")
                parametros['incluye_proyector'] = self.var_chk.get()
                
            elif tipo_srv == "Alquiler de Equipo Informatico":
                try:
                    parametros['dias'] = int(self.ent_param1.get())
                except ValueError:
                    raise SistemaGestionError("Los dias deben ser un numero entero.")
                parametros['requiere_seguro'] = self.var_chk.get()
                
            elif tipo_srv == "Asesoria Especializada":
                parametros['nivel_experto'] = self.ent_param1.get().strip()
            
            reserva = self.gestor.crear_reserva(id_cl, servicio_obj, **parametros)
            messagebox.showinfo("Exito", f"Reserva creada para {reserva.cliente.nombre} por un costo de ${reserva.costo_total}")
            
            self.ent_res_id_cliente.delete(0, tk.END)
            self.frame_parametros.grid_remove()
            self.cmb_servicio.set("")
            self.actualizar_logs()
            
        except SistemaGestionError as e:
            messagebox.showerror("Error de Logica", str(e))
        except Exception as e:
            messagebox.showerror("Error del Sistema", str(e))

    # --- INTERFAZ PESTAÑA LOGS ---
    def crear_interfaz_logs(self):
        frame_sim = tk.Frame(self.tab_logs)
        frame_sim.pack(fill="x", padx=10, pady=5)
        
        btn_simular = tk.Button(frame_sim, text="Ejecutar Simulacion de 10 Operaciones", command=self.correr_simulacion, bg="#FF9800", fg="black")
        btn_simular.pack(side="left", pady=10)
        
        btn_actualizar = tk.Button(frame_sim, text="Actualizar Vista de Logs", command=self.actualizar_logs)
        btn_actualizar.pack(side="right", pady=10)
        
        frame_txt = tk.LabelFrame(self.tab_logs, text=" Archivo de Log: sistema.log ")
        frame_txt.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_logs = tk.Text(frame_txt, height=20, font=("Courier", 10))
        self.txt_logs.pack(fill="both", expand=True)

    def actualizar_logs(self):
        self.txt_logs.delete("1.0", tk.END)
        if not os.path.exists("sistema.log"):
            self.txt_logs.insert(tk.END, "El archivo 'sistema.log' todavia no ha sido creado.")
            return
            
        with open("sistema.log", "r", encoding="utf-8") as f:
            lineas = f.readlines()
            # Mostrar las ultimas 40 lineas para no saturar
            ultimas_lineas = lineas[-40:]
            for linea in ultimas_lineas:
                self.txt_logs.insert(tk.END, linea)

    def correr_simulacion(self):
        # Limpia el gestor para que la simulacion empiece limpia
        self.gestor = GestorEmpresa()
        self.crear_servicios_iniciales()
        
        # Corremos la simulación importando y llamando la funcion
        from main import simular_operaciones
        try:
            simular_operaciones()
            messagebox.showinfo("Simulacion Completa", "Se ejecutaron las 10 operaciones de prueba. Revisa la pestaña de logs.")
            self.actualizar_lista_clientes()
            self.actualizar_logs()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulacion: {e}")

if __name__ == "__main__":
    window = tk.Tk()
    app = AppSoftwareFJ(window)
    window.mainloop()
