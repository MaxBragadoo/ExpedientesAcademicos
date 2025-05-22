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

class EliminarMiembroScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.current_student = None
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los componentes de la interfaz"""
        # Título
        ctk.CTkLabel(
            self.frame,
            text="Eliminar Miembro",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Panel de búsqueda
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por ID, nombre o carrera...",
            width=300
        ).pack(side="left", padx=(0, 10))
        
        # Botones de búsqueda
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=100,
            command=self.buscar_estudiantes
        ).pack(side="left", padx=5)
        
        # Lista de resultados
        self.results_frame = ctk.CTkScrollableFrame(self.frame, height=150)
        self.results_frame.pack(fill="x", padx=20, pady=10)
        
        # Panel de detalles
        self.details_frame = ctk.CTkFrame(self.frame)
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Eliminar Miembro",
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self.confirmar_eliminacion
        )
        self.delete_button.pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cerrar
        ).pack(side="left", padx=10)
        
        # Inicialmente ocultar detalles y botón de eliminar
        self.mostrar_detalles(False)
        self.delete_button.configure(state="disabled")
    
    def buscar_estudiantes(self):
        """Busca estudiantes en la base de datos"""
        termino = self.search_var.get().strip()
        
        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not termino:
            messagebox.showwarning("Búsqueda vacía", "Ingrese un ID, nombre o carrera para buscar")
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
        for estudiante in resultados:
            student_frame = ctk.CTkFrame(self.results_frame)
            student_frame.pack(fill="x", pady=2)
            
            # Mostrar información básica
            info_text = f"ID: {estudiante['id']} - {estudiante['nombre']} ({estudiante['carrera']})"
            
            ctk.CTkLabel(
                student_frame,
                text=info_text,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
            
            # Botón de selección
            ctk.CTkButton(
                student_frame,
                text="Seleccionar",
                width=100,
                command=lambda e=estudiante: self.mostrar_datos_estudiante(e)
            ).pack(side="right", padx=5)
    
    def mostrar_datos_estudiante(self, estudiante):
        """Muestra los detalles del estudiante seleccionado"""
        self.current_student = estudiante
        self.mostrar_detalles(True)
        self.delete_button.configure(state="normal")
        
        # Limpiar detalles anteriores
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Mostrar detalles del estudiante
        detalles = [
            ("ID:", estudiante['id']),
            ("Nombre:", estudiante['nombre']),
            ("Carrera:", estudiante['carrera']),
            ("Fecha Nacimiento:", estudiante['fecha_nacimiento'].strftime('%Y-%m-%d')),
            ("Género:", estudiante['genero']),
            ("Nacionalidad:", estudiante['nacionalidad']),
            ("Dirección:", estudiante['direccion']),
            ("Teléfono:", estudiante['telefono']),
            ("Correo:", estudiante['correo_electronico']),
            ("Contacto Emergencia:", f"{estudiante['contacto_emergencia_nombre']} ({estudiante['contacto_emergencia_relacion']})"),
            ("Teléfono Emergencia:", estudiante['contacto_emergencia_telefono'])
        ]
        
        for i, (campo, valor) in enumerate(detalles):
            row_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row_frame,
                text=campo,
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
    
    def confirmar_eliminacion(self):
        """Muestra confirmación antes de eliminar"""
        if not self.current_student:
            return
            
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar permanentemente a {self.current_student['nombre']} (ID: {self.current_student['id']})?\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            self.eliminar_estudiante()
    
    def eliminar_estudiante(self):
        """Elimina el estudiante de la base de datos"""
        if not self.current_student:
            return
        
        if self.eliminar_estudiante_db(self.current_student['id']):
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
            self.current_student = None
            self.mostrar_detalles(False)
            self.delete_button.configure(state="disabled")
            self.buscar_estudiantes()  # Actualizar lista
    
    def eliminar_estudiante_db(self, estudiante_id):
        """Elimina un estudiante de la base de datos"""
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return False
        
        try:
            cursor = conexion.cursor()
            
            query = "DELETE FROM estudiantes WHERE id = %s"
            cursor.execute(query, (estudiante_id,))
            
            conexion.commit()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el estudiante: {str(e)}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
    
    def mostrar_detalles(self, mostrar):
        """Muestra u oculta el panel de detalles"""
        if mostrar:
            self.details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        else:
            self.details_frame.pack_forget()
    
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
                  carrera LIKE %s
            """
            params = (f"%{termino}%", f"%{termino}%", f"%{termino}%")
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