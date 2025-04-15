import tkinter as tk
from tkinter import ttk, messagebox

from post import generar_post
from front_page import portada_carrusel
from cta import slide_cta
from config import COLORS

class CarouselApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configurador de Carrusel con Texto Multicolor")
        self.geometry("900x700")
        
        # Aquí guardaremos todos los slides como dict
        # Cada slide tendrá: {
        #   "titulo": str,
        #   "categoria": str,
        #   "contenido": List[(texto, color_key)],
        #   "color_texto": str (opcional, si quisieras un color de fallback)
        # }
        self.slides = []
        
        self.create_widgets()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both')

        # ------------------------------------------------
        #  Pestaña Portada (igual que antes, ejemplo básico)
        # ------------------------------------------------
        tab_portada = ttk.Frame(notebook)
        notebook.add(tab_portada, text="Portada")

        tk.Label(tab_portada, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.portada_titulo = tk.Entry(tab_portada, width=50)
        self.portada_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(tab_portada, text="Categoría:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.portada_categoria = tk.Entry(tab_portada, width=50)
        self.portada_categoria.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(tab_portada, text="Archivo de salida:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.portada_output = tk.Entry(tab_portada, width=50)
        self.portada_output.insert(0, "solid_slide_1_portada.png")
        self.portada_output.grid(row=2, column=1, padx=5, pady=5)

        # (Opcional) Combobox para color global en la portada
        tk.Label(tab_portada, text="Color de texto global (opcional):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.portada_color = ttk.Combobox(tab_portada, values=list(COLORS.keys()), state="readonly")
        self.portada_color.set("texto")  # valor por defecto
        self.portada_color.grid(row=3, column=1, padx=5, pady=5)

        # ------------------------------------------------
        # Pestaña Slides de Contenido (con texto multicolor)
        # ------------------------------------------------
        tab_slides = ttk.Frame(notebook)
        notebook.add(tab_slides, text="Slides de Contenido")

        # Panel izquierdo: Listbox con los slides agregados
        frame_slide_list = ttk.Frame(tab_slides)
        frame_slide_list.grid(row=0, column=0, rowspan=6, padx=5, pady=5, sticky="ns")

        self.slide_listbox = tk.Listbox(frame_slide_list, height=16, width=30)
        self.slide_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_slide_list, orient=tk.VERTICAL, command=self.slide_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.slide_listbox.config(yscrollcommand=scrollbar.set)

        # Panel derecho: Datos para crear/editar un slide
        tk.Label(tab_slides, text="Título del slide:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.slide_titulo = tk.Entry(tab_slides, width=40)
        self.slide_titulo.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(tab_slides, text="Categoría:").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.slide_categoria = tk.Entry(tab_slides, width=40)
        self.slide_categoria.grid(row=1, column=2, padx=5, pady=5)

        # Combobox para color global del slide (opcional)
        tk.Label(tab_slides, text="Color global (opcional):").grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.slide_color = ttk.Combobox(tab_slides, values=list(COLORS.keys()), state="readonly")
        self.slide_color.set("texto")
        self.slide_color.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # ------------------------------------------------
        #    Sección para Agregar Fragmentos de Texto
        # ------------------------------------------------
        # Cada fragmento es (texto, color_key)

        tk.Label(tab_slides, text="Texto del Fragmento:").grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.fragmento_texto = tk.Entry(tab_slides, width=40)
        self.fragmento_texto.grid(row=3, column=2, padx=5, pady=2)

        tk.Label(tab_slides, text="Color del Fragmento:").grid(row=4, column=1, sticky="w", padx=5, pady=2)
        self.fragmento_color = ttk.Combobox(tab_slides, values=list(COLORS.keys()), state="readonly")
        self.fragmento_color.set("")  # puede dejarse vacío
        self.fragmento_color.grid(row=4, column=2, padx=5, pady=2, sticky="w")

        # Listbox donde se almacenan los fragmentos para ESTE slide
        self.fragmentos_listbox = tk.Listbox(tab_slides, height=8, width=40)
        self.fragmentos_listbox.grid(row=5, column=2, padx=5, pady=5, sticky="n")

        btn_agregar_fragmento = tk.Button(tab_slides, text="Agregar Fragmento", command=self.agregar_fragmento)
        btn_agregar_fragmento.grid(row=5, column=1, padx=5, pady=5, sticky="n")

        btn_eliminar_fragmento = tk.Button(tab_slides, text="Eliminar Fragmento", command=self.eliminar_fragmento)
        btn_eliminar_fragmento.grid(row=5, column=1, padx=5, pady=5, sticky="s")

        # Botones para Guardar el Slide o Eliminar Slide
        btn_agregar_slide = tk.Button(tab_slides, text="Agregar Slide", command=self.agregar_slide)
        btn_agregar_slide.grid(row=6, column=2, padx=5, pady=5, sticky="e")

        btn_eliminar_slide = tk.Button(tab_slides, text="Eliminar Slide Seleccionado", command=self.eliminar_slide)
        btn_eliminar_slide.grid(row=7, column=2, padx=5, pady=5, sticky="e")

        # ------------------------------------------------
        # Pestaña CTA (igual que antes, ejemplo)
        # ------------------------------------------------
        tab_cta = ttk.Frame(notebook)
        notebook.add(tab_cta, text="Slide CTA")

        tk.Label(tab_cta, text="Bloque 1:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cta_bloque1 = tk.Entry(tab_cta, width=50)
        self.cta_bloque1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(tab_cta, text="Bloque 2:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cta_bloque2 = tk.Entry(tab_cta, width=50)
        self.cta_bloque2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(tab_cta, text="Bloque 3:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cta_bloque3 = tk.Entry(tab_cta, width=50)
        self.cta_bloque3.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(tab_cta, text="Archivo de salida:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.cta_output = tk.Entry(tab_cta, width=50)
        self.cta_output.insert(0, "solid_slide_7_cta.png")
        self.cta_output.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(tab_cta, text="Color de texto (opcional):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.cta_color = ttk.Combobox(tab_cta, values=list(COLORS.keys()), state="readonly")
        self.cta_color.set("texto")
        self.cta_color.grid(row=4, column=1, padx=5, pady=5)

        # ------------------------------------------------
        #   Botón Final para Generar Todo el Carrusel
        # ------------------------------------------------
        btn_generar = tk.Button(self, text="Generar Carrusel", command=self.generar_carrusel)
        btn_generar.pack(pady=10)

    # ------------------------------------------------
    #    MÉTODOS PARA MANEJAR FRAGMENTOS DE TEXTO
    # ------------------------------------------------
    def agregar_fragmento(self):
        """Agrega un nuevo fragmento (texto + color) a la lista local de fragmentos."""
        texto = self.fragmento_texto.get().strip()
        color_key = self.fragmento_color.get().strip()  # podría estar vacío
        
        if not texto:
            messagebox.showerror("Error", "Debes escribir algo de texto para el fragmento.")
            return
        
        # Guardamos la tupla (texto, color_key) en el listbox. 
        # Ej: ("Hola mundo", "coral")
        # Si color_key está vacío, el dibujado usará el color por defecto en la función.
        item_str = f'"{texto}" | {color_key if color_key else "None"}'
        self.fragmentos_listbox.insert(tk.END, item_str)
        
        # Limpiar campos
        self.fragmento_texto.delete(0, tk.END)
        self.fragmento_color.set("")

    def eliminar_fragmento(self):
        """Elimina el fragmento seleccionado en el listbox de fragmentos."""
        index = self.fragmentos_listbox.curselection()
        if not index:
            messagebox.showerror("Error", "Selecciona un fragmento para eliminar.")
            return
        
        self.fragmentos_listbox.delete(index[0])

    def obtener_fragmentos(self):
        """
        Retorna los fragmentos actuales del listbox como lista de tuplas (texto, color_key).
        """
        fragmentos = []
        for i in range(self.fragmentos_listbox.size()):
            item_str = self.fragmentos_listbox.get(i)  
            # item_str es algo como:  "Hola mundo" | coral
            # Podríamos parsear con un split en '|'
            # O podemos usar otra convención
            if '|' in item_str:
                partes = item_str.split('|', maxsplit=1)
                texto_str = partes[0].strip().strip('"')
                color_key = partes[1].strip()
                if color_key == "None":
                    color_key = None
                fragmentos.append((texto_str, color_key))
            else:
                # Si no hay '|', asumimos sin color
                fragmentos.append((item_str, None))
        return fragmentos
    
    # ------------------------------------------------
    #    MÉTODOS PARA AGREGAR / ELIMINAR SLIDES
    # ------------------------------------------------
    def agregar_slide(self):
        """Agrega un nuevo slide con los datos actuales (título, categoría, fragmentos)."""
        titulo = self.slide_titulo.get().strip()
        categoria = self.slide_categoria.get().strip()
        
        if not titulo or not categoria:
            messagebox.showerror("Error", "Debes completar Título y Categoría para el slide.")
            return
        
        # Obtenemos la lista de fragmentos que el usuario definió
        fragmentos = self.obtener_fragmentos()
        if not fragmentos:
            messagebox.showwarning("Advertencia", "Estás agregando un slide sin contenido (fragmentos).")
        
        # Creamos el diccionario con la información del slide
        slide_data = {
            "titulo": titulo,
            "categoria": categoria,
            "contenido": fragmentos,
            # color_texto es un color "global" opcional (si tu generar_post lo requiere)
            "color_texto": self.slide_color.get().strip()
        }
        
        self.slides.append(slide_data)
        self.slide_listbox.insert(tk.END, titulo)
        
        # Limpiamos campos
        self.slide_titulo.delete(0, tk.END)
        self.slide_categoria.delete(0, tk.END)
        self.fragmentos_listbox.delete(0, tk.END)
        self.slide_color.set("texto")

    def eliminar_slide(self):
        """Elimina el slide seleccionado en el listbox de slides."""
        selected_index = self.slide_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Selecciona un slide para eliminar.")
            return
        
        index = selected_index[0]
        self.slide_listbox.delete(index)
        del self.slides[index]

    # ------------------------------------------------
    #   MÉTODO PARA GENERAR TODO EL CARRUSEL
    # ------------------------------------------------
    def generar_carrusel(self):
        try:
            # 1) Generar imagen de Portada
            portada_carrusel(
                titulo=self.portada_titulo.get().strip(),
                categoria=self.portada_categoria.get().strip(),
                output=self.portada_output.get().strip(),
                color_texto=self.portada_color.get().strip()  # Ajustado si tu portada admite color_texto
            )

            # 2) Generar imágenes de Slides de Contenido
            for i, slide in enumerate(self.slides, start=2):
                # Aquí asumes que tu generar_post admite color_texto como parámetro
                generar_post(
                    titulo=slide["titulo"],
                    contenido=slide["contenido"],  # Ojo: es una lista de (texto, color_key)
                    categoria=slide["categoria"],
                    output=f"solid_slide_{i}_post.png",
                    color_texto=slide["color_texto"]  # si lo deseas usar como fallback
                )

            # 3) Generar imagen de CTA
            slide_cta(
                bloque1=self.cta_bloque1.get().strip(),
                bloque2=self.cta_bloque2.get().strip(),
                bloque3=self.cta_bloque3.get().strip(),
                output=self.cta_output.get().strip(),
                color_texto=self.cta_color.get().strip()
            )

            messagebox.showinfo("Éxito", "¡El carrusel se generó correctamente!")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el carrusel:\n{e}")


if __name__ == "__main__":
    app = CarouselApp()
    app.mainloop()
