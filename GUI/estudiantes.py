import customtkinter as ctk
from tkinter import messagebox
from students_crud.consultarMiembro import ConsultarEstudiantesScreen
from students_crud.crearMiembro import RegistroEstudianteForm
from students_crud.editarMiembro import EditarMiembroScreen
from students_crud.eliminarMiembro import EliminarMiembroScreen

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial de la ventana
        ctk.set_appearance_mode("System")  # Modo claro/oscuro según sistema
        ctk.set_default_color_theme("dark-blue")  # Tema de colores
        
        self.title("Gestión de Estudiantes")
        self.geometry("1400x800")
        self.minsize(1000, 600)
        
        self.iconbitmap(default='')
        
        # Inicializar el menú principal
        self.menu = Menu(self)
        
        # Centrar la ventana al iniciar
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menu_visible = True
        
        # Configuración del frame del menú
        self.configure(width=250, corner_radius=0, fg_color=("#f0f0f0", "#2b2b2b"))
        self.pack_propagate(False)
        self.pack(side="left", fill="y", padx=(0, 5))
        
        # Logo de la aplicación
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.logo_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        self.logo_label = ctk.CTkLabel(
            self.logo_frame, 
            text="Administrador", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.logo_label.pack(fill="x", padx=10)
        
        # Separador
        ctk.CTkLabel(self, text="", height=2, fg_color=("#e0e0e0", "#3a3a3a")).pack(fill="x", pady=5)
        
        # Botón principal del menú
        self.btn_miembros = ctk.CTkButton(
            self,
            text="Gestión de Estudiantes",
            command=self.miembros,
            width=220,
            height=45,  # Aumentado el tamaño
            corner_radius=8,
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),  # Texto en negrita
            fg_color=("#3a5f8a", "#2a4a6f"),  # Azul oscuro más formal
            hover_color=("#2d4a6b", "#1f3a5a"),  # Hover más oscuro
            text_color=("#ffffff", "#ffffff"),
            border_width=1,
            border_color=("#2a4a6f", "#1f3a5a")
        )
        self.btn_miembros.pack(pady=5, padx=10)
        
        # Botón para ocultar/mostrar menú
        self.btn_toggle = ctk.CTkButton(
            self.parent, 
            text="☰", 
            command=self.toggle_menu, 
            width=45,  # Aumentado el tamaño
            height=45,
            corner_radius=20,
            fg_color=("#f0f0f0", "#2b2b2b"),
            hover_color=("#d0d0d0", "#3a3a3a"),
            font=ctk.CTkFont(size=18),
            border_width=1,
            border_color=("#d0d0d0", "#3a3a3a")
        )
        self.btn_toggle.place(x=260, y=10)
        
        # Contenedor de las pantallas
        self.screen_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.screen_container.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Pantalla inicial (gestión de miembros)
        self.screen_miembros = self.create_miembros_screen()
        self.screen_miembros.pack(fill="both", expand=True)
        
        # Eventos
        self.parent.bind("<Configure>", self.ajustar_posicion_toggle)

    def create_miembros_screen(self):
        """Crea la pantalla de gestión de miembros"""
        frame = ctk.CTkFrame(self.screen_container, fg_color="transparent")
        
        # Título
        ctk.CTkLabel(
            frame, 
            text="Gestión de Estudiantes", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 10))

        # Contenedor para botones CRUD
        crud_frame = ctk.CTkFrame(frame, fg_color="transparent")
        crud_frame.pack(pady=(0, 20))
        
        # Configuración común para botones
        button_style = {
            "width": 110,  # Aumentado el ancho
            "height": 40,  # Aumentado el alto
            "corner_radius": 8,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "border_width": 1,
            "hover": True
        }
        
        # Botones de operaciones
        ctk.CTkButton(
            crud_frame,
            text="Agregar",
            fg_color=("#4a7c59", "#3a6b49"),  # Verde oscuro formal
            hover_color=("#3a6b49", "#2a5a39"),
            border_color=("#3a6b49", "#2a5a39"),
            command=self.agregar_miembro,
            **button_style
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            crud_frame,
            text="Consultar",
            fg_color=("#6a5a8a", "#5a4a7a"),  # Púrpura oscuro formal
            hover_color=("#5a4a7a", "#4a3a6a"),
            border_color=("#5a4a7a", "#4a3a6a"),
            command=self.consultar_miembro,
            **button_style
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            crud_frame,
            text="Editar",
            fg_color=("#5a6b8a", "#4a5b7a"),  # Azul grisáceo formal
            hover_color=("#4a5b7a", "#3a4b6a"),
            border_color=("#4a5b7a", "#3a4b6a"),
            command=self.editar_miembro,
            **button_style
        ).pack(side="left", padx=5, pady=5)

       

        ctk.CTkButton(
            crud_frame,
            text="Eliminar",
            fg_color=("#8a4a4a", "#7a3a3a"),  # Rojo vino formal
            hover_color=("#7a3a3a", "#6a2a2a"),
            border_color=("#7a3a3a", "#6a2a2a"),
            command=self.eliminar_miembro,
            **button_style
        ).pack(side="left", padx=5, pady=5)

        # Lista de miembros (con scroll)
        self.member_list_frame = ctk.CTkScrollableFrame(frame, height=300)
        self.member_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mensaje inicial (puedes reemplazarlo con datos reales)
        ctk.CTkLabel(
            self.member_list_frame, 
            text="Aquí se mostrarán los miembros registrados",
            font=ctk.CTkFont(size=12)
        ).pack(pady=20)
        
        return frame

    # ==================== MÉTODOS PARA GESTIÓN DE MIEMBROS ====================
    def agregar_miembro(self):
        """Abre el formulario de registro"""
        self.limpiar_contenido()
        RegistroEstudianteForm(
            root=self.member_list_frame,
            on_submit=self.guardar_nuevo_estudiante
        )

    def editar_miembro(self):
        """Abre la pantalla de edición"""
        self.limpiar_contenido()
        EditarMiembroScreen(self.member_list_frame).frame.pack(fill="both", expand=True)

    def consultar_miembro(self):
        """Abre la pantalla de consulta"""
        self.limpiar_contenido()
        ConsultarEstudiantesScreen(self.member_list_frame).frame.pack(fill="both", expand=True)

    def eliminar_miembro(self):
        """Abre la pantalla de eliminación"""
        self.limpiar_contenido()
        EliminarMiembroScreen(self.member_list_frame).frame.pack(fill="both", expand=True)

    def guardar_nuevo_estudiante(self, estudiante_data):
        """Simula guardar en base de datos (debes implementar esto)"""
        messagebox.showinfo("Éxito", f"Se guardó: {estudiante_data}")
        self.limpiar_contenido()
        self.cargar_miembros()

    def cargar_miembros(self):
        """Simula carga de miembros (implementa tu lógica real aquí)"""
        self.limpiar_contenido()
        ctk.CTkLabel(
            self.member_list_frame, 
            text="Lista actualizada de miembros",
            font=ctk.CTkFont(size=12)
        ).pack(pady=20)

    def limpiar_contenido(self):
        """Limpia el área de contenido"""
        for widget in self.member_list_frame.winfo_children():
            widget.destroy()

    # ==================== MÉTODOS DEL MENÚ LATERAL ====================
    def miembros(self):
        """Muestra la pantalla de gestión de miembros"""
        self.screen_miembros.pack(fill="both", expand=True)
        self.btn_miembros.configure(
            fg_color=("#3a5f8a", "#2a4a6f"),
            text_color=("#ffffff", "#ffffff")
        )

    def toggle_menu(self):
        """Alterna la visibilidad del menú lateral"""
        if self.menu_visible:
            self.pack_forget()
            self.menu_visible = False
            self.btn_toggle.place(x=10, y=10)
        else:
            self.pack(side="left", fill="y", padx=(0, 5))
            self.menu_visible = True
            self.btn_toggle.place(x=260, y=10)

    def ajustar_posicion_toggle(self, event=None):
        """Ajusta la posición del botón toggle al redimensionar"""
        if self.menu_visible:
            self.btn_toggle.place(x=260, y=10)
        else:
            self.btn_toggle.place(x=10, y=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()