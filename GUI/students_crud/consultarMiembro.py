import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='gestion_academica'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

class ConsultarEstudiantesScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los componentes de la interfaz"""
        # Configuración de estilos
        button_style = {
            "height": 38,
            "corner_radius": 8,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "border_width": 1,
            "hover": True
        }
        
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Consulta de Estudiantes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 15))
        
        # Panel de filtros
        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por ID, nombre, apellido o carrera...",
            width=350,
            height=38,
            font=ctk.CTkFont(size=14),
            border_width=1,
            corner_radius=8
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Botones de filtro
        ctk.CTkButton(
            filter_frame,
            text="Buscar",
            fg_color=("#5a6b8a", "#4a5b7a"),  # Azul grisáceo formal
            hover_color=("#4a5b7a", "#3a4b6a"),
            border_color=("#4a5b7a", "#3a4b6a"),
            width=120,
            command=self.filtrar_estudiantes,
            **button_style
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Mostrar Todos",
            fg_color=("#6a5a8a", "#5a4a7a"),  # Púrpura oscuro formal
            hover_color=("#5a4a7a", "#4a3a6a"),
            border_color=("#5a4a7a", "#4a3a6a"),
            width=120,
            command=self.mostrar_todos,
            **button_style
        ).pack(side="left", padx=5)
        
        # Lista de estudiantes
        self.list_container = ctk.CTkScrollableFrame(
            self.frame, 
            height=400,
            fg_color=("#f8f8f8", "#2a2a2a")
        )
        self.list_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón de volver
        ctk.CTkButton(
            self.frame,
            text="Volver",
            fg_color=("#8a4a4a", "#7a3a3a"),  # Rojo vino formal
            hover_color=("#7a3a3a", "#6a2a2a"),
            border_color=("#7a3a3a", "#6a2a2a"),
            width=120,
            command=self.cerrar,
            **button_style
        ).pack(pady=(10, 20))
        
        # Cargar todos los estudiantes inicialmente
        self.mostrar_todos()
    
    def mostrar_todos(self):
        """Muestra todos los estudiantes sin filtros"""
        self.search_var.set("")
        self.filtrar_estudiantes()
    
    def filtrar_estudiantes(self):
        """Filtra los estudiantes según el texto ingresado"""
        termino = self.search_var.get().strip().lower()
        
        # Limpiar lista actual
        for widget in self.list_container.winfo_children():
            widget.destroy()
        
        # Obtener estudiantes de la base de datos
        estudiantes = self.obtener_estudiantes_db(termino)
        
        if not estudiantes:
            ctk.CTkLabel(
                self.list_container,
                text="No se encontraron estudiantes",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        # Crear encabezados de la tabla
        header_frame = ctk.CTkFrame(
            self.list_container,
            fg_color=("#e0e0e0", "#3a3a3a"),
            height=40,
            corner_radius=6
        )
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = ["ID", "Nombre", "Apellido", "Carrera", "Teléfono", "Correo", "Acciones"]
        column_widths = [50, 120, 120, 100, 100, 150, 80]  # Anchos personalizados para cada columna
        
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=column_widths[i],
                text_color=("#333333", "#ffffff")
            ).grid(row=0, column=i, padx=2, sticky="w")
        
        # Mostrar cada estudiante
        for idx, estudiante in enumerate(estudiantes):
            # Alternar colores de fondo para mejor legibilidad
            bg_color = ("#ffffff", "#2a2a2a") if idx % 2 == 0 else ("#f0f0f0", "#333333")
            self.crear_item_estudiante(estudiante, column_widths, bg_color)
    
    def crear_item_estudiante(self, estudiante, column_widths, bg_color):
        """Crea un item de estudiante en la lista"""
        item_frame = ctk.CTkFrame(
            self.list_container,
            fg_color=bg_color,
            height=40,
            corner_radius=6
        )
        item_frame.pack(fill="x", pady=2)
        
        # Configurar grid para el item
        for i in range(len(column_widths)-1):  # -1 porque la última columna es de acciones
            item_frame.grid_columnconfigure(i, minsize=column_widths[i])
        
        # ID
        ctk.CTkLabel(
            item_frame,
            text=str(estudiante['id']),
            width=column_widths[0],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=2, sticky="w")
        
        # Nombre
        ctk.CTkLabel(
            item_frame,
            text=estudiante['nombre'],
            width=column_widths[1],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=1, padx=2, sticky="w")
        
        # Apellido
        ctk.CTkLabel(
            item_frame,
            text=estudiante['apellido'],
            width=column_widths[2],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=2, sticky="w")
        
        # Carrera
        ctk.CTkLabel(
            item_frame,
            text=estudiante['carrera'],
            width=column_widths[3],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=3, padx=2, sticky="w")
        
        # Teléfono
        ctk.CTkLabel(
            item_frame,
            text=estudiante['telefono'],
            width=column_widths[4],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=4, padx=2, sticky="w")
        
        # Correo
        ctk.CTkLabel(
            item_frame,
            text=estudiante['correo_electronico'],
            width=column_widths[5],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=5, padx=2, sticky="w")
        
        # Botón de seleccionar
        ctk.CTkButton(
            item_frame,
            text="Ver",
            fg_color=("#4a7c59", "#3a6b49"),  # Verde oscuro formal
            hover_color=("#3a6b49", "#2a5a39"),
            border_color=("#3a6b49", "#2a5a39"),
            width=column_widths[6]-10,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda e=estudiante: self.mostrar_detalles(e)
        ).grid(row=0, column=6, padx=2)
    
    def mostrar_detalles(self, estudiante):
        """Muestra los detalles completos del estudiante"""
        # Limpiar la lista
        for widget in self.list_container.winfo_children():
            widget.destroy()
        
        # Botón para volver a la lista
        ctk.CTkButton(
            self.list_container,
            text="← Volver a la lista",
            fg_color=("#5a6b8a", "#4a5b7a"),  # Azul grisáceo formal
            hover_color=("#4a5b7a", "#3a4b6a"),
            border_color=("#4a5b7a", "#3a4b6a"),
            width=150,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.filtrar_estudiantes
        ).pack(pady=(0, 20), anchor="w")
        
        # Marco para los detalles
        details_frame = ctk.CTkFrame(
            self.list_container,
            fg_color=("#f0f0f0", "#333333"),
            corner_radius=10
        )
        details_frame.pack(fill="x", pady=10, padx=10)
        
        # Título de detalles
        ctk.CTkLabel(
            details_frame,
            text=f"Detalles del Estudiante: {estudiante['nombre']} {estudiante['apellido']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#333333", "#ffffff")
        ).pack(pady=(15, 10), padx=15, anchor="w")
        
        # Mostrar todos los campos del estudiante
        campos = [
            ("ID", estudiante['id']),
            ("Nombre", estudiante['nombre']),
            ("Apellido", estudiante['apellido']),
            ("Carrera", estudiante['carrera']),
            ("Fecha de Nacimiento", estudiante['fecha_nacimiento'].strftime('%Y-%m-%d')),
            ("Género", estudiante['genero']),
            ("Nacionalidad", estudiante['nacionalidad']),
            ("Dirección", estudiante['direccion']),
            ("Teléfono", estudiante['telefono']),
            ("Correo Electrónico", estudiante['correo_electronico']),
            ("Contacto Emergencia", f"{estudiante['contacto_emergencia_nombre']} ({estudiante['contacto_emergencia_relacion']})"),
            ("Teléfono Emergencia", estudiante['contacto_emergencia_telefono'])
        ]
        
        for i, (campo, valor) in enumerate(campos):
            row_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3, padx=15)
            
            ctk.CTkLabel(
                row_frame,
                text=f"{campo}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=180,
                anchor="e",
                text_color=("#555555", "#dddddd")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=ctk.CTkFont(size=13),
                wraplength=400,
                justify="left",
                text_color=("#333333", "#ffffff")
            ).pack(side="left", padx=5)
    
    def obtener_estudiantes_db(self, filtro=None):
        """Obtiene estudiantes de la base de datos MySQL"""
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        try:
            cursor = conexion.cursor(dictionary=True)
            
            if filtro:
                query = """
                SELECT * FROM estudiantes 
                WHERE id LIKE %s OR 
                      nombre LIKE %s OR 
                      apellido LIKE %s OR 
                      carrera LIKE %s
                """
                params = (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%")
                cursor.execute(query, params)
            else:
                cursor.execute("SELECT * FROM estudiantes")
            
            estudiantes = cursor.fetchall()
            return estudiantes
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estudiantes: {str(e)}")
            return []
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
    
    def cerrar(self):
        """Cierra esta pantalla"""
        self.frame.pack_forget()