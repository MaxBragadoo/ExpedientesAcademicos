

import tkinter as tk
from tkinter import messagebox

def lanzar_menu():
    menu = tk.Tk()
    menu.title("Sistema de Gestión Académica")
    menu.geometry("400x350")
    menu.resizable(False, False)

    tk.Label(menu, text="Menú Principal", font=("Arial", 16)).pack(pady=20)

    tk.Button(menu, text="Gestión de Estudiantes", width=30, command=lambda: abrir_ventana("estudiantes")).pack(pady=10)
    tk.Button(menu, text="Gestión de Cursos e Inscripciones", width=30, command=lambda: abrir_ventana("cursos")).pack(pady=10)
    tk.Button(menu, text="Gestión de Calificaciones", width=30, command=lambda: abrir_ventana("calificaciones")).pack(pady=10)
    tk.Button(menu, text="Reportes", width=30, command=lambda: abrir_ventana("reportes")).pack(pady=10)
    tk.Button(menu, text="Salir", width=30, command=menu.destroy).pack(pady=20)

    menu.mainloop()

def abrir_ventana(modulo):
    try:
        if modulo == "estudiantes":
            from GUI.estudiantes import VentanaEstudiantes
            VentanaEstudiantes()
        elif modulo == "cursos":
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

