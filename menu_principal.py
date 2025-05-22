import tkinter as tk
from tkinter import messagebox
from GUI.calificaciones import VentanaCalificaciones
from GUI.reportes import VentanaReportes
from GUI.cursos import VentanaCursos
import subprocess
import sys


def menu_principal():
    menu = tk.Tk()
    menu.title("Sistema Académico")
    menu.geometry("500x450")
    menu.configure(bg="#eaf4fc")
    menu.resizable(False, False)

    frame = tk.Frame(menu, bg="#ffffff", padx=30, pady=30, relief=tk.RIDGE, bd=2)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Menú Principal", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 20))

    boton_estilo = {
        "width": 30,
        "height": 2,
        "font": ("Helvetica", 10),
        "bg": "#5c71e8",
        "fg": "white",
        "activebackground": "#5c71e8",
        "relief": tk.RAISED,
        "bd": 1
    }

    tk.Button(menu, text="Gestión de Estudiantes", width=30, command=abrir_estudiantes).pack(pady=10)
    tk.Button(frame, text=" Gestión de Cursos e Inscripciones", command=lambda: abrir_ventana("cursos"), **boton_estilo).pack(pady=5)
    tk.Button(frame, text=" Gestión de Calificaciones", command=lambda: abrir_ventana("calificaciones"), **boton_estilo).pack(pady=5)
    tk.Button(frame, text=" Reportes", command=lambda: abrir_ventana("reportes"), **boton_estilo).pack(pady=5)
    tk.Button(frame, text=" Salir", command=menu.destroy, bg="#f8872f", activebackground="#c0392b", fg="white", width=30, height=2).pack(pady=(20, 0))

    menu.mainloop()

def abrir_estudiantes():
    try:
        # Ejecutar el archivo estudiantes.py directamente
        subprocess.Popen([sys.executable, "GUI/estudiantes.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el módulo de estudiantes.\n{str(e)}")

def abrir_ventana(modulo):
    try:
        if modulo == "cursos":
            from GUI.cursos import VentanaCursos
            VentanaCursos()
        elif modulo == "calificaciones":
            from GUI.calificaciones import VentanaCalificaciones
            VentanaCalificaciones()
        elif modulo == "reportes":
            from GUI.reportes import VentanaReportes
            VentanaReportes()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el módulo {modulo}.\n{str(e)}")
