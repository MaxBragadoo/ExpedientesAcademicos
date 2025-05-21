

import tkinter as tk
from tkinter import ttk, messagebox
from db.Conexion import crear_conexion

class VentanaCursos:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Cursos e Inscripciones")
        self.ventana.geometry("800x500")
        self.ventana.resizable(False, False)

        self.crear_widgets()
        self.cargar_cursos()
        self.cargar_estudiantes()

    def crear_widgets(self):
        # Sección de cursos
        frame_cursos = tk.LabelFrame(self.ventana, text="Cursos")
        frame_cursos.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_cursos, text="Nombre").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(frame_cursos, width=30)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(frame_cursos, text="Descripción").grid(row=1, column=0)
        self.entry_descripcion = tk.Entry(frame_cursos, width=30)
        self.entry_descripcion.grid(row=1, column=1)

        tk.Label(frame_cursos, text="Créditos").grid(row=2, column=0)
        self.entry_creditos = tk.Entry(frame_cursos, width=10)
        self.entry_creditos.grid(row=2, column=1)

        tk.Button(frame_cursos, text="Agregar Curso", command=self.agregar_curso).grid(row=3, column=0, pady=10)
        tk.Button(frame_cursos, text="Actualizar Curso", command=self.actualizar_curso).grid(row=3, column=1)
        tk.Button(frame_cursos, text="Eliminar Curso", command=self.eliminar_curso).grid(row=3, column=2)

        # Tabla de cursos
        self.tabla_cursos = ttk.Treeview(self.ventana, columns=("id", "nombre", "descripcion", "creditos"), show="headings")
        for col in self.tabla_cursos["columns"]:
            self.tabla_cursos.heading(col, text=col.capitalize())
            self.tabla_cursos.column(col, width=150)
        self.tabla_cursos.pack(pady=10)
        self.tabla_cursos.bind("<<TreeviewSelect>>", self.seleccionar_curso)

        # Inscripciones
        frame_inscripciones = tk.LabelFrame(self.ventana, text="Inscribir estudiante")
        frame_inscripciones.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inscripciones, text="Estudiante:").grid(row=0, column=0)
        self.combo_estudiantes = ttk.Combobox(frame_inscripciones, state="readonly", width=40)
        self.combo_estudiantes.grid(row=0, column=1)

        tk.Button(frame_inscripciones, text="Inscribir", command=self.inscribir_estudiante).grid(row=0, column=2, padx=5)
        tk.Button(frame_inscripciones, text="Ver Inscripciones", command=self.ver_inscripciones).grid(row=0, column=3)

    def cargar_cursos(self):
        for row in self.tabla_cursos.get_children():
            self.tabla_cursos.delete(row)

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM cursos")
            for fila in cursor.fetchall():
                self.tabla_cursos.insert("", tk.END, values=fila)
            conexion.close()

    def cargar_estudiantes(self):
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, apellido FROM estudiantes")
            self.estudiantes = cursor.fetchall()
            nombres = [f"{e[1]} {e[2]} (ID {e[0]})" for e in self.estudiantes]
            self.combo_estudiantes['values'] = nombres
            conexion.close()

    def seleccionar_curso(self, event):
        fila = self.tabla_cursos.focus()
        valores = self.tabla_cursos.item(fila, "values")
        if valores:
            self.id_curso = valores[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[2])
            self.entry_creditos.delete(0, tk.END)
            self.entry_creditos.insert(0, valores[3])

    def agregar_curso(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        creditos = self.entry_creditos.get()

        if not nombre or not creditos:
            messagebox.showwarning("Campos obligatorios", "Nombre y créditos son obligatorios.")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO cursos (nombre, descripcion, creditos) VALUES (%s, %s, %s)",
                           (nombre, descripcion, creditos))
            conexion.commit()
            conexion.close()
            self.cargar_cursos()
            self.entry_nombre.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.entry_creditos.delete(0, tk.END)

    def actualizar_curso(self):
        if not hasattr(self, 'id_curso'):
            messagebox.showwarning("Curso no seleccionado", "Selecciona un curso para actualizar.")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE cursos
                SET nombre=%s, descripcion=%s, creditos=%s
                WHERE id=%s
            """, (
                self.entry_nombre.get(),
                self.entry_descripcion.get(),
                self.entry_creditos.get(),
                self.id_curso
            ))
            conexion.commit()
            conexion.close()
            self.cargar_cursos()

    def eliminar_curso(self):
        if not hasattr(self, 'id_curso'):
            messagebox.showwarning("Curso no seleccionado", "Selecciona un curso para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este curso?")
        if confirmar:
            conexion = crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM cursos WHERE id=%s", (self.id_curso,))
                conexion.commit()
                conexion.close()
                self.cargar_cursos()

    def inscribir_estudiante(self):
        if not hasattr(self, 'id_curso'):
            messagebox.showwarning("Curso no seleccionado", "Selecciona un curso para inscribir.")
            return
        if not self.combo_estudiantes.get():
            messagebox.showwarning("Selecciona estudiante", "Selecciona un estudiante.")
            return

        idx = self.combo_estudiantes.current()
        id_estudiante = self.estudiantes[idx][0]

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO inscripciones (id_estudiante, id_curso, fecha_inscripcion)
                VALUES (%s, %s, CURDATE())
            """, (id_estudiante, self.id_curso))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Estudiante inscrito correctamente.")

    def ver_inscripciones(self):
        if not hasattr(self, 'id_curso'):
            messagebox.showwarning("Curso no seleccionado", "Selecciona un curso para ver inscripciones.")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT e.nombre, e.apellido, i.fecha_inscripcion
                FROM inscripciones i
                JOIN estudiantes e ON e.id = i.id_estudiante
                WHERE i.id_curso = %s
            """, (self.id_curso,))
            resultado = cursor.fetchall()
            conexion.close()

            ventana_inscripciones = tk.Toplevel()
            ventana_inscripciones.title("Estudiantes Inscritos")
            ventana_inscripciones.geometry("400x300")

            tree = ttk.Treeview(ventana_inscripciones, columns=("nombre", "apellido", "fecha"), show="headings")
            tree.heading("nombre", text="Nombre")
            tree.heading("apellido", text="Apellido")
            tree.heading("fecha", text="Fecha Inscripción")
            tree.pack(fill="both", expand=True)

            for fila in resultado:
                tree.insert("", tk.END, values=fila)
