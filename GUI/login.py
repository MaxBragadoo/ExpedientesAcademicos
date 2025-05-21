# gui/login.py

import tkinter as tk
from tkinter import messagebox
from db.Conexion import crear_conexion

def verificar_credenciales(usuario, contraseña):
    conexion = crear_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, contraseña))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    return False

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login - Gestión Académica")
        master.geometry("300x200")
        master.resizable(False, False)

        tk.Label(master, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        tk.Label(master, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(master, show="*")
        self.entry_contrasena.pack()

        tk.Button(master, text="Iniciar Sesión", command=self.login).pack(pady=15)

    def login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        if verificar_credenciales(usuario, contrasena):
            messagebox.showinfo("Éxito", "Login exitoso")
            self.master.destroy()
            from GUI.menu_principal import lanzar_menu
            lanzar_menu()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")


