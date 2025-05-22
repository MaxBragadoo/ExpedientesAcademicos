import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re
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

class RegistroEstudianteForm:
    def __init__(self, root, on_submit=None):
        """
        Formulario para registrar un nuevo estudiante/miembro
        
        Args:
            root: Ventana padre o frame contenedor
            on_submit: Función callback que se ejecutará al enviar el formulario
        """
        self.root = root
        self.on_submit = on_submit
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(1, weight=1)
        
        # Título del formulario
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="Registro de Nuevo Estudiante",
            font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Campos del formulario
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los widgets del formulario"""
        row = 1
        
        # ID (puede ser autogenerado o manual)
        self.id_label = ctk.CTkLabel(self.root, text="ID Estudiante:")
        self.id_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = ctk.CTkEntry(self.root, placeholder_text="Número de identificación")
        self.id_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Nombre
        self.nombre_label = ctk.CTkLabel(self.root, text="Nombre(s):")
        self.nombre_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = ctk.CTkEntry(self.root)
        self.nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Apellido
        self.apellido_label = ctk.CTkLabel(self.root, text="Apellido:")
        self.apellido_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.apellido_entry = ctk.CTkEntry(self.root)
        self.apellido_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Carrera
        self.carrera_label = ctk.CTkLabel(self.root, text="Carrera:")
        self.carrera_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.carrera_entry = ctk.CTkEntry(self.root, placeholder_text="Ej: Ingeniería en Sistemas")
        self.carrera_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Fecha de Nacimiento
        self.fecha_nac_label = ctk.CTkLabel(self.root, text="Fecha de Nacimiento:")
        self.fecha_nac_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.fecha_nac_entry = ctk.CTkEntry(self.root, placeholder_text="AAAA-MM-DD")
        self.fecha_nac_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Género
        self.genero_label = ctk.CTkLabel(self.root, text="Género:")
        self.genero_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.genero_var = ctk.StringVar(value="Masculino")
        self.genero_combobox = ctk.CTkComboBox(
            self.root, 
            values=["Masculino", "Femenino", "Otro"],
            variable=self.genero_var
        )
        self.genero_combobox.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Nacionalidad
        self.nacionalidad_label = ctk.CTkLabel(self.root, text="Nacionalidad:")
        self.nacionalidad_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.nacionalidad_entry = ctk.CTkEntry(self.root, placeholder_text="Ej: Mexicana")
        self.nacionalidad_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Dirección
        self.direccion_label = ctk.CTkLabel(self.root, text="Dirección:")
        self.direccion_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.direccion_entry = ctk.CTkEntry(self.root, placeholder_text="Dirección completa")
        self.direccion_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Teléfono
        self.telefono_label = ctk.CTkLabel(self.root, text="Teléfono:")
        self.telefono_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.telefono_entry = ctk.CTkEntry(self.root, placeholder_text="+52 1234567890")
        self.telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Correo Electrónico
        self.correo_label = ctk.CTkLabel(self.root, text="Correo Electrónico:")
        self.correo_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.correo_entry = ctk.CTkEntry(self.root, placeholder_text="ejemplo@dominio.com")
        self.correo_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Nombre
        self.contacto_nombre_label = ctk.CTkLabel(self.root, text="Contacto Emergencia (Nombre):")
        self.contacto_nombre_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.contacto_nombre_entry = ctk.CTkEntry(self.root)
        self.contacto_nombre_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Relación
        self.contacto_relacion_label = ctk.CTkLabel(self.root, text="Relación:")
        self.contacto_relacion_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.contacto_relacion_entry = ctk.CTkEntry(self.root, placeholder_text="Ej: Padre, Madre, Familiar")
        self.contacto_relacion_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Contacto de Emergencia - Teléfono
        self.contacto_telefono_label = ctk.CTkLabel(self.root, text="Teléfono Emergencia:")
        self.contacto_telefono_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.contacto_telefono_entry = ctk.CTkEntry(self.root, placeholder_text="+52 9876543210")
        self.contacto_telefono_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        
        # Botones de acción
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="e")
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame, 
            text="Cancelar", 
            fg_color="gray", 
            command=self.close_form
        )
        self.cancel_button.pack(side="right", padx=5)
        
        self.submit_button = ctk.CTkButton(
            self.button_frame, 
            text="Registrar Estudiante", 
            command=self.submit_form
        )
        self.submit_button.pack(side="right", padx=5)
    
    def validate_form(self):
        """Valida los datos del formulario"""
        errors = []
        
        # Validar campos obligatorios
        if not self.id_entry.get().strip():
            errors.append("El ID de estudiante es obligatorio")
        if not self.nombre_entry.get().strip():
            errors.append("El nombre es obligatorio")
        if not self.apellido_entry.get().strip():
            errors.append("El apellido es obligatorio")
        if not self.carrera_entry.get().strip():
            errors.append("La carrera es obligatoria")
        if not self.fecha_nac_entry.get().strip():
            errors.append("La fecha de nacimiento es obligatoria")
        if not self.genero_var.get().strip():
            errors.append("El género es obligatorio")
        if not self.nacionalidad_entry.get().strip():
            errors.append("La nacionalidad es obligatoria")
        if not self.direccion_entry.get().strip():
            errors.append("La dirección es obligatoria")
        if not self.telefono_entry.get().strip():
            errors.append("El teléfono es obligatorio")
        if not self.correo_entry.get().strip():
            errors.append("El correo electrónico es obligatorio")
        if not self.contacto_nombre_entry.get().strip():
            errors.append("El nombre del contacto de emergencia es obligatorio")
        if not self.contacto_relacion_entry.get().strip():
            errors.append("La relación del contacto de emergencia es obligatoria")
        if not self.contacto_telefono_entry.get().strip():
            errors.append("El teléfono de emergencia es obligatorio")
        
        # Validar formato de correo
        correo = self.correo_entry.get().strip()
        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            errors.append("El correo electrónico no tiene un formato válido")
        
        # Validar fecha de nacimiento
        fecha_nac = self.fecha_nac_entry.get().strip()
        if fecha_nac:
            try:
                datetime.strptime(fecha_nac, "%Y-%m-%d")
            except ValueError:
                errors.append("La fecha de nacimiento debe estar en formato AAAA-MM-DD")
        
        # Validar ID es numérico
        try:
            int(self.id_entry.get().strip())
        except ValueError:
            errors.append("El ID debe ser un número entero")
        
        return errors
    
    def get_form_data(self):
        """Obtiene los datos del formulario en un diccionario"""
        return {
            "id": int(self.id_entry.get().strip()),
            "carrera": self.carrera_entry.get().strip(),
            "nombre": self.nombre_entry.get().strip(),
            "apellido": self.apellido_entry.get().strip(),  # Nuevo campo
            "fecha_nacimiento": self.fecha_nac_entry.get().strip(),
            "genero": self.genero_var.get(),
            "nacionalidad": self.nacionalidad_entry.get().strip(),
            "direccion": self.direccion_entry.get().strip(),
            "telefono": self.telefono_entry.get().strip(),
            "correo_electronico": self.correo_entry.get().strip(),
            "contacto_emergencia_nombre": self.contacto_nombre_entry.get().strip(),
            "contacto_emergencia_relacion": self.contacto_relacion_entry.get().strip(),
            "contacto_emergencia_telefono": self.contacto_telefono_entry.get().strip()
        }
    
    def submit_form(self):
        """Envía el formulario después de validar los datos"""
        errors = self.validate_form()
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return
        
        form_data = self.get_form_data()
        
        # Insertar en la base de datos
        if self.insertar_estudiante(form_data):
            if self.on_submit:
                self.on_submit(form_data)
    
    def insertar_estudiante(self, estudiante_data):
        """Inserta un nuevo estudiante en la base de datos"""
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return False
        
        try:
            cursor = conexion.cursor()
            
            query = """
            INSERT INTO estudiantes (
                id, carrera, nombre, apellido, fecha_nacimiento, genero, 
                nacionalidad, direccion, telefono, correo_electronico, 
                contacto_emergencia_nombre, contacto_emergencia_relacion, 
                contacto_emergencia_telefono
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                estudiante_data['id'],
                estudiante_data['carrera'],
                estudiante_data['nombre'],
                estudiante_data['apellido'],  # Nuevo campo
                estudiante_data['fecha_nacimiento'],
                estudiante_data['genero'],
                estudiante_data['nacionalidad'],
                estudiante_data['direccion'],
                estudiante_data['telefono'],
                estudiante_data['correo_electronico'],
                estudiante_data['contacto_emergencia_nombre'],
                estudiante_data['contacto_emergencia_relacion'],
                estudiante_data['contacto_emergencia_telefono']
            ))
            
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante registrado correctamente")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar estudiante: {str(e)}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
    
    def close_form(self):
        """Cierra el formulario"""
        if hasattr(self.root, "destroy"):
            self.root.destroy()
        else:
            self.root.grid_forget()

# Ejemplo de uso
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Registro de Estudiante")
    root.geometry("800x800")
    
    def handle_submit(data):
        print("Datos del estudiante recibidos:")
        print(data)
        root.destroy()
    
    # Crear un frame principal
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Mostrar el formulario
    form = RegistroEstudianteForm(main_frame, on_submit=handle_submit)
    
    root.mainloop()