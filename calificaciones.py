import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from db.Conexion import crear_conexion

__version__ = "1.0.0"

# Configurar logger de auditoría y errores
logging.basicConfig(
    filename='auditoria_calificaciones.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_auditoria(operacion, detalles):
    entry = f"OPERACION={operacion}; VERSION={__version__}; {detalles}"
    logging.info(entry)

class VentanaCalificaciones:
    def __init__(self, master=None, usuario='desconocido'):
        self.usuario = usuario
        self.ventana = tk.Toplevel(master)
        self.ventana.title(f"Gestión de Calificaciones v{__version__}")
        self.ventana.geometry("900x550")
        self.ventana.configure(bg="#f0f8ff")  # AliceBlue
        self.ventana.resizable(False, False)

        # Estilos
        style = ttk.Style(self.ventana)
        style.theme_use('clam')
        style.configure('TLabel', background='#f0f8ff', foreground='#000000', font=('Segoe UI', 10))
        style.configure('Header.TLabel', background='#f0f8ff', foreground='#4682b4', font=('Segoe UI Semibold', 14))
        style.configure('TButton', font=('Segoe UI', 10), padding=6,
                        background='#5f9ea0', foreground='#ffffff')  # CadetBlue
        style.map('TButton', background=[('active', '#7fffd4')])  # Aquamarine
        style.configure('TCombobox', font=('Segoe UI', 10), fieldbackground='#ffffff', background='#ffffff', foreground='#000000')
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=25,
                        background='#e6f0f8', fieldbackground='#e6f0f8', foreground='#000000')  # Light blue
        style.configure('Treeview.Heading', font=('Segoe UI Semibold', 11), background='#4682b4', foreground='#ffffff')
        style.map('Treeview', background=[('selected', '#7fffd4')])

        # Contenedores
        self.header_frame = tk.Frame(self.ventana, bg='#f0f8ff', height=120)
        self.header_frame.pack(fill='x')
        self.content_frame = tk.Frame(self.ventana, bg='#f0f8ff', padx=20, pady=10)
        self.content_frame.pack(fill='both', expand=True)

        self._cargar_imagen_halcon()
        ttk.Label(self.header_frame, text="Panel de Calificaciones", style='Header.TLabel').place(x=260, y=40)
        self._crear_widgets()
        self.cargar_cursos()

    def _cargar_imagen_halcon(self):
        ruta = "halcon.png"
        if os.path.exists(ruta):
            try:
                img = Image.open(ruta).convert("RGBA")
                img = img.point(lambda p: p if p < 250 else 255)
                img = img.resize((180, 90), Image.Resampling.LANCZOS)
                self.halcon_img = ImageTk.PhotoImage(img)
                tk.Label(self.header_frame, image=self.halcon_img, bg='#f0f8ff').place(x=20, y=15)
            except Exception as e:
                logging.error(f"ERROR_IMAGEN_HALCON; {e}")
                messagebox.showerror("Error", "No se pudo procesar la imagen del halcón.")

    def _crear_widgets(self):
        ttk.Label(self.content_frame, text="Curso:").grid(row=0, column=0, sticky='w')
        self.combo_cursos = ttk.Combobox(self.content_frame, width=40, state="readonly")
        self.combo_cursos.grid(row=0, column=1, pady=5, sticky='w')
        self.combo_cursos.bind("<<ComboboxSelected>>", self.cargar_inscritos)

        cols = ("Nombre", "Apellido", "Calificación")
        self.tabla = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor='center')
        self.tabla.grid(row=1, column=0, columnspan=3, pady=10, sticky='nsew')
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky='ns', pady=10)

        ttk.Label(self.content_frame, text="Calificación (0-100):").grid(row=2, column=0, sticky='w')
        self.entry_calificacion = ttk.Entry(self.content_frame)
        self.entry_calificacion.grid(row=2, column=1, sticky='w')

        self.btn_guardar = ttk.Button(
            self.content_frame,
            text="Guardar Calificación",
            command=self.guardar_calificacion,
            style='TButton'
        )
        self.btn_guardar.grid(row=3, column=1, pady=15, sticky='e')

        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.columnconfigure(2, weight=1)

    def cargar_cursos(self):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM cursos")
            self.cursos = cursor.fetchall()
            self.combo_cursos['values'] = [f"{c[1]} (ID {c[0]})" for c in self.cursos]
        except Exception as e:
            logging.error(f"ERROR_CARGAR_CURSOS; {e}")
            messagebox.showerror("Error", "No se pudieron cargar los cursos.")
        finally:
            if 'conexion' in locals(): conexion.close()

    def cargar_inscritos(self, event=None):
        idx = self.combo_cursos.current()
        if idx < 0: return
        id_curso = self.cursos[idx][0]
        for row in self.tabla.get_children(): self.tabla.delete(row)
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT e.nombre, e.apellido, c.calificacion,i.id
                FROM inscripciones i
                JOIN estudiantes e ON e.id = i.id_estudiante
                LEFT JOIN calificaciones c ON c.id_inscripcion = i.id
                WHERE i.id_curso = %s
                """, (id_curso,)
            )
            for fila in cursor.fetchall():
                self.tabla.insert('', tk.END, values=fila)
        except Exception as e:
            logging.error(f"ERROR_CARGAR_INSCRITOS; {e}")
            messagebox.showerror("Error", "No se pudieron cargar los inscritos.")
        finally:
            if 'conexion' in locals(): conexion.close()

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel: return
        valores = self.tabla.item(sel[0], 'values')
        self.id_inscripcion = valores[3]
        self.entry_calificacion.delete(0, tk.END)
        if valores[2] is not None:
            self.entry_calificacion.insert(0, valores[2])

    def guardar_calificacion(self):
        if not hasattr(self, 'id_inscripcion'):
            messagebox.showwarning("Atención", "Selecciona un estudiante.")
            return
        try:
            cal = float(self.entry_calificacion.get())
            if cal < 0 or cal > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Calificación debe ser 0-100.")
            return
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM calificaciones WHERE id_inscripcion=%s", (self.id_inscripcion,))
            existe = cursor.fetchone()
            if existe:
                cursor.execute(
                    "UPDATE calificaciones SET calificacion=%s WHERE id_inscripcion=%s",
                    (cal, self.id_inscripcion)
                )
                oper = 'ACTUALIZAR_CALIFICACION'
            else:
                cursor.execute(
                    "INSERT INTO calificaciones (id_inscripcion, calificacion) VALUES (%s, %s)",
                    (self.id_inscripcion, cal)
                )
                oper = 'INSERTAR_CALIFICACION'
            conexion.commit()
            mensaje = "Calificación guardada." if existe else "Calificación registrada."
            messagebox.showinfo("¡Listo!", mensaje)
            detalles = f"usuario={self.usuario}; id_inscripcion={self.id_inscripcion}; calificacion={cal}"
            registrar_auditoria(oper, detalles)
            self.cargar_inscritos()
            self.entry_calificacion.delete(0, tk.END)
        except Exception as e:
            logging.error(f"ERROR_GUARDAR_CALIFICACION; {e}")
            messagebox.showerror("Error", "No se pudo guardar la calificación.")
        finally:
            if 'conexion' in locals(): conexion.close()