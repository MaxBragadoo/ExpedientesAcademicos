import tkinter as tk
from tkinter import messagebox
from db.Conexion import crear_conexion

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistema Académico")
        self.geometry("400x470")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        self.login_frame = tk.Frame(self, bg="#f0f0f0")
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Bienvenido", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)
        tk.Label(self.login_frame, text="Inicia sesión para continuar", font=("Helvetica", 10), bg="#f0f0f0").pack()

        tk.Label(self.login_frame, text="Usuario:", bg="#f0f0f0").pack(pady=(20, 5))
        self.usuario_entry = tk.Entry(self.login_frame, width=30)
        self.usuario_entry.pack()

        tk.Label(self.login_frame, text="Contraseña:", bg="#f0f0f0").pack(pady=(10, 5))
        self.clave_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.clave_entry.pack()

        tk.Button(self.login_frame, text=" Iniciar Sesión", command=self.verificar_login, bg="#4CAF50", fg="white", width=20).pack(pady=15)
        tk.Label(self.login_frame, text="", bg="#f0f0f0").pack(pady=10)  
        tk.Label(self.login_frame, text="¿No tienes una cuenta?", font=("Helvetica", 10), bg="#f0f0f0").pack()
        tk.Button(self.login_frame, text=" Registrarse", command=self.mostrar_registro, bg="#174f9a", fg="white", width=20).pack()

        # Frame de registro
        self.registro_frame = tk.Frame(self, bg="#f0f0f0")

        tk.Label(self.registro_frame, text="Registro de Usuario", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

        tk.Label(self.registro_frame, text="Nuevo Usuario:", bg="#f0f0f0").pack(pady=(10, 5))
        self.nuevo_usuario_entry = tk.Entry(self.registro_frame, width=30)
        self.nuevo_usuario_entry.pack()

        tk.Label(self.registro_frame, text="Nueva Contraseña:", bg="#f0f0f0").pack(pady=(10, 5))
        self.nueva_clave_entry = tk.Entry(self.registro_frame, show="*", width=30)
        self.nueva_clave_entry.pack()

        tk.Label(self.registro_frame, text="Confirmar Contraseña:", bg="#f0f0f0").pack(pady=(10, 5))
        self.confirmar_clave_entry = tk.Entry(self.registro_frame, show="*", width=30)
        self.confirmar_clave_entry.pack()

        tk.Button(self.registro_frame, text=" Crear Cuenta", command=self.registrar_usuario, bg="#4CAF50", fg="white", width=13).pack(side=tk.LEFT, padx=5, pady=50)
        tk.Button(self.registro_frame, text=" Volver al Login", command=self.mostrar_login, bg="#9c2d55", fg="white", width=13).pack(side=tk.RIGHT, padx=5, pady=50)

    def mostrar_registro(self):
        self.login_frame.pack_forget()
        self.registro_frame.pack(pady=20)

    def mostrar_login(self):
        self.registro_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        clave = self.clave_entry.get()
        if self.verificar_credenciales(usuario, clave):
            messagebox.showinfo("Acceso correcto", f"Bienvenido {usuario}")
            self.destroy()
            from GUI.menu_principal import menu_principal
            menu_principal()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

    def verificar_credenciales(self, usuario, contraseña):
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, contraseña))
            resultado = cursor.fetchone()
            conexion.close()
            return resultado is not None
        return False

    def registrar_usuario(self):
        usuario = self.nuevo_usuario_entry.get()
        clave = self.nueva_clave_entry.get()
        confirmar = self.confirmar_clave_entry.get()

        if not usuario or not clave or not confirmar:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if clave != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El usuario ya se encuentra registrado")
                conexion.close()
                return
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario, clave))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente ")
            self.mostrar_login()
            self.nuevo_usuario_entry.delete(0, tk.END)
            self.nueva_clave_entry.delete(0, tk.END)
            self.confirmar_clave_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Error al conectar con la base de datos")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
