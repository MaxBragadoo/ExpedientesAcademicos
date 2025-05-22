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

class EditarMiembroScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.current_student = None
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los componentes de la interfaz"""
        # Configuración de estilos
        button_style = {
            "height": 38,
            "corner_radius": 8,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "border_width": 1
        }
        
        entry_style = {
            "height": 36,
            "corner_radius": 6,
            "font": ctk.CTkFont(size=13),
            "border_width": 1
        }
        
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Editar Estudiante",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 15))
        
        # Panel de búsqueda
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por ID, nombre, apellido o carrera...",
            width=350,
            **entry_style
        ).pack(side="left", padx=(0, 10))
        
        # Botón de búsqueda
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            fg_color=("#5a6b8a", "#4a5b7a"),  # Azul grisáceo formal
            hover_color=("#4a5b7a", "#3a4b6a"),
            border_color=("#4a5b7a", "#3a4b6a"),
            width=120,
            command=self.buscar_estudiantes,
            **button_style
        ).pack(side="left", padx=5)
        
        # Lista de resultados
        self.results_frame = ctk.CTkScrollableFrame(
            self.frame, 
            height=180,
            fg_color=("#f8f8f8", "#2a2a2a")
        )
        self.results_frame.pack(fill="x", padx=20, pady=10)
        
        # Formulario de edición
        self.form_frame = ctk.CTkFrame(
            self.frame,
            fg_color=("#f0f0f0", "#333333"),
            corner_radius=10
        )
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        
        ctk.CTkButton(
            button_frame,
            text="Guardar Cambios",
            fg_color=("#4a7c59", "#3a6b49"),  # Verde oscuro formal
            hover_color=("#3a6b49", "#2a5a39"),
            border_color=("#3a6b49", "#2a5a39"),
            width=150,
            command=self.guardar_cambios,
            **button_style
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color=("#8a4a4a", "#7a3a3a"),  # Rojo vino formal
            hover_color=("#7a3a3a", "#6a2a2a"),
            border_color=("#7a3a3a", "#6a2a2a"),
            width=120,
            command=self.cerrar,
            **button_style
        ).pack(side="left", padx=10)
        
        # Inicialmente ocultar el formulario
        self.mostrar_formulario(False)
    
    def buscar_estudiantes(self):
        """Busca estudiantes en la base de datos"""
        termino = self.search_var.get().strip()
        
        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not termino:
            messagebox.showwarning("Búsqueda vacía", "Ingrese un ID, nombre, apellido o carrera para buscar")
            return
        
        # Obtener resultados de la base de datos
        resultados = self.obtener_estudiantes_db(termino)
        
        if not resultados:
            ctk.CTkLabel(
                self.results_frame,
                text="No se encontraron estudiantes",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10)
            return
        
        # Mostrar resultados
        for idx, estudiante in enumerate(resultados):
            # Alternar colores de fondo para mejor legibilidad
            bg_color = ("#ffffff", "#2a2a2a") if idx % 2 == 0 else ("#f0f0f0", "#333333")
            
            student_frame = ctk.CTkFrame(
                self.results_frame,
                fg_color=bg_color,
                height=40,
                corner_radius=6
            )
            student_frame.pack(fill="x", pady=2)
            
            # Mostrar información básica
            info_text = f"ID: {estudiante['id']} - {estudiante['nombre']} {estudiante['apellido']} ({estudiante['carrera']})"
            
            ctk.CTkLabel(
                student_frame,
                text=info_text,
                font=ctk.CTkFont(size=12),
                text_color=("#333333", "#ffffff")
            ).pack(side="left", padx=10, expand=True, fill="x")
            
            # Botón de selección
            ctk.CTkButton(
                student_frame,
                text="Seleccionar",
                fg_color=("#5a6b8a", "#4a5b7a"),  # Azul grisáceo formal
                hover_color=("#4a5b7a", "#3a4b6a"),
                border_color=("#4a5b7a", "#3a4b6a"),
                width=100,
                height=30,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda e=estudiante: self.cargar_estudiante(e)
            ).pack(side="right", padx=5)
    
    def cargar_estudiante(self, estudiante):
        """Carga los datos del estudiante en el formulario"""
        self.current_student = estudiante
        self.mostrar_formulario(True)
        
        # Limpiar formulario primero
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        # Crear formulario de edición
        self.crear_formulario_edicion()
        
        # Cargar datos
        self.cargar_datos_formulario(estudiante)
    
    def crear_formulario_edicion(self):
        """Crea los campos del formulario de edición"""
        # Configuración de estilos
        label_style = {
            "font": ctk.CTkFont(size=13, weight="bold"),
            "text_color": ("#555555", "#dddddd")
        }
        
        entry_style = {
            "height": 36,
            "corner_radius": 6,
            "font": ctk.CTkFont(size=13),
            "border_width": 1
        }
        
        # Configurar grid
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(2, minsize=20)  # Espacio entre columnas
        row = 0
        
        # Título del formulario
        ctk.CTkLabel(
            self.form_frame,
            text=f"Editando: {self.current_student['nombre']} {self.current_student['apellido']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#333333", "#ffffff")
        ).grid(row=row, column=0, columnspan=3, pady=(15, 20), padx=15, sticky="w")
        row += 1
        
        # ID (no editable)
        ctk.CTkLabel(self.form_frame, text="ID:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.id_label = ctk.CTkLabel(
            self.form_frame, 
            text="", 
            font=ctk.CTkFont(size=13),
            text_color=("#333333", "#ffffff")
        )
        self.id_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1
        
        # Nombre
        ctk.CTkLabel(self.form_frame, text="Nombre(s):", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.nombre_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Apellido
        ctk.CTkLabel(self.form_frame, text="Apellido:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.apellido_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.apellido_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Carrera
        ctk.CTkLabel(self.form_frame, text="Carrera:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.carrera_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.carrera_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Fecha de Nacimiento
        ctk.CTkLabel(self.form_frame, text="Fecha Nacimiento:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.fecha_nac_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="AAAA-MM-DD",
            **entry_style
        )
        self.fecha_nac_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Género
        ctk.CTkLabel(self.form_frame, text="Género:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.genero_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Masculino", "Femenino", "Otro"],
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            border_width=1
        )
        self.genero_combobox.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Nacionalidad
        ctk.CTkLabel(self.form_frame, text="Nacionalidad:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.nacionalidad_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.nacionalidad_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Dirección
        ctk.CTkLabel(self.form_frame, text="Dirección:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.direccion_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.direccion_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Teléfono
        ctk.CTkLabel(self.form_frame, text="Teléfono:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.telefono_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Correo Electrónico
        ctk.CTkLabel(self.form_frame, text="Correo Electrónico:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.correo_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.correo_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Nombre
        ctk.CTkLabel(self.form_frame, text="Contacto Emergencia:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.contacto_nombre_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.contacto_nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Relación
        ctk.CTkLabel(self.form_frame, text="Relación:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.contacto_relacion_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.contacto_relacion_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Teléfono
        ctk.CTkLabel(self.form_frame, text="Teléfono Emergencia:", **label_style).grid(row=row, column=0, padx=15, pady=5, sticky="e")
        self.contacto_telefono_entry = ctk.CTkEntry(self.form_frame, **entry_style)
        self.contacto_telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
    
    def cargar_datos_formulario(self, estudiante):
        """Carga los datos del estudiante en los campos del formulario"""
        self.id_label.configure(text=str(estudiante['id']))
        self.nombre_entry.insert(0, estudiante['nombre'])
        self.apellido_entry.insert(0, estudiante['apellido'])
        self.carrera_entry.insert(0, estudiante['carrera'])
        self.fecha_nac_entry.insert(0, estudiante['fecha_nacimiento'].strftime('%Y-%m-%d'))
        self.genero_combobox.set(estudiante['genero'])
        self.nacionalidad_entry.insert(0, estudiante['nacionalidad'])
        self.direccion_entry.insert(0, estudiante['direccion'])
        self.telefono_entry.insert(0, estudiante['telefono'])
        self.correo_entry.insert(0, estudiante['correo_electronico'])
        self.contacto_nombre_entry.insert(0, estudiante['contacto_emergencia_nombre'])
        self.contacto_relacion_entry.insert(0, estudiante['contacto_emergencia_relacion'])
        self.contacto_telefono_entry.insert(0, estudiante['contacto_emergencia_telefono'])
    
    def guardar_cambios(self):
        """Guarda los cambios del estudiante en la base de datos"""
        if not self.current_student:
            messagebox.showwarning("Error", "No hay ningún estudiante seleccionado")
            return
        
        # Validar campos obligatorios
        if not all([
            self.nombre_entry.get().strip(),
            self.apellido_entry.get().strip(),
            self.carrera_entry.get().strip(),
            self.fecha_nac_entry.get().strip(),
            self.genero_combobox.get().strip(),
            self.nacionalidad_entry.get().strip(),
            self.direccion_entry.get().strip(),
            self.telefono_entry.get().strip(),
            self.correo_entry.get().strip(),
            self.contacto_nombre_entry.get().strip(),
            self.contacto_relacion_entry.get().strip(),
            self.contacto_telefono_entry.get().strip()
        ]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            'id': self.current_student['id'],
            'nombre': self.nombre_entry.get().strip(),
            'apellido': self.apellido_entry.get().strip(),
            'carrera': self.carrera_entry.get().strip(),
            'fecha_nacimiento': self.fecha_nac_entry.get().strip(),
            'genero': self.genero_combobox.get(),
            'nacionalidad': self.nacionalidad_entry.get().strip(),
            'direccion': self.direccion_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip(),
            'correo_electronico': self.correo_entry.get().strip(),
            'contacto_emergencia_nombre': self.contacto_nombre_entry.get().strip(),
            'contacto_emergencia_relacion': self.contacto_relacion_entry.get().strip(),
            'contacto_emergencia_telefono': self.contacto_telefono_entry.get().strip()
        }
        
        # Actualizar en la base de datos
        if self.actualizar_estudiante_db(datos_actualizados):
            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente")
            self.cerrar()
    
    def actualizar_estudiante_db(self, estudiante_data):
        """Actualiza un estudiante en la base de datos"""
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return False
        
        try:
            cursor = conexion.cursor()
            
            query = """
            UPDATE estudiantes SET
                nombre = %s,
                apellido = %s,
                carrera = %s,
                fecha_nacimiento = %s,
                genero = %s,
                nacionalidad = %s,
                direccion = %s,
                telefono = %s,
                correo_electronico = %s,
                contacto_emergencia_nombre = %s,
                contacto_emergencia_relacion = %s,
                contacto_emergencia_telefono = %s
            WHERE id = %s
            """
            
            cursor.execute(query, (
                estudiante_data['nombre'],
                estudiante_data['apellido'],
                estudiante_data['carrera'],
                estudiante_data['fecha_nacimiento'],
                estudiante_data['genero'],
                estudiante_data['nacionalidad'],
                estudiante_data['direccion'],
                estudiante_data['telefono'],
                estudiante_data['correo_electronico'],
                estudiante_data['contacto_emergencia_nombre'],
                estudiante_data['contacto_emergencia_relacion'],
                estudiante_data['contacto_emergencia_telefono'],
                estudiante_data['id']
            ))
            
            conexion.commit()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {str(e)}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
    
    def mostrar_formulario(self, mostrar):
        """Muestra u oculta el formulario"""
        if mostrar:
            self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        else:
            self.form_frame.pack_forget()
    
    def obtener_estudiantes_db(self, termino):
        """Obtiene estudiantes de la base de datos MySQL"""
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        try:
            cursor = conexion.cursor(dictionary=True)
            
            query = """
            SELECT * FROM estudiantes 
            WHERE id LIKE %s OR 
                  nombre LIKE %s OR 
                  apellido LIKE %s OR 
                  carrera LIKE %s
            """
            params = (f"%{termino}%", f"%{termino}%", f"%{termino}%", f"%{termino}%")
            cursor.execute(query, params)
            
            return cursor.fetchall()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar estudiantes: {str(e)}")
            return []
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
    
    def cerrar(self):
        """Cierra esta pantalla"""
        self.frame.pack_forget()