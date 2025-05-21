

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from db.Conexion import crear_conexion

class VentanaReportes:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Módulo de Reportes")
        self.ventana.geometry("850x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#e6f0f9")

        self.crear_widgets()

    def crear_widgets(self):
        # Selección del tipo de reporte
        opciones = ["Historial académico por estudiante", "Lista de estudiantes por curso"]
        self.combo_reporte = ttk.Combobox(self.ventana, values=opciones, state="readonly", width=50)
        self.combo_reporte.set("Selecciona un tipo de reporte")
        self.combo_reporte.pack(pady=10)
        self.combo_reporte.bind("<<ComboboxSelected>>", self.mostrar_opciones)

        self.frame_opciones = tk.Frame(self.ventana)
        self.frame_opciones.pack()

        self.tabla = ttk.Treeview(self.ventana, show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.ventana, text="Exportar a CSV", command=self.exportar_csv).pack(pady=5)

    def mostrar_opciones(self, event):
        for widget in self.frame_opciones.winfo_children():
            widget.destroy()

        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = ()

        tipo = self.combo_reporte.get()
        if tipo == "Historial académico por estudiante":
            self.combo_estudiantes = ttk.Combobox(self.frame_opciones, state="readonly", width=60)
            self.combo_estudiantes.pack()
            self.cargar_estudiantes()
            tk.Button(self.frame_opciones, text="Consultar", command=self.reporte_estudiante).pack(pady=5)
        else:
            self.combo_cursos = ttk.Combobox(self.frame_opciones, state="readonly", width=60)
            self.combo_cursos.pack()
            self.cargar_cursos()
            tk.Button(self.frame_opciones, text="Consultar", command=self.reporte_curso).pack(pady=5)

    def cargar_estudiantes(self):
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, apellido FROM estudiantes")
            self.estudiantes = cursor.fetchall()
            self.combo_estudiantes["values"] = [f"{e[1]} {e[2]} (ID {e[0]})" for e in self.estudiantes]
            conexion.close()

    def cargar_cursos(self):
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM cursos")
            self.cursos = cursor.fetchall()
            self.combo_cursos["values"] = [f"{c[1]} (ID {c[0]})" for c in self.cursos]
            conexion.close()

    def reporte_estudiante(self):
        idx = self.combo_estudiantes.current()
        if idx == -1:
            return
        id_estudiante = self.estudiantes[idx][0]

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT c.nombre AS curso, i.fecha_inscripcion, cal.calificacion
                FROM inscripciones i
                JOIN cursos c ON c.id = i.id_curso
                LEFT JOIN calificaciones cal ON cal.id_inscripcion = i.id
                WHERE i.id_estudiante = %s
            """, (id_estudiante,))
            resultados = cursor.fetchall()
            conexion.close()

            self.tabla["columns"] = ("curso", "fecha", "calificacion")
            for col in self.tabla["columns"]:
                self.tabla.heading(col, text=col.title())
                self.tabla.column(col, width=200)

            self.tabla.delete(*self.tabla.get_children())
            for fila in resultados:
                self.tabla.insert("", tk.END, values=fila)

    def reporte_curso(self):
        idx = self.combo_cursos.current()
        if idx == -1:
            return
        id_curso = self.cursos[idx][0]

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT e.nombre, e.apellido, i.fecha_inscripcion
                FROM inscripciones i
                JOIN estudiantes e ON e.id = i.id_estudiante
                WHERE i.id_curso = %s
            """, (id_curso,))
            resultados = cursor.fetchall()
            conexion.close()

            self.tabla["columns"] = ("nombre", "apellido", "fecha_inscripcion")
            for col in self.tabla["columns"]:
                self.tabla.heading(col, text=col.replace("_", " ").title())
                self.tabla.column(col, width=200)

            self.tabla.delete(*self.tabla.get_children())
            for fila in resultados:
                self.tabla.insert("", tk.END, values=fila)

    def exportar_csv(self):
        if not self.tabla.get_children():
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            columnas = self.tabla["columns"]
            with open(archivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columnas)
                for item in self.tabla.get_children():
                    writer.writerow(self.tabla.item(item)["values"])
            messagebox.showinfo("Exportación exitosa", f"Datos exportados a {archivo}")
