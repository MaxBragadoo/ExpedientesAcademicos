

import tkinter as tk
from tkinter import messagebox, ttk
from db.Conexion import crear_conexion

class VentanaEstudiantes:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Estudiantes")
        self.ventana.geometry("750x400")
        self.ventana.resizable(False, False)

        self.crear_widgets()
        self.cargar_estudiantes()

    def crear_widgets(self):
        # Formulario
        frame_form = tk.Frame(self.ventana)
        frame_form.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_form, text="Nombre").grid(row=0, column=0, sticky="e")
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(frame_form, text="Apellido").grid(row=1, column=0, sticky="e")
        self.entry_apellido = tk.Entry(frame_form)
        self.entry_apellido.grid(row=1, column=1)

        tk.Label(frame_form, text="Correo").grid(row=2, column=0, sticky="e")
        self.entry_correo = tk.Entry(frame_form)
        self.entry_correo.grid(row=2, column=1)

        tk.Label(frame_form, text="Teléfono").grid(row=3, column=0, sticky="e")
        self.entry_telefono = tk.Entry(frame_form)
        self.entry_telefono.grid(row=3, column=1)

        tk.Label(frame_form, text="Fecha de nacimiento (YYYY-MM-DD)").grid(row=4, column=0, sticky="e")
        self.entry_nacimiento = tk.Entry(frame_form)
        self.entry_nacimiento.grid(row=4, column=1)

        tk.Button(frame_form, text="Agregar", command=self.agregar_estudiante).grid(row=5, column=0, pady=10)
        tk.Button(frame_form, text="Actualizar", command=self.actualizar_estudiante).grid(row=5, column=1)
        tk.Button(frame_form, text="Eliminar", command=self.eliminar_estudiante).grid(row=6, column=0, columnspan=2)

        # Tabla
        frame_tabla = tk.Frame(self.ventana)
        frame_tabla.pack(side=tk.RIGHT, padx=10, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=("id", "nombre", "apellido", "correo", "telefono", "nacimiento"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col.title())
            self.tabla.column(col, width=100)

        self.tabla.pack()
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_estudiantes(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM estudiantes")
            for fila in cursor.fetchall():
                self.tabla.insert("", tk.END, values=fila)
            conexion.close()

    def agregar_estudiante(self):
        datos = (
            self.entry_nombre.get(),
            self.entry_apellido.get(),
            self.entry_correo.get(),
            self.entry_telefono.get(),
            self.entry_nacimiento.get()
        )

        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO estudiantes (nombre, apellido, correo, telefono, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s)", datos)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Estudiante agregado correctamente")
            self.cargar_estudiantes()
            self.limpiar_campos()

    def seleccionar_fila(self, event):
        fila = self.tabla.focus()
        valores = self.tabla.item(fila, "values")
        if valores:
            self.id_estudiante = valores[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_apellido.delete(0, tk.END)
            self.entry_apellido.insert(0, valores[2])
            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, valores[3])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[4])
            self.entry_nacimiento.delete(0, tk.END)
            self.entry_nacimiento.insert(0, valores[5])

    def actualizar_estudiante(self):
        if not hasattr(self, 'id_estudiante'):
            messagebox.showwarning("Error", "Selecciona un estudiante para actualizar")
            return

        datos = (
            self.entry_nombre.get(),
            self.entry_apellido.get(),
            self.entry_correo.get(),
            self.entry_telefono.get(),
            self.entry_nacimiento.get(),
            self.id_estudiante
        )

        if not all(datos[:-1]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE estudiantes
                SET nombre=%s, apellido=%s, correo=%s, telefono=%s, fecha_nacimiento=%s
                WHERE id=%s
            """, datos)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
            self.cargar_estudiantes()
            self.limpiar_campos()

    def eliminar_estudiante(self):
        if not hasattr(self, 'id_estudiante'):
            messagebox.showwarning("Error", "Selecciona un estudiante para eliminar")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este estudiante?")
        if not confirmar:
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE id=%s", (self.id_estudiante,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Estudiante eliminado")
            self.cargar_estudiantes()
            self.limpiar_campos()

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_nacimiento.delete(0, tk.END)
        if hasattr(self, 'id_estudiante'):
            del self.id_estudiante

