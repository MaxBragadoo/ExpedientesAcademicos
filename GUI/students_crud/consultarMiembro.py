import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
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
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Consulta de Estudiantes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Panel de filtros
        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por ID, nombre, apellido o carrera...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Botones de filtro
        ctk.CTkButton(
            filter_frame,
            text="Buscar",
            width=100,
            command=self.filtrar_estudiantes
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Mostrar Todos",
            width=100,
            command=self.mostrar_todos
        ).pack(side="left", padx=5)
        
        # Lista de estudiantes
        self.list_container = ctk.CTkScrollableFrame(self.frame, height=400)
        self.list_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón de volver
        ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.cerrar
        ).pack(pady=20)
        
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
        header_frame = ctk.CTkFrame(self.list_container)
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = ["ID", "Nombre", "Apellido", "Carrera", "Teléfono", "Correo", "Acciones"]
        column_widths = [50, 120, 120, 100, 100, 150, 80]  # Anchos personalizados para cada columna
        
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=column_widths[i]
            ).grid(row=0, column=i, padx=2, sticky="w")
        
        # Mostrar cada estudiante
        for estudiante in estudiantes:
            self.crear_item_estudiante(estudiante, column_widths)
    
    def crear_item_estudiante(self, estudiante, column_widths):
        """Crea un item de estudiante en la lista"""
        item_frame = ctk.CTkFrame(self.list_container)
        item_frame.pack(fill="x", pady=2)
        
        # Configurar grid para el item
        for i in range(len(column_widths)-1):  # -1 porque la última columna es de acciones
            item_frame.grid_columnconfigure(i, minsize=column_widths[i])
        
        # ID
        ctk.CTkLabel(
            item_frame,
            text=str(estudiante['id']),
            width=column_widths[0]
        ).grid(row=0, column=0, padx=2, sticky="w")
        
        # Nombre
        ctk.CTkLabel(
            item_frame,
            text=estudiante['nombre'],
            width=column_widths[1]
        ).grid(row=0, column=1, padx=2, sticky="w")
        
        # Apellido
        ctk.CTkLabel(
            item_frame,
            text=estudiante['apellido'],
            width=column_widths[2]
        ).grid(row=0, column=2, padx=2, sticky="w")
        
        # Carrera
        ctk.CTkLabel(
            item_frame,
            text=estudiante['carrera'],
            width=column_widths[3]
        ).grid(row=0, column=3, padx=2, sticky="w")
        
        # Teléfono
        ctk.CTkLabel(
            item_frame,
            text=estudiante['telefono'],
            width=column_widths[4]
        ).grid(row=0, column=4, padx=2, sticky="w")
        
        # Correo
        ctk.CTkLabel(
            item_frame,
            text=estudiante['correo_electronico'],
            width=column_widths[5]
        ).grid(row=0, column=5, padx=2, sticky="w")
        
        # Botón de seleccionar
        ctk.CTkButton(
            item_frame,
            text="Ver",
            width=column_widths[6],
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
            text="Volver a la lista",
            command=self.filtrar_estudiantes
        ).pack(pady=(0, 20), anchor="w")
        
        # Marco para los detalles
        details_frame = ctk.CTkFrame(self.list_container)
        details_frame.pack(fill="x", pady=10, padx=10)
        
        # Mostrar todos los campos del estudiante
        campos = [
            ("ID", estudiante['id']),
            ("Nombre", estudiante['nombre']),
            ("Apellido", estudiante['apellido']),  # Nuevo campo
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
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row_frame,
                text=f"{campo}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=180,
                anchor="e"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=ctk.CTkFont(size=12),
                wraplength=400,
                justify="left"
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