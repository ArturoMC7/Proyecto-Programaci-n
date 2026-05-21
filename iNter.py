import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import supervision_client as cli

URL_SERVIDOR = "http://localhost:8080" 

COLOR_BARRA_TOP = "#1e293b"
COLOR_SIDEBAR   = "#334155"
COLOR_BG        = "#f8fafc"
COLOR_CARD      = "#ffffff"
COLOR_TEXT_MAIN = "#0f172a"
COLOR_ACCENT    = "#0ea5e9"
COLOR_SUCCESS   = "#10b981"

class SistemaSupervisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Supervisión - V3 Dinámica")
        self.geometry("1180x740")
        self.minsize(1050, 680)
        
        # Guardamos TODO el perfil del usuario en sesión
        self.usuario_actual = ""
        self.password_actual = ""
        self.rol_actual = ""
        self.email_actual = ""
        self.edad_actual = ""

        self.contenedor = tk.Frame(self, bg=COLOR_BG)
        self.contenedor.pack(fill="both", expand=True)
        self.mostrar_login()

    def mostrar_login(self):
        self.limpiar_contenedor()
        PantallaLogin(self.contenedor, self).pack(fill="both", expand=True)

    def mostrar_registro(self):
        self.limpiar_contenedor()
        PantallaRegistro(self.contenedor, self).pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        self.limpiar_contenedor()
        PantallaDashboard(self.contenedor, self).pack(fill="both", expand=True)

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children(): widget.destroy()

class PantallaLogin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        card = tk.Frame(self, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e2e8f0", padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text="¡Bienvenido!", font=("Arial", 22, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(0, 5))
        
        tk.Label(card, text="Usuario", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_SIDEBAR).pack(anchor="w")
        self.ent_user = ttk.Entry(card, font=("Arial", 11), width=30)
        self.ent_user.pack(pady=(5, 15))
        
        tk.Label(card, text="Contraseña", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_SIDEBAR).pack(anchor="w")
        self.ent_pass = ttk.Entry(card, font=("Arial", 11), show="*", width=30)
        self.ent_pass.pack(pady=(5, 25))
        
        tk.Button(card, text="Iniciar Sesión", font=("Arial", 11, "bold"), bg=COLOR_ACCENT, fg="white", bd=0, cursor="hand2", width=28, pady=8, command=self.auth_login).pack(pady=(0, 15))
        tk.Button(card, text="¿No tienes cuenta? Regístrate aquí", font=("Arial", 9, "underline"), bg=COLOR_CARD, fg="#475569", bd=0, cursor="hand2", command=self.controller.mostrar_registro).pack()

    def auth_login(self):
        user, pwd = self.ent_user.get().strip(), self.ent_pass.get().strip()
        if not user or not pwd: return
        try:
            res = json.loads(cli.openSession(URL_SERVIDOR, user, pwd))
            if "message" in res and res["message"] == "session updated":
                # AQUÍ GUARDAMOS LOS DATOS DINÁMICOS
                self.controller.usuario_actual = user
                self.controller.password_actual = pwd
                self.controller.rol_actual = res["user_data"].get("role", "viewer")
                self.controller.email_actual = res["user_data"].get("email", "Sin registrar")
                self.controller.edad_actual = res["user_data"].get("age", "Sin registrar")
                
                self.controller.mostrar_dashboard()
            else: messagebox.showerror("Error", res.get("error", "Credenciales incorrectas."))
        except Exception as e: messagebox.showerror("Error de Conexión", f"Asegúrate de que 'server.py' esté corriendo.\n{e}")

class PantallaRegistro(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        card = tk.Frame(self, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e2e8f0", padx=40, pady=25)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text="Crear Usuario", font=("Arial", 20, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(0, 15))
        
        tk.Label(card, text="Usuario", font=("Arial", 9, "bold"), bg=COLOR_CARD).pack(anchor="w")
        self.ent_user = ttk.Entry(card, font=("Arial", 10), width=35)
        self.ent_user.pack(pady=(2, 10))
        
        tk.Label(card, text="Contraseña", font=("Arial", 9, "bold"), bg=COLOR_CARD).pack(anchor="w")
        self.ent_pass = ttk.Entry(card, font=("Arial", 10), show="*", width=35)
        self.ent_pass.pack(pady=(2, 10))

        tk.Label(card, text="Correo Electrónico", font=("Arial", 9, "bold"), bg=COLOR_CARD).pack(anchor="w")
        self.ent_mail = ttk.Entry(card, font=("Arial", 10), width=35)
        self.ent_mail.pack(pady=(2, 10))

        tk.Label(card, text="Edad", font=("Arial", 9, "bold"), bg=COLOR_CARD).pack(anchor="w")
        self.ent_edad = ttk.Entry(card, font=("Arial", 10), width=35)
        self.ent_edad.pack(pady=(2, 10))
        
        tk.Label(card, text="Rol asignado", font=("Arial", 9, "bold"), bg=COLOR_CARD).pack(anchor="w")
        self.cb_role = ttk.Combobox(card, values=["admin", "supervisor", "viewer"], state="readonly", width=32)
        self.cb_role.current(2)
        self.cb_role.pack(pady=(2, 20))
        
        tk.Button(card, text="Registrar", font=("Arial", 11, "bold"), bg=COLOR_SUCCESS, fg="white", bd=0, width=30, pady=6, command=self.registrar).pack(pady=(0, 10))
        tk.Button(card, text="← Volver al Login", font=("Arial", 9), bg=COLOR_CARD, fg="#475569", bd=0, command=self.controller.mostrar_login).pack()

    def registrar(self):
        u, p, r = self.ent_user.get().strip(), self.ent_pass.get().strip(), self.cb_role.get()
        mail, edad = self.ent_mail.get().strip(), self.ent_edad.get().strip()
        if not u or not p: return
        try:
            res = json.loads(cli.registerUser(URL_SERVIDOR, u, p, r, mail, edad))
            if "message" in res and res["message"] == "registered":
                messagebox.showinfo("Completado", "Usuario creado. Ahora inicia sesión.")
                self.controller.mostrar_login()
            else: messagebox.showerror("Error", res.get('error'))
        except Exception as e: messagebox.showerror("Error", str(e))

class PantallaDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        rol = self.controller.rol_actual
        
        top_bar = tk.Frame(self, bg=COLOR_BARRA_TOP, height=60)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)
        tk.Label(top_bar, text="S.S.C. | MODO: " + rol.upper(), font=("Arial", 12, "bold"), bg=COLOR_BARRA_TOP, fg="white").pack(side="left", padx=20)
        tk.Button(top_bar, text="Cerrar Sesión", font=("Arial", 9, "bold"), bg="#ef4444", fg="white", bd=0, padx=15, pady=5, command=self.logout).pack(side="right", padx=20)
        tk.Label(top_bar, text=f"Hola, {self.controller.usuario_actual}", font=("Arial", 10, "italic"), bg=COLOR_BARRA_TOP, fg="#94a3b8").pack(side="right", padx=10)

        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=200)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)
        
        self.area_trabajo = tk.Frame(self, bg=COLOR_BG, padx=20, pady=15)
        self.area_trabajo.pack(fill="both", expand=True, side="left")
        
        # --- GENERADOR DINÁMICO DE BOTONES SEGÚN EL ROL ---
        opciones = [("👤 Mi Perfil", lambda: self.cargar_panel("Perfil"))]
        
        if rol in ["admin", "supervisor"]:
            opciones.append(("📝 Gestión Contratos", lambda: self.cargar_panel("Contratos_Full")))
            opciones.append(("📈 Avances de Obra", lambda: self.cargar_panel("Seguimientos_Full")))
            opciones.append(("📊 Estadísticas", lambda: self.cargar_panel("Estadísticas")))
            
        if rol == "viewer":
            opciones.append(("🔍 Mis Contratos", lambda: self.cargar_panel("Contratos_Viewer")))
            opciones.append(("⏱️ Ver Historial", lambda: self.cargar_panel("Seguimientos_Viewer")))
            
        if rol == "admin":
            opciones.append(("💾 Exportar CSV", lambda: self.cargar_panel("Exportar")))

        for texto, cmd in opciones:
            tk.Button(self.sidebar, text=f"  {texto}", font=("Arial", 11), bg=COLOR_SIDEBAR, fg="#e2e8f0", bd=0, anchor="w", height=2, cursor="hand2", command=cmd).pack(fill="x", padx=5, pady=2)

        self.cargar_panel("Perfil") # Pantalla por defecto

    def cargar_panel(self, nombre):
        for w in self.area_trabajo.winfo_children(): w.destroy()
        titulo = nombre.replace("_Full", "").replace("_Viewer", "")
        tk.Label(self.area_trabajo, text=titulo.upper(), font=("Arial", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0,10))
        
        if nombre == "Perfil": self.render_panel_perfil()
        elif nombre == "Contratos_Full": self.render_panel_contratos_full()
        elif nombre == "Contratos_Viewer": self.render_panel_contratos_viewer()
        elif nombre == "Seguimientos_Full": self.render_panel_seguimientos_full()
        elif nombre == "Seguimientos_Viewer": self.render_panel_seguimientos_viewer()
        elif nombre == "Estadísticas": self.render_panel_stats()
        elif nombre == "Exportar": self.render_panel_export()

    def logout(self):
        try: cli.closeSession(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual)
        except: pass
        self.controller.mostrar_login()

    # ==========================================================
    # NUEVO MÓDULO: PERFIL DE USUARIO
    # ==========================================================
    def render_panel_perfil(self):
        card = tk.Frame(self.area_trabajo, bg=COLOR_CARD, bd=1, relief="solid", padx=40, pady=30)
        card.pack(pady=20, fill="x")
        
        tk.Label(card, text="Información de la Cuenta Activa", font=("Arial", 14, "bold"), bg=COLOR_CARD, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0,15))
        
        # Muestra la info que trajimos de users.json al hacer Login
        info = [
            ("Nombre de Usuario:", self.controller.usuario_actual),
            ("Nivel de Permisos:", self.controller.rol_actual.upper()),
            ("Correo Electrónico:", self.controller.email_actual),
            ("Edad Registrada:", self.controller.edad_actual)
        ]
        
        for lbl, val in info:
            fila = tk.Frame(card, bg=COLOR_CARD)
            fila.pack(fill="x", pady=5)
            tk.Label(fila, text=lbl, font=("Arial", 10, "bold"), bg=COLOR_CARD, width=20, anchor="w").pack(side="left")
            tk.Label(fila, text=val, font=("Arial", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left")

    # ==========================================================
    # INTERFAZ 1: CONTRATOS PARA ADMIN/SUPERVISOR (Edición Total)
    # ==========================================================
    def render_panel_contratos_full(self):
        top_split = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        top_split.pack(fill="x", pady=(0, 10))
        
        form_frame = tk.LabelFrame(top_split, text=" Registrar / Editar Contrato ", bg=COLOR_CARD, font=("Arial", 10, "bold"), fg=COLOR_SIDEBAR, padx=10, pady=5)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        campos = [("N° Contrato:", "number"), ("Contratista:", "contractor"), 
                  ("Objeto Contractual:", "object"), ("F. Inicio (DD/MM/AAAA):", "start"),
                  ("F. Fin (DD/MM/AAAA):", "end"), ("Valor Neto ($):", "value"),
                  ("Supervisor:", "supervisor"), ("Email Contacto:", "email")]
        
        self.inputs_contrato = {}
        for i, (lbl, key) in enumerate(campos):
            r, c = i // 2, (i % 2) * 2
            tk.Label(form_frame, text=lbl, font=("Arial", 9), bg=COLOR_CARD).grid(row=r, column=c, sticky="w", pady=2, padx=4)
            ent = ttk.Entry(form_frame, font=("Arial", 9), width=20)
            ent.grid(row=r, column=c+1, pady=2, padx=4)
            self.inputs_contrato[key] = ent
            
        tk.Label(form_frame, text="Estado:", font=("Arial", 9), bg=COLOR_CARD).grid(row=4, column=0, sticky="w", pady=2, padx=4)
        self.cb_status = ttk.Combobox(form_frame, values=["ACTIVO", "SUSPENDIDO", "LIQUIDADO", "CONCLUIDO", "CANCELADO"], state="readonly", width=17, font=("Arial", 9))
        self.cb_status.current(0)
        self.cb_status.grid(row=4, column=1, pady=2, padx=4)
        
        btn_box = tk.Frame(form_frame, bg=COLOR_CARD)
        btn_box.grid(row=4, column=2, columnspan=2, sticky="e", pady=2, padx=4)
        tk.Button(btn_box, text="Crear Nuevo", font=("Arial", 9, "bold"), bg=COLOR_ACCENT, fg="white", bd=0, padx=8, command=self.api_registrar_contrato).pack(side="left", padx=2)
        tk.Button(btn_box, text="Actualizar", font=("Arial", 9, "bold"), bg="#f59e0b", fg="white", bd=0, padx=8, command=self.api_actualizar_contrato).pack(side="left", padx=2)

        self.crear_buscador_y_tabla(top_split, mostrar_carga=True)

    # ==========================================================
    # INTERFAZ 2: CONTRATOS PARA VIEWER (Solo Búsqueda y Cancelación)
    # ==========================================================
    def render_panel_contratos_viewer(self):
        # A los viewer no les mostramos ningún formulario de ingreso
        top_split = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        top_split.pack(fill="x", pady=(0, 10))
        self.crear_buscador_y_tabla(top_split, mostrar_carga=False)

    def crear_buscador_y_tabla(self, top_split, mostrar_carga):
        search_frame = tk.LabelFrame(top_split, text=" Buscador Rápido ", bg=COLOR_CARD, font=("Arial", 10, "bold"), fg=COLOR_SIDEBAR, padx=10, pady=5)
        search_frame.pack(side="right", fill="both")
        self.ent_search_num = ttk.Entry(search_frame, font=("Arial", 10), width=18)
        self.ent_search_num.pack(pady=4)
        tk.Button(search_frame, text="Buscar Código", font=("Arial", 9, "bold"), bg=COLOR_SIDEBAR, fg="white", bd=0, width=16, command=self.api_buscar_contrato).pack(pady=2)
        tk.Button(search_frame, text="Refrescar Lista", font=("Arial", 9), bg="#e2e8f0", bd=0, width=16, command=self.api_listar_contratos).pack(pady=2)

        tabla_frame = tk.Frame(self.area_trabajo, bg=COLOR_CARD, bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True)
        
        self.tabla_c = ttk.Treeview(tabla_frame, columns=("num", "con", "obj", "ini", "fin", "val", "est"), show="headings", selectmode="browse")
        for k, txt, w in [("num","N° Contrato",80), ("con","Contratista",130), ("obj","Objeto",200), ("ini","F. Inicio",85), ("fin","F. Fin",85), ("val","Valor",90), ("est","Estado",90)]:
            self.tabla_c.heading(k, text=txt)
            self.tabla_c.column(k, width=w, anchor="e" if k=="val" else "center" if k in ["num","ini","fin","est"] else "w")
            
        scr = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_c.yview)
        self.tabla_c.configure(yscrollcommand=scr.set)
        self.tabla_c.pack(fill="both", expand=True, side="left")
        scr.pack(fill="y", side="right")

        action_bar = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        action_bar.pack(fill="x", pady=5)
        
        if mostrar_carga:
            tk.Button(action_bar, text="✏️ Editar Fila (Pasar a Formulario)", font=("Arial", 9, "bold"), bg="#64748b", fg="white", bd=0, padx=10, pady=5, command=self.ui_cargar_fila_a_campos).pack(side="left", padx=5)
        
        # Este botón ROJO lo ven todos
        tk.Button(action_bar, text="🚫 CANCELAR CONTRATO", font=("Arial", 9, "bold"), bg="#dc2626", fg="white", bd=0, padx=10, pady=5, command=self.api_cancelar_contrato_forzado).pack(side="right", padx=5)
        
        self.api_listar_contratos()

    # --- LÓGICA DE ACTUALIZACIÓN CORREGIDA ---
    def api_actualizar_contrato(self):
        u, p = self.controller.usuario_actual, self.controller.password_actual
        vals = {k: v.get().strip() for k, v in self.inputs_contrato.items()}
        
        # Limpiar posible basura en el dinero por si el usuario le metió el signo $ manual
        valor_limpio = vals["value"].replace("$", "").replace(",", "")
        
        try:
            res = json.loads(cli.updateContract(URL_SERVIDOR, u, p, vals["number"], vals["contractor"], vals["object"], vals["start"], vals["end"], valor_limpio, vals["supervisor"], self.cb_status.get(), vals["email"]))
            if "message" in res and res["message"] == "updated":
                messagebox.showinfo("Éxito", f"Contrato {vals['number']} modificado exitosamente.")
                for entry in self.inputs_contrato.values(): entry.delete(0, tk.END)
                self.api_listar_contratos()
            else:
                # Mostrar el motivo exacto por el cual no deja modificar
                err = res.get("error", "Error desconocido")
                if "date format" in err: messagebox.showerror("Error", "La fecha debe ir exactamente en formato DD/MM/AAAA\nEjemplo: 25/12/2026")
                elif "invalid value" in err: messagebox.showerror("Error", "El valor del contrato debe ser solo números (Ej: 3500000)")
                else: messagebox.showerror("Denegado", f"Error del servidor: {err}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def ui_cargar_fila_a_campos(self):
        sel = self.tabla_c.selection()
        if not sel: return
        vals = self.tabla_c.item(sel[0], "values")
        try:
            res = json.loads(cli.searchContract(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, vals[0]))
            if "error" not in res:
                for k, entry in self.inputs_contrato.items():
                    entry.delete(0, tk.END)
                    if k in res: 
                        # Evitamos cargar valores formateados, usamos el crudo de la DB
                        entry.insert(0, str(int(res[k])) if k=="value" else str(res[k])) 
                self.cb_status.set(res.get("status", "ACTIVO"))
        except: pass

    # ... RESTO DE LA LÓGICA DE CONTRATOS (Cancelación, Lista, etc)...
    def api_registrar_contrato(self):
        u, p = self.controller.usuario_actual, self.controller.password_actual
        vals = {k: v.get().strip() for k, v in self.inputs_contrato.items()}
        try:
            res = json.loads(cli.registerContract(URL_SERVIDOR, u, p, vals["number"], vals["contractor"], vals["object"], vals["start"], vals["end"], vals["value"], vals["supervisor"], self.cb_status.get(), vals["email"]))
            if "message" in res and res["message"] == "registered":
                messagebox.showinfo("Éxito", "Registrado.")
                for entry in self.inputs_contrato.values(): entry.delete(0, tk.END)
                self.api_listar_contratos()
            else: messagebox.showerror("Error", res.get("error"))
        except: pass

    def api_cancelar_contrato_forzado(self):
        sel = self.tabla_c.selection()
        if not sel: return messagebox.showwarning("Atención", "Selecciona un contrato en la tabla.")
        num_c = self.tabla_c.item(sel[0], "values")[0]
        motivo = simpledialog.askstring("Gatillo de Cancelación", f"Motivo de cancelación de {num_c}:")
        if not motivo: return
        try:
            res = json.loads(cli.cancelContract(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, num_c, motivo))
            if "message" in res:
                messagebox.showwarning("Listo", f"El contrato {num_c} fue CANCELADO.")
                self.api_listar_contratos()
            else: messagebox.showerror("Error", res.get("error"))
        except: pass

    def api_listar_contratos(self):
        for item in self.tabla_c.get_children(): self.tabla_c.delete(item)
        try:
            res = json.loads(cli.listContracts(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual))
            if "contracts" in res:
                for c in res["contracts"]:
                    self.tabla_c.insert("", "end", values=(c["number"], c["contractor"], c["object"], c["start"], c["end"], f"${c['value']:,}", c["status"]))
        except: pass

    def api_buscar_contrato(self):
        num = self.ent_search_num.get().strip()
        if not num: return
        for item in self.tabla_c.get_children(): self.tabla_c.delete(item)
        try:
            res = json.loads(cli.searchContract(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, num))
            if "error" not in res: self.tabla_c.insert("", "end", values=(res["number"], res["contractor"], res["object"], res["start"], res["end"], f"${res['value']:,}", res["status"]))
        except: pass

    # ==========================================================
    # SEGUIMIENTOS DINÁMICOS
    # ==========================================================
    def render_panel_seguimientos_full(self):
        top_split = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        top_split.pack(fill="x", pady=(0, 10))
        form_frame = tk.LabelFrame(top_split, text=" Añadir Avance ", bg=COLOR_CARD, font=("Arial", 10, "bold"), fg=COLOR_SIDEBAR, padx=10, pady=5)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        tk.Label(form_frame, text="N° Contrato:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_t_num = ttk.Entry(form_frame, font=("Arial", 9), width=15)
        self.ent_t_num.grid(row=0, column=1, pady=2)
        
        tk.Label(form_frame, text="Fecha (DD/MM/AAAA):").grid(row=0, column=2, sticky="w", pady=2)
        self.ent_t_date = ttk.Entry(form_frame, font=("Arial", 9), width=15)
        self.ent_t_date.grid(row=0, column=3, pady=2)
        
        tk.Label(form_frame, text="% Avance:").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_t_prog = ttk.Entry(form_frame, font=("Arial", 9), width=15)
        self.ent_t_prog.grid(row=1, column=1, pady=2)
        
        tk.Label(form_frame, text="Descripción:").grid(row=1, column=2, sticky="w", pady=2)
        self.ent_t_desc = ttk.Entry(form_frame, font=("Arial", 9), width=15)
        self.ent_t_desc.grid(row=1, column=3, pady=2)
        
        tk.Button(form_frame, text="Registrar", font=("Arial", 9, "bold"), bg=COLOR_SUCCESS, fg="white", bd=0, command=self.api_add_tracking).grid(row=2, column=3, sticky="e", pady=5)
        self.crear_historial_seguimientos(top_split)

    def render_panel_seguimientos_viewer(self):
        # Viewer NO puede añadir avances, solo ver
        top_split = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        top_split.pack(fill="x", pady=(0, 10))
        self.crear_historial_seguimientos(top_split)

    def crear_historial_seguimientos(self, top_split):
        view_frame = tk.LabelFrame(top_split, text=" Ver Historial ", bg=COLOR_CARD, font=("Arial", 10, "bold"), fg=COLOR_SIDEBAR, padx=10, pady=5)
        view_frame.pack(side="right", fill="both", expand=True)
        self.ent_query_t = ttk.Entry(view_frame, font=("Arial", 10), width=15)
        self.ent_query_t.pack(pady=2)
        tk.Button(view_frame, text="Consultar por Código", font=("Arial", 9, "bold"), bg=COLOR_SIDEBAR, fg="white", bd=0, width=18, command=self.api_query_trackings).pack(pady=2)
        self.lbl_avg_display = tk.Label(view_frame, text="Promedio: -- %", font=("Arial", 10, "bold"), bg="#eff6ff", fg=COLOR_ACCENT, width=15)
        self.lbl_avg_display.pack(pady=2)

        tabla_frame = tk.Frame(self.area_trabajo, bg=COLOR_CARD, bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True)
        self.tabla_t = ttk.Treeview(tabla_frame, columns=("id", "fecha", "avance", "desc"), show="headings", selectmode="browse")
        for k, t, w in [("id","ID",40), ("fecha","Fecha",90), ("avance","% Avance",80), ("desc","Descripción y Obs.",400)]:
            self.tabla_t.heading(k, text=t)
            self.tabla_t.column(k, width=w, anchor="center" if k in ["id","fecha","avance"] else "w")
        scr = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_t.yview)
        self.tabla_t.configure(yscrollcommand=scr.set)
        self.tabla_t.pack(fill="both", expand=True, side="left")
        scr.pack(fill="y", side="right")

    def api_add_tracking(self):
        try:
            res = json.loads(cli.addTracking(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, self.ent_t_num.get().strip(), self.ent_t_date.get().strip(), self.ent_t_desc.get().strip(), self.ent_t_prog.get().strip(), "N/A"))
            if "message" in res and res["message"] == "added":
                messagebox.showinfo("Éxito", "Avance ingresado.")
            else: messagebox.showerror("Error", res.get("error"))
        except Exception as e: messagebox.showerror("Error", str(e))

    def api_query_trackings(self):
        num = self.ent_query_t.get().strip()
        if not num: return
        for item in self.tabla_t.get_children(): self.tabla_t.delete(item)
        try:
            res = json.loads(cli.listTrackings(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, num))
            if "trackings" in res:
                for t in res["trackings"]: self.tabla_t.insert("", "end", values=(t["id"], t["date"], f"{t['progress']}%", t["desc"] + " | " + t.get("obs","")))
            avg_res = json.loads(cli.avgProgress(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual, num))
            if "avg" in avg_res: self.lbl_avg_display.config(text=f"Promedio: {avg_res['avg']:.1f} %")
        except: pass

    # ==========================================================
    # ESTADÍSTICAS Y EXPORT (Igual que antes)
    # ==========================================================
    def render_panel_stats(self):
        self.frame_cards = tk.Frame(self.area_trabajo, bg=COLOR_BG)
        self.frame_cards.pack(fill="x", pady=5)
        self.frame_alerts = tk.LabelFrame(self.area_trabajo, text=" Contratos por vencer en 30 días ", bg=COLOR_CARD, font=("Arial", 10, "bold"), fg="#b91c1c", padx=10, pady=5)
        self.frame_alerts.pack(fill="both", expand=True, pady=5)
        self.txt_alerts = tk.Text(self.frame_alerts, font=("Consolas", 9), bg="#fef2f2", fg="#991b1b", bd=0, height=6)
        self.txt_alerts.pack(fill="both", expand=True)
        self.after(200, self.api_cargar_estadisticas)

    def api_cargar_estadisticas(self):
        try:
            res = json.loads(cli.stats(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual))
            if not res: return
            self.crear_kpi_card(self.frame_cards, "Monto Total Invertido", f"${res.get('total_value',0):,.1f}", COLOR_ACCENT).pack(side="left", padx=5, fill="x", expand=True)
            self.crear_kpi_card(self.frame_cards, "Monto Promedio", f"${res.get('avg_value',0):,.1f}", COLOR_SUCCESS).pack(side="left", padx=5, fill="x", expand=True)
            status_str = "\n".join([f"• {k}: {v}" for k, v in res.get("total_by_status", {}).items()])
            self.crear_kpi_card(self.frame_cards, "Estados Actuales", status_str, COLOR_SIDEBAR).pack(side="left", padx=5, fill="x", expand=True)
            self.txt_alerts.delete("1.0", tk.END)
            near = res.get("near_expiry", [])
            if near:
                for n in near: self.txt_alerts.insert(tk.END, f"[⚠️ ALERTA] Contrato N° {n} expira pronto.\n")
            else: self.txt_alerts.insert(tk.END, "Sin alertas.")
        except: pass

    def crear_kpi_card(self, parent, tit, val, col):
        c = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e2e8f0", height=100)
        c.pack_propagate(False)
        tk.Frame(c, bg=col, height=4).pack(fill="x", side="top")
        tk.Label(c, text=tit, font=("Arial", 9, "bold"), bg=COLOR_CARD, fg="#64748b").pack(pady=4)
        tk.Label(c, text=val, font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, justify="center").pack(pady=2)
        return c

    def render_panel_export(self):
        card = tk.Frame(self.area_trabajo, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e2e8f0", padx=30, pady=30)
        card.pack(pady=20)
        tk.Label(card, text="Respaldo General (.CSV)", font=("Arial", 14, "bold"), bg=COLOR_CARD).pack(pady=5)
        tk.Button(card, text="Exportar Base de Datos Completa", font=("Arial", 11, "bold"), bg=COLOR_ACCENT, fg="white", bd=0, padx=20, pady=8, command=self.api_exportar_csv).pack(pady=5)

    def api_exportar_csv(self):
        try:
            res = json.loads(cli.exportCsv(URL_SERVIDOR, self.controller.usuario_actual, self.controller.password_actual))
            if "message" in res: messagebox.showinfo("Éxito", "Archivos guardados.")
            else: messagebox.showerror("Denegado", res.get("error"))
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    SistemaSupervisionApp().mainloop()