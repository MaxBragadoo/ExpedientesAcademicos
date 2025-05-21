

import tkinter as tk
from tkinter import ttk, messagebox
from db.Conexion import crear_conexion

class VentanaCalificaciones:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Calificaciones")
        self.ventana.geometry("800x500")
        self.ventana.resizable(False, False)

        self.crear_widgets()
        self.cargar_cursos()

    def crear_widgets(self):
        # Selección de curso
        tk.Label(self.ventana, text="Curso:").pack(pady=5)
        self.combo_cursos = ttk.Combobox(self.ventana, width=50, state="readonly")
        self.combo_cursos.pack()
        self.combo_cursos.bind("<<ComboboxSelected>>", self.cargar_inscritos)

        # Tabla de estudiantes inscritos
        self.tabla = ttk.Treeview(self.ventana, columns=("id", "nombre", "apellido", "calificacion"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)
        self.tabla.pack(pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # Ingreso de calificación
        tk.Label(self.ventana, text="Calificación (0-100):").pack()
        self.entry_calificacion = tk.Entry(self.ventana)
        self.entry_calificacion.pack()

        tk.Button(self.ventana, text="Guardar Calificación", command=self.guardar_calificacion).pack(pady=10)

    def cargar_cursos(self):
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM cursos")
            self.cursos = cursor.fetchall()
            self.combo_cursos['values'] = [f"{c[1]} (ID {c[0]})" for c in self.cursos]
            conexion.close()

    def cargar_inscritos(self, event=None):
        curso_idx = self.combo_cursos.current()
        if curso_idx == -1:
            return
        id_curso = self.cursos[curso_idx][0]

        self.tabla.delete(*self.tabla.get_children())

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT i.id, e.nombre, e.apellido, c.calificacion
                FROM inscripciones i
                JOIN estudiantes e ON e.id = i.id_estudiante
                LEFT JOIN calificaciones c ON c.id_inscripcion = i.id
                WHERE i.id_curso = %s
            """, (id_curso,))
            for fila in cursor.fetchall():
                self.tabla.insert("", tk.END, values=fila)
            conexion.close()

    def seleccionar_fila(self, event):
        fila = self.tabla.focus()
        valores = self.tabla.item(fila, "values")
        if valores:
            self.id_inscripcion = valores[0]
            self.entry_calificacion.delete(0, tk.END)
            if valores[3] is not None:
                self.entry_calificacion.insert(0, str(valores[3]))

    def guardar_calificacion(self):
        if not hasattr(self, 'id_inscripcion'):
            messagebox.showwarning("Selecciona un estudiante", "Debes seleccionar un estudiante de la tabla.")
            return

        try:
            calificacion = float(self.entry_calificacion.get())
            if not 0 <= calificacion <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Entrada inválida", "La calificación debe ser un número entre 0 y 100.")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM calificaciones WHERE id_inscripcion = %s", (self.id_inscripcion,))
            existente = cursor.fetchone()
            if existente:
                cursor.execute("UPDATE calificaciones SET calificacion=%s WHERE id_inscripcion=%s",
                               (calificacion, self.id_inscripcion))
            else:
                cursor.execute("INSERT INTO calificaciones (id_inscripcion, calificacion) VALUES (%s, %s)",
                               (self.id_inscripcion, calificacion))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Calificación guardada correctamente.")
            self.cargar_inscritos()
            self.entry_calificacion.delete(0, tk.END)
