import tkinter as tk
from tkinter import ttk, messagebox
from db.Conexion import crear_conexion
from PIL import Image, ImageTk
import os

class VentanaCursos:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Gestión de Cursos e Inscripciones")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#e6f0f8")

        ruta_original = "C:/Users/Asus ExpertBook/Documents/DECIMO SEMESTRE/TOPICOS DESARROLLO SISTEMAS/U3/ProyectoU5/GUI/halcon.png"
        if os.path.exists(ruta_original):
            try:
                imagen_original = Image.open(ruta_original).convert("RGBA")
                nueva_imagen = Image.new("RGBA", imagen_original.size, (255, 255, 255, 0))
                for y in range(imagen_original.height):
                    for x in range(imagen_original.width):
                        r, g, b, a = imagen_original.getpixel((x, y))
                        if r > 240 and g > 240 and b > 240:
                            nueva_imagen.putpixel((x, y), (255, 255, 255, 0))
                        else:
                            nueva_imagen.putpixel((x, y), (r, g, b, a))
                nueva_imagen_resized = nueva_imagen.resize((200, 100))
                self.halcon_img = ImageTk.PhotoImage(nueva_imagen_resized)
                tk.Label(self.ventana, image=self.halcon_img, bg="#e6f0f8").place(x=20, y=10)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la imagen del halcón: {e}")

        self.contenedor = tk.Frame(self.ventana, bg="#eaf1fb", bd=1, relief="ridge")
        self.contenedor.place(x=10, y=120, width=880, height=470)

        self.crear_widgets()
        self.cargar_cursos()
        self.cargar_estudiantes()

    def crear_widgets(self):
        estilo_azul = {"bg": "#004c97", "fg": "white", "font": ("Arial", 9, "bold")}
        estilo_naranja = {"bg": "#f47b20", "fg": "white", "font": ("Arial", 9, "bold")}
        estilo_rojo = {"bg": "#8b0000", "fg": "white", "font": ("Arial", 9, "bold")}

        frame_cursos = tk.LabelFrame(self.contenedor, text="📘 Cursos", bg="#eaf1fb", fg="#004c97", font=("Arial", 10, "bold"))
        frame_cursos.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_cursos, text="Nombre:", bg="#eaf1fb").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.entry_nombre = tk.Entry(frame_cursos, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_cursos, text="Descripción:", bg="#eaf1fb").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.entry_descripcion = tk.Entry(frame_cursos, width=60)
        self.entry_descripcion.grid(row=1, column=1, columnspan=2, padx=5, pady=2)

        tk.Label(frame_cursos, text="Créditos:", bg="#eaf1fb").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.entry_creditos = tk.Entry(frame_cursos, width=10)
        self.entry_creditos.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        tk.Button(frame_cursos, text="Agregar Curso", command=self.agregar_curso, **estilo_azul).grid(row=0, column=2, padx=10)
        tk.Button(frame_cursos, text="Actualizar Curso", command=self.actualizar_curso, **estilo_naranja).grid(row=1, column=2, padx=10)
        tk.Button(frame_cursos, text="Eliminar Curso", command=self.eliminar_curso, **estilo_rojo).grid(row=2, column=2, padx=10)

        estilo_tabla = ttk.Style()
        estilo_tabla.theme_use("default")
        estilo_tabla.configure("Treeview", font=("Arial", 9), rowheight=25, background="#ffffff", fieldbackground="#f8f8f8")
        estilo_tabla.configure("Treeview.Heading", font=("Arial", 9, "bold"), background="#004c97", foreground="white")

        self.tabla_cursos = ttk.Treeview(self.contenedor, columns=("id", "nombre", "descripcion", "creditos"), show="headings")
        for col in self.tabla_cursos["columns"]:
            self.tabla_cursos.heading(col, text=col.capitalize())
            self.tabla_cursos.column(col, width=200)
        self.tabla_cursos.pack(padx=10, pady=10)
        self.tabla_cursos.bind("<<TreeviewSelect>>", self.seleccionar_curso)

        frame_inscripciones = tk.LabelFrame(self.contenedor, text="👤 Inscribir estudiante", bg="#eaf1fb", fg="#004c97", font=("Arial", 10, "bold"))
        frame_inscripciones.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_inscripciones, text="Estudiante:", bg="#eaf1fb").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_estudiantes = ttk.Combobox(frame_inscripciones, state="readonly", width=50)
        self.combo_estudiantes.grid(row=0, column=1, padx=5)

        tk.Button(frame_inscripciones, text="Inscribir", command=self.inscribir_estudiante, bg="#006d2c", fg="white").grid(row=0, column=2, padx=10)
        tk.Button(frame_inscripciones, text="Ver Inscripciones", command=self.ver_inscripciones).grid(row=0, column=3, padx=10)


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
            cursor.execute("INSERT INTO cursos (nombre, descripcion, creditos) VALUES (%s, %s, %s)", (nombre, descripcion, creditos))
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


