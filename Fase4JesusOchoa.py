import tkinter as tk
from tkinter import messagebox, ttk


class BSTNode:
  """representa un nodo individual dentro del arbol binario de busqueda (BST)."""

  def __init__(self, key: int):
    # valor entero almacenado en el nodo (clave de ordenamiento del ABB)
    self.key = key
    # referencia al hijo izquierdo (valores menores que self.key)
    self.left = None
    # referencia al hijo derecho (valores mayores que self.key)
    self.right = None
    # coordenada horizontal en pixeles dentro del Canvas para dibujar el nodo
    self.x = 0
    # coordenada vertical en pixeles dentro del Canvas para dibujar el nodo
    self.y = 0


class BinarySearchTree:
  """administra la estructura del ABB, inserción, busqueda, altura y recorridos"""

  def __init__(self):
    # nodo raiz del arbol binario de busqueda
    self.root = None
    # contador total de nodos insertados actualmente en el arbol
    self.node_count = 0

  def insert(self, key: int):
    """inserta una clave entera en el árbol respetando el límite máximo de 4 niveles"""
    # calcula la profundidad que tendría el nuevo nodo antes de insertarlo
    predicted_depth = self._get_insertion_depth(self.root, key, 1)
    # si supera el nivel 4, lanza una excepción para detener la inserción
    if predicted_depth > 4:
      raise ValueError(
          f"Cannot insert node {key}. This tree is limited to 4 levels. "
          f"Adding this node would create a level {predicted_depth}."
      )

    # inserta el nodo de forma recursiva y obtiene si se agregó exitosamente
    self.root, inserted = self._insert_recursive(self.root, key)
    if inserted:
      self.node_count += 1
    return inserted

  def _get_insertion_depth(self, node, key, current_depth):
    """calcula recursivamente en que nivel se ubicaria 'key'."""
    # si se llega a un espacio vacío, ese es el nivel destino
    if not node:
      return current_depth
    # desciende por el subarbol izquierdo si la clave es menor
    if key < node.key:
      return self._get_insertion_depth(node.left, key, current_depth + 1)
    # desciende por el subarbol derecho si la clave es mayor
    elif key > node.key:
      return self._get_insertion_depth(node.right, key, current_depth + 1)
    # Si la clave ya existe, retorna el nivel actual sin aumentar
    else:
      return current_depth

  def _insert_recursive(self, node, key):
    """inserta recursivamente un nuevo BSTNode en su posición correspondiente"""
    # caso base: crea y retorna el nuevo nodo
    if not node:
      return BSTNode(key), True
    # inserta a la izquierda si el valor es menor
    if key < node.key:
      node.left, inserted = self._insert_recursive(node.left, key)
    # inserta a la derecha si el valor es mayor
    elif key > node.key:
      node.right, inserted = self._insert_recursive(node.right, key)
    # evita duplicados exactos
    else:
      inserted = False
    return node, inserted

  def search(self, key: int):
    """busca una clave en el arbol y devuelve (encontrado, lista_de_ruta)"""
    # almacena el recorrido de nodos visitados durante la busqueda
    path = []
    # puntero auxiliar que inicia desde la raíz
    current = self.root

    while current:
      path.append(str(current.key))
      if key == current.key:
        return True, path
      elif key < current.key:
        current = current.left
      else:
        current = current.right

    return False, path

  def get_height(self, node=None):
    """calcula la altura (cantidad de niveles) del arbol o de un subarbol dado"""
    if node is None:
      node = self.root
    if not node:
      return 0
    # altura máxima entre el subárbol izquierdo y el derecho
    left_h = self.get_height(node.left) if node.left else 0
    right_h = self.get_height(node.right) if node.right else 0
    return 1 + max(left_h, right_h)

  def pre_order(self, node, result=None):
    """recorrido Preorden: raíz - izquierda - derecha"""
    if result is None:
      result = []
    if node:
      result.append(node.key)
      self.pre_order(node.left, result)
      self.pre_order(node.right, result)
    return result

  def in_order(self, node, result=None):
    """recorrido inorden: izquierda - raíz - derecha (orden ascendente en BST)"""
    if result is None:
      result = []
    if node:
      self.in_order(node.left, result)
      result.append(node.key)
      self.in_order(node.right, result)
    return result

  def post_order(self, node, result=None):
    """recorrido postorden: izquierda - derecha - raíz"""
    if result is None:
      result = []
    if node:
      self.post_order(node.left, result)
      self.post_order(node.right, result)
      result.append(node.key)
    return result

  def clear(self):
    """reinicia el arbol eliminando todos los nodos y reseteando el contador"""
    self.root = None
    self.node_count = 0


class GlassRoundedButton(tk.Canvas):
  """botón personalizado con esquinas redondeadas y efecto de reflejo"""

  def __init__(
      self,
      parent,
      text: str,
      command=None,
      bg_color: str = "#00F5D4",
      hover_color: str = "#4CC9F0",
      text_color: str = "#0B132B",
      border_color: str = "#A8FFEF",
      glass_shine: str = "#FFFFFF",
      parent_bg: str = "#0B132B",
      height: int = 40,
      radius: int = 12,
      font=("Segoe UI", 10, "bold"),
  ):
    # inicializa el lienzo que hará las veces de botón redondeado
    super().__init__(
        parent,
        height=height,
        bg=parent_bg, 
        highlightthickness=0,
        bd=0,
        cursor="hand2",
    )
    # texto visible dentro del botón
    self.text = text
    # función o método a ejecutar al hacer clic
    self.command = command
    # color base del botón
    self.bg_color = bg_color
    # color al pasar el cursor por encima (hover)
    self.hover_color = hover_color
    # color del texto del botón
    self.text_color = text_color
    # color del borde translúcido/neón
    self.border_color = border_color
    # color de la franja superior que simula el brillo del cristal
    self.glass_shine = glass_shine
    # radio de curvatura de las esquinas en píxeles
    self.radius = radius
    # tipografía del botón
    self.font = font
    # estado actual del cursor sobre el botón
    self._is_hovered = False
    # estado visual al presionar el botón
    self._is_pressed = False

    # eventos de redibujado y ratón
    self.bind("<Configure>", self._on_resize)
    self.bind("<Enter>", self._on_enter)
    self.bind("<Leave>", self._on_leave)
    self.bind("<ButtonPress-1>", self._on_press)
    self.bind("<ButtonRelease-1>", self._on_release)

  def _on_resize(self, event):
    """redibuja el botón cuando cambia su ancho disponible"""
    self._draw_button()

  def _on_enter(self, event):
    """activa el estado hover al entrar el puntero"""
    self._is_hovered = True
    self._draw_button()

  def _on_leave(self, event):
    """restaura el estado normal al salir el puntero"""
    self._is_hovered = False
    self._is_pressed = False
    self._draw_button()

  def _on_press(self, event):
    """simula el hundimiento leve al presionar el clic izquierdo"""
    self._is_pressed = True
    self._draw_button()

  def _on_release(self, event):
    """ejecuta el comando si se suelta el clic dentro del área del botón"""
    was_pressed = self._is_pressed
    self._is_pressed = False
    self._draw_button()

    w = self.winfo_width()
    h = self.winfo_height()
    if was_pressed and 0 <= event.x <= w and 0 <= event.y <= h and self.command:
      self.command()

  def _create_rounded_rect_points(self, x1, y1, x2, y2, r):
    """genera los puntos suavizados para dibujar un rectángulo con esquinas redondeadas"""
    points = [
        x1 + r,
        y1,
        x2 - r,
        y1,
        x2,
        y1,
        x2,
        y1 + r,
        x2,
        y2 - r,
        x2,
        y2,
        x2 - r,
        y2,
        x1 + r,
        y2,
        x1,
        y2,
        x1,
        y2 - r,
        x1,
        y1 + r,
        x1,
        y1,
    ]
    return points

  def _draw_button(self):
    """dibuja el cuerpo redondeado, el reflejo superior tipo cristal y el texto centrado"""
    self.delete("all")
    w = self.winfo_width()
    h = self.winfo_height()
    if w <= 4 or h <= 4:
      return

    # define el color activo según hover/presión
    fill_col = self.hover_color if self._is_hovered else self.bg_color
    offset_y = 1 if self._is_pressed else 0
    r = min(self.radius, h // 2, w // 4)

    # cuerpo principal redondeado
    body_pts = self._create_rounded_rect_points(
        2, 2 + offset_y, w - 2, h - 2 + offset_y, r
    )
    self.create_polygon(
        body_pts, smooth=True, fill=fill_col, outline=self.border_color, width=1
    )

    # franja superior con efecto reflejo
    glass_h = max(6, (h - 4) // 2)
    if h > 14:
      glass_pts = self._create_rounded_rect_points(
          4, 3 + offset_y, w - 4, 3 + glass_h + offset_y, max(4, r - 2)
      )
      self.create_polygon(
          glass_pts,
          smooth=True,
          fill=self.glass_shine,
          stipple="gray25",
          outline="",
      )

    # texto centrado del botón
    self.create_text(
        w // 2,
        (h // 2) + offset_y,
        text=self.text,
        font=self.font,
        fill=self.text_color,
    )


class LoginWindow:
  """ventana inicial de acceso con contraseña enmascarada, botón de visualización"""

  def __init__(self, root):
    # ventana raíz de inicio de sesión
    self.root = root
    self.root.title("Fase4JesusOchoa - Login")
    self.root.geometry("480x550")
    self.root.minsize(480, 550)
    self.root.configure(bg="#0B132B")

    # Estado booleano que indica si la contraseña está visible o enmascarada
    self._password_visible = False

    # Centra la ventana y construye los controles visuales
    self._center_window()
    self._create_widgets()

  def _center_window(self):
    """centra la ventana de login en la pantalla del usuario"""
    self.root.update_idletasks()
    width = self.root.winfo_width()
    height = self.root.winfo_height()
    x = (self.root.winfo_screenwidth() // 2) - (width // 2)
    y = (self.root.winfo_screenheight() // 2) - (height // 2)
    self.root.geometry(f"{width}x{height}+{x}+{y}")

  def _create_widgets(self):
    """crea el encabezado, la información del estudiante, el campo de clave con botón y el acceso"""
    # contenedor del título principal
    header_frame = tk.Frame(self.root, bg="#1C2541", bd=2, relief="flat")
    header_frame.pack(fill="x", padx=20, pady=20)

    title_lbl = tk.Label(
        header_frame,
        text="⚡ BST Explorer",
        font=("Segoe UI", 20, "bold"),
        fg="#00F5D4",
        bg="#1C2541",
    )
    title_lbl.pack(pady=(15, 5))

    subtitle_lbl = tk.Label(
        header_frame,
        text="Binary Search Tree • Phase 4",
        font=("Segoe UI", 11),
        fg="#4CC9F0",
        bg="#1C2541",
    )
    subtitle_lbl.pack(pady=(0, 15))

    # tarjeta con los metadatos de la aplicación y el estudiante
    info_frame = tk.Frame(self.root, bg="#1C2541", bd=1, relief="solid")
    info_frame.pack(fill="x", padx=20, pady=5)

    details = [
        ("Application:", "Fase4JesusOchoa"),
        ("Student:", "Jesús Mauricio Ochoa Pinilla"),
        ("Course:", "Data Structures • 301305_218"),
        ("Date:", "November, 2026"),
    ]

    for lbl_text, val_text in details:
      row_f = tk.Frame(info_frame, bg="#1C2541")
      row_f.pack(fill="x", padx=15, pady=4)
      tk.Label(
          row_f,
          text=lbl_text,
          font=("Segoe UI", 10, "bold"),
          fg="#8D99AE",
          bg="#1C2541",
          width=13,
          anchor="w",
      ).pack(side="left")
      tk.Label(
          row_f,
          text=val_text,
          font=("Segoe UI", 10),
          fg="#FFFFFF",
          bg="#1C2541",
          anchor="w",
      ).pack(side="left", fill="x", expand=True)

    # sección de ingreso de contraseña enmascarada
    pass_frame = tk.Frame(self.root, bg="#0B132B")
    pass_frame.pack(fill="x", padx=20, pady=20)

    tk.Label(
        pass_frame,
        text="Enter Access Password:",
        font=("Segoe UI", 10, "bold"),
        fg="#00F5D4",
        bg="#0B132B",
        anchor="w",
    ).pack(fill="x", pady=(0, 5))

    # contenedor horizontal para el campo de texto y el botón de mostrar/ocultar clave
    entry_row = tk.Frame(pass_frame, bg="#0B132B")
    entry_row.pack(fill="x", pady=(0, 5))

    # campo de texto oculto con guiones largos para enmascarar la contraseña por defecto
    self.pass_entry = ttk.Entry(entry_row, font=("Segoe UI", 12), show="*")
    self.pass_entry.pack(
        side="left", fill="x", expand=True, ipady=6, padx=(0, 8)
    )
    self.pass_entry.focus()
    self.pass_entry.bind("<Return>", lambda e: self._verify_login())

    # botón interactivo para alternar la visibilidad de la clave digitada antes de ingresar
    self.toggle_btn = tk.Button(
        entry_row,
        text="👁 Show",
        font=("Segoe UI", 9, "bold"),
        bg="#1C2541",
        fg="#00F5D4",
        activebackground="#4CC9F0",
        activeforeground="#0B132B",
        relief="flat",
        cursor="hand2",
        width=9,
        command=self._toggle_password_visibility,
    )
    self.toggle_btn.pack(side="right", ipady=6)

    # etiqueta informativa sobre el estado de enmascaramiento de la contraseña
    self.mask_status_lbl = tk.Label(
        pass_frame,
        text=(
            "Password is masked (****). Click 'Show' to preview before"
            " entering."
        ),
        font=("Segoe UI", 8, "italic"),
        fg="#8D99AE",
        bg="#0B132B",
        anchor="w",
    )
    self.mask_status_lbl.pack(fill="x")

    # botón redondeado con efecto cristal para acceder al explorador BST
    btn_frame = tk.Frame(self.root, bg="#0B132B")
    btn_frame.pack(fill="x", padx=20, pady=10)

    login_btn = GlassRoundedButton(
        btn_frame,
        text="Access BST Explorer",
        command=self._verify_login,
        bg_color="#00F5D4",
        hover_color="#4CC9F0",
        text_color="#0B132B",
        border_color="#CFFAFE",
        glass_shine="#FFFFFF",
        parent_bg="#0B132B",
        height=44,
        radius=14,
        font=("Segoe UI", 11, "bold"),
    )
    login_btn.pack(fill="x")

    # pie de página institucional
    footer_lbl = tk.Label(
        self.root,
        text="UNAD • ECBTI • Systems Engineering",
        font=("Segoe UI", 8),
        fg="#4361EE",
        bg="#0B132B",
    )
    footer_lbl.pack(pady=10)

  def _toggle_password_visibility(self):
    """alterna entre mostrar en texto claro la clave digitada y enmascararla nuevamente"""
    self._password_visible = not self._password_visible
    if self._password_visible:
      # muestra los caracteres reales digitados por el usuario
      self.pass_entry.config(show="")
      self.toggle_btn.config(text="👁 Hide", bg="#4CC9F0", fg="#0B132B")
      self.mask_status_lbl.config(
          text="Password is visible. Click 'Hide' to mask it again."
      )
    else:
      # vuelve a enmascarar la contraseña con asteriscos
      self.pass_entry.config(show="*")
      self.toggle_btn.config(text="👁 Show", bg="#1C2541", fg="#00F5D4")
      self.mask_status_lbl.config(
          text=(
              "Password is masked (****). Click 'Show' to preview before"
              " entering."
          )
      )

  def _verify_login(self):
    """valida la contraseña 'UNAD' que sea correcta"""
    entered_pass = self.pass_entry.get().strip()

    # validación cuando el usuario deja el campo vacío
    if not entered_pass:
      messagebox.showwarning(
          "Authentication Required",
          "Please enter your access password to continue.",
          parent=self.root,
      )
      self.pass_entry.focus()
      return

    if entered_pass == "UNAD":
      self.root.destroy()
      main_root = tk.Tk()
      MainWindow(main_root)
      main_root.mainloop()
    else:
      # mensaje de error si la contraseña es incorrecta
      messagebox.showerror(
          "Authentication Failed",
          "Invalid credentials. The password entered does not match our"
          " records.\nPlease verify your password and try again.",
          parent=self.root,
      )
      self.pass_entry.delete(0, tk.END)
      self.pass_entry.focus()


class MainWindow:
  """ventana principal del explorador BST con lienzo estilo blueprint y recorridos"""

  def __init__(self, root):
    # ventana principal de la aplicación
    self.root = root
    self.root.title("Fase4JesusOchoa — BST Explorer (Binary Search Tree)")
    self.root.geometry("1280x768")
    self.root.minsize(1024, 650)
    self.root.configure(bg="#0B132B")

    # instancia del arbol binario de búsqueda
    self.bst = BinarySearchTree()
    # clave del último nodo encontrado o insertado para resaltarlo
    self.found_node_key = None
    # lista de nodos que forman parte de la última ruta de búsqueda
    self.search_path_nodes = []

    # construye la interfaz principal
    self._create_main_layout()

  def _create_main_layout(self):
    """configura la barra superior, el panel de controles y el área de visualización"""
    # Barra superior con título y mis datos 
    top_bar = tk.Frame(self.root, bg="#1C2541", height=50)
    top_bar.pack(fill="x", side="top")

    brand_lbl = tk.Label(
        top_bar,
        text=" ⚡ BST Explorer — Binary Search Tree (Phase 4)",
        font=("Segoe UI", 12, "bold"),
        fg="#00F5D4",
        bg="#1C2541",
    )
    brand_lbl.pack(side="left", padx=15, pady=10)

    user_info = "Jesús Mauricio Ochoa Pinilla | Data Structures - 301305:_218"
    user_lbl = tk.Label(
        top_bar,
        text=user_info,
        font=("Segoe UI", 10),
        fg="#4CC9F0",
        bg="#1C2541",
    )
    user_lbl.pack(side="right", padx=15, pady=10)

    # contenedor central dividido en panel izquierdo y panel derecho
    body_frame = tk.Frame(self.root, bg="#0B132B")
    body_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # panel izquierdo: Controles, estadísticas y leyenda
    left_panel = tk.Frame(
        body_frame, bg="#111827", width=300, bd=1, relief="solid"
    )
    left_panel.pack(side="left", fill="y", padx=(0, 10))
    left_panel.pack_propagate(False)

    ctrl_title = tk.Label(
        left_panel,
        text="⚙️ Controls",
        font=("Segoe UI", 11, "bold"),
        fg="#00F5D4",
        bg="#111827",
        anchor="w",
    )
    ctrl_title.pack(fill="x", padx=15, pady=(15, 5))

    input_frame = tk.Frame(left_panel, bg="#111827")
    input_frame.pack(fill="x", padx=15, pady=5)

    tk.Label(
        input_frame,
        text="Node Value (Integer):",
        font=("Segoe UI", 9, "bold"),
        fg="#D1D5DB",
        bg="#111827",
        anchor="w",
    ).pack(fill="x", pady=(0, 3))

    # entrada numérica para agregar o buscar valores enteros
    self.node_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
    self.node_entry.pack(fill="x", ipady=4, pady=(0, 10))
    self.node_entry.focus()
    self.node_entry.bind("<Return>", lambda e: self._add_node())

    # configuración de los 4 botones redondeados con efecto cristal
    btn_configs = [
        ("➕ Add Node", "#00F5D4", "#38BDF8", "#0B132B", "#E0F2FE", self._add_node),
        (
            "🔍 Search Node",
            "#4CC9F0",
            "#00F5D4",
            "#0B132B",
            "#E0F2FE",
            self._search_node,
        ),
        (
            "🧹 Clear Tree",
            "#F72585",
            "#B5179E",
            "#FFFFFF",
            "#FBCFE8",
            self._clear_tree,
        ),
        ("🚪 Exit", "#334155", "#475569", "#FFFFFF", "#CBD5E1", self._exit_app),
    ]

    for text, bg_col, hover_col, fg_col, shine_col, cmd in btn_configs:
      b = GlassRoundedButton(
          input_frame,
          text=text,
          command=cmd,
          bg_color=bg_col,
          hover_color=hover_col,
          text_color=fg_col,
          border_color=shine_col,
          glass_shine="#FFFFFF",
          parent_bg="#111827",
          height=38,
          radius=12,
          font=("Segoe UI", 10, "bold"),
      )
      b.pack(fill="x", pady=4)

    # sección de estadísticas dinámicas del arbol
    stat_title = tk.Label(
        left_panel,
        text="📊 Tree Statistics",
        font=("Segoe UI", 11, "bold"),
        fg="#00F5D4",
        bg="#111827",
        anchor="w",
    )
    stat_title.pack(fill="x", padx=15, pady=(20, 5))

    stat_frame = tk.Frame(left_panel, bg="#1F2937", bd=1, relief="flat")
    stat_frame.pack(fill="x", padx=15, pady=5)

    self.stat_nodes_lbl = tk.Label(
        stat_frame,
        text="nodes: 0",
        font=("Consolas", 10),
        fg="#E5E7EB",
        bg="#1F2937",
        anchor="w",
    )
    self.stat_nodes_lbl.pack(fill="x", padx=10, pady=4)

    self.stat_height_lbl = tk.Label(
        stat_frame,
        text="height: 0",
        font=("Consolas", 10),
        fg="#E5E7EB",
        bg="#1F2937",
        anchor="w",
    )
    self.stat_height_lbl.pack(fill="x", padx=10, pady=4)

    self.stat_root_lbl = tk.Label(
        stat_frame,
        text="root: —",
        font=("Consolas", 10),
        fg="#E5E7EB",
        bg="#1F2937",
        anchor="w",
    )
    self.stat_root_lbl.pack(fill="x", padx=10, pady=(4, 10))

    # leyenda de colores de los nodos en el arbol
    legend_title = tk.Label(
        left_panel,
        text="🎨 Legend",
        font=("Segoe UI", 11, "bold"),
        fg="#00F5D4",
        bg="#111827",
        anchor="w",
    )
    legend_title.pack(fill="x", padx=15, pady=(20, 5))

    legend_frame = tk.Frame(left_panel, bg="#111827")
    legend_frame.pack(fill="x", padx=15, pady=5)

    legends = [
        ("● Regular node", "#00B4D8"),
        ("● Found node", "#7209B7"),
        ("● Search path", "#F72585"),
        ("● Traversal node", "#FFB703"),
    ]
    for l_text, l_color in legends:
      tk.Label(
          legend_frame,
          text=l_text,
          font=("Segoe UI", 9),
          fg=l_color,
          bg="#111827",
          anchor="w",
      ).pack(fill="x", pady=2)

    # etiqueta inferior de estado de la aplicación
    self.status_lbl = tk.Label(
        left_panel,
        text="Ready. Max 4 levels allowed.",
        font=("Segoe UI", 8, "italic"),
        fg="#9CA3AF",
        bg="#111827",
        wraplength=270,
        justify="left",
    )
    self.status_lbl.pack(side="bottom", fill="x", padx=15, pady=15)

    # panel derecho: lienzo blueprint y paneles de recorridos
    right_panel = tk.Frame(body_frame, bg="#0B132B")
    right_panel.pack(side="right", fill="both", expand=True)

    canvas_container = tk.Frame(right_panel, bg="#111827", bd=1, relief="solid")
    canvas_container.pack(fill="both", expand=True, pady=(0, 10))

    canvas_header = tk.Frame(canvas_container, bg="#1F2937", height=30)
    canvas_header.pack(fill="x")
    tk.Label(
        canvas_header,
        text=" 📐 BST Tree [max 4 levels] — Blueprint Grid",
        font=("Segoe UI", 10, "bold"),
        fg="#00F5D4",
        bg="#1F2937",
    ).pack(side="left", padx=10, pady=5)

    # lienzo donde se dibujan la cuadrícula blueprint y el arbol binario
    self.canvas = tk.Canvas(canvas_container, bg="#0B132B", highlightthickness=0)
    self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
    self.canvas.bind("<Configure>", lambda e: self._redraw_tree())

    # contenedor inferior para Pre-order, In-order y Post-order
    trav_container = tk.Frame(right_panel, bg="#0B132B", height=160)
    trav_container.pack(fill="x", ipady=5)
    trav_container.pack_propagate(False)

    trav_panels = [
        ("🔹 Pre-order", self._create_trav_subpanel(trav_container, "Pre-order")),
        ("🔸 In-order", self._create_trav_subpanel(trav_container, "In-order")),
        ("🔹 Post-order", self._create_trav_subpanel(trav_container, "Post-order")),
    ]

    # diccionario para actualizar el texto de cada recorrido fácilmente
    self.trav_labels = {}
    for title, (_, l_widget) in trav_panels:
      self.trav_labels[title] = l_widget

  def _create_trav_subpanel(self, parent, title):
    """crea un subpanel individual para mostrar los valores de un recorrido"""
    frame = tk.Frame(parent, bg="#111827", bd=1, relief="solid")
    frame.pack(side="left", fill="both", expand=True, padx=3)

    hdr = tk.Frame(frame, bg="#1F2937", height=26)
    hdr.pack(fill="x")
    tk.Label(
        hdr,
        text=title,
        font=("Segoe UI", 9, "bold"),
        fg="#00F5D4",
        bg="#1F2937",
    ).pack(side="left", padx=8, pady=3)

    content_f = tk.Frame(frame, bg="#111827")
    content_f.pack(fill="both", expand=True, padx=8, pady=8)

    lbl = tk.Label(
        content_f,
        text="No data yet.",
        font=("Consolas", 9),
        fg="#9CA3AF",
        bg="#111827",
        wraplength=300,
        justify="left",
    )
    lbl.pack(fill="both", expand=True)

    return frame, lbl

  def _add_node(self):
    """valida el dato ingresado y agrega el nodo al arbol si no excede 4 niveles"""
    val_str = self.node_entry.get().strip()
    if not val_str:
      messagebox.showwarning(
          "Warning", "Please enter an integer value.", parent=self.root
      )
      return

    # intenta convertir el texto a número entero
    try:
      val = int(val_str)
    except ValueError:
      messagebox.showerror(
          "Invalid Input",
          f"'{val_str}' is not a valid integer.\nOnly whole numbers are"
          " accepted (10, 5, 42).",
          parent=self.root,
      )
      self.node_entry.delete(0, tk.END)
      self.node_entry.focus()
      return

    # intenta insertar en el ABB controlando el límite de profundidad
    try:
      inserted = self.bst.insert(val)
      if not inserted:
        messagebox.showinfo(
            "Duplicate", f"Node {val} already exists in the BST.", parent=self.root
        )
      else:
        self.status_lbl.config(text=f"Node {val} added successfully.")
        self.found_node_key = val
        self.search_path_nodes = []
        self._update_ui()
    except ValueError as e:
      messagebox.showerror("Maximum Depth Reached", str(e), parent=self.root)

    self.node_entry.delete(0, tk.END)
    self.node_entry.focus()

  def _search_node(self):
    """busca un valor entero en el arbol, muestra la ruta y resalta el resultado"""
    val_str = self.node_entry.get().strip()
    if not val_str:
      messagebox.showwarning(
          "Warning",
          "Please enter an integer value to search.",
          parent=self.root,
      )
      return

    try:
      val = int(val_str)
    except ValueError:
      messagebox.showerror(
          "Invalid Input", f"'{val_str}' is not a valid integer.", parent=self.root
      )
      return

    found, path = self.bst.search(val)
    if found:
      self.found_node_key = val
      self.search_path_nodes = [int(p) for p in path]
      messagebox.showinfo(
          "Node Found",
          f"Node {val} was found in the tree.\nSearch path:"
          f" {' ➔ '.join(path)}",
          parent=self.root,
      )
      self.status_lbl.config(
          text=f"Node {val} found in tree. Path: {' -> '.join(path)}"
      )
    else:
      self.found_node_key = None
      self.search_path_nodes = []
      messagebox.showwarning(
          "Node Not Found",
          f"Node {val} does not exist in the BST.",
          parent=self.root,
      )
      self.status_lbl.config(text=f"Node {val} not found.")

    self._redraw_tree()
    self.node_entry.delete(0, tk.END)
    self.node_entry.focus()

  def _clear_tree(self):
    """limpia por completo el arbol, los recorridos y los indicadores visuales"""
    if not self.bst.root:
      return
    if messagebox.askyesno(
        "Clear Tree",
        "Are you sure you want to clear the entire BST?",
        parent=self.root,
    ):
      self.bst.clear()
      self.found_node_key = None
      self.search_path_nodes = []
      self.status_lbl.config(text="Tree cleared successfully.")
      self._update_ui()

  def _exit_app(self):
    """solicita confirmación y cierra la ventana principal"""
    if messagebox.askyesno(
        "Exit", "Do you want to close the application?", parent=self.root
    ):
      self.root.destroy()

  def _update_ui(self):
    """actualiza estadísticas, recorridos (preorden, inorden, postorden) y gráfico"""
    nodes_cnt = self.bst.node_count
    height_val = self.bst.get_height() if nodes_cnt > 0 else 0
    root_val = self.bst.root.key if self.bst.root else "—"

    self.stat_nodes_lbl.config(text=f"nodes: {nodes_cnt}")
    self.stat_height_lbl.config(text=f"height: {height_val}")
    self.stat_root_lbl.config(text=f"root: {root_val}")

    pre = self.bst.pre_order(self.bst.root)
    ino = self.bst.in_order(self.bst.root)
    post = self.bst.post_order(self.bst.root)

    self.trav_labels["🔹 Pre-order"].config(
        text=", ".join(map(str, pre)) if pre else "Empty tree."
    )
    self.trav_labels["🔸 In-order"].config(
        text=", ".join(map(str, ino)) if ino else "Empty tree."
    )
    self.trav_labels["🔹 Post-order"].config(
        text=", ".join(map(str, post)) if post else "Empty tree."
    )

    self._redraw_tree()

  def _draw_blueprint_grid(self, w, h):
    """dibuja la cuadrícula estilo blueprint en el lienzo"""
    grid_size = 40
    for x in range(0, w, grid_size):
      self.canvas.create_line(x, 0, x, h, fill="#13315C", width=1)
    for y in range(0, h, grid_size):
      self.canvas.create_line(0, y, w, y, fill="#13315C", width=1)

  def _redraw_tree(self):
    """limpia el lienzo y redibuja la cuadrícula, las conexiones y los nodos"""
    self.canvas.delete("all")
    w = self.canvas.winfo_width()
    h = self.canvas.winfo_height()
    if w < 100 or h < 100:
      return

    self._draw_blueprint_grid(w, h)

    if not self.bst.root:
      self.canvas.create_text(
          w // 2,
          h // 2,
          text="Empty Tree — Add nodes using the left control panel.",
          font=("Segoe UI", 12),
          fill="#6B7280",
      )
      return

    self._assign_coords(self.bst.root, w / 2, 50, w / 4, 1)
    self._draw_edges(self.bst.root)
    self._draw_nodes(self.bst.root)

  def _assign_coords(self, node, x, y, offset, level):
    """calcula recursivamente las coordenadas (x, y) de cada nodo según su nivel"""
    if not node:
      return
    node.x = x
    node.y = y
    next_offset = max(offset / 2, 30)
    if node.left:
      self._assign_coords(node.left, x - offset, y + 75, next_offset, level + 1)
    if node.right:
      self._assign_coords(
          node.right, x + offset, y + 75, next_offset, level + 1
      )

  def _draw_edges(self, node):
    """dibuja las líneas que conectan cada nodo padre con sus hijos"""
    if not node:
      return
    if node.left:
      self.canvas.create_line(
          node.x, node.y, node.left.x, node.left.y, fill="#38BDF8", width=2
      )
      self._draw_edges(node.left)
    if node.right:
      self.canvas.create_line(
          node.x, node.y, node.right.x, node.right.y, fill="#38BDF8", width=2
      )
      self._draw_edges(node.right)

  def _draw_nodes(self, node):
    """dibuja los círculos y etiquetas de cada nodo en el lienzo"""
    if not node:
      return

    r = 22
    fill_color = "#00B4D8"
    if node.key == self.found_node_key:
      fill_color = "#7209B7"
    elif node.key in self.search_path_nodes:
      fill_color = "#F72585"

    self.canvas.create_oval(
        node.x - r,
        node.y - r,
        node.x + r,
        node.y + r,
        fill=fill_color,
        outline="#FFFFFF",
        width=2,
    )
    self.canvas.create_text(
        node.x,
        node.y,
        text=str(node.key),
        font=("Segoe UI", 10, "bold"),
        fill="#FFFFFF",
    )

    self._draw_nodes(node.left)
    self._draw_nodes(node.right)


if __name__ == "__main__":
  main_root = tk.Tk()
  LoginWindow(main_root)
  main_root.mainloop()