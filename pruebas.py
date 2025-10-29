import pygame
import os
import math  # ### NUEVO ### Importar math y numpy
import numpy as np

# --- Algoritmo Bresenham para líneas ---
def bresenham(screen, x1, y1, x2, y2, color):
    # (Tu código de bresenham... está un poco incompleto,
    # le falta el último punto, lo corrijo)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    if dx > dy:
        err = dx / 2.0
        # Bucle debe correr dx + 1 veces para incluir el último punto
        for _ in range(int(dx) + 1):
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        # Bucle debe correr dy + 1 veces
        for _ in range(int(dy) + 1):
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

# Algoritmo DDA para líneas
def dda(screen, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    
    steps = int(max(abs(dx), abs(dy)))
    # Evitar división por cero si los puntos son iguales
    if steps == 0:
        pygame.draw.circle(screen, color, (round(x1), round(y1)), 1)
        return

    x_inc = dx / steps
    y_inc = dy / steps
    x, y = float(x1), float(y1)
    
    # +1 para incluir el último punto
    for _ in range(steps + 1):
        pygame.draw.circle(screen, color, (round(x), round(y)), 1)
        x += x_inc
        y += y_inc
        
# --- Algoritmo Bresenham para circulos ---
def bresenham_circle(screen, cx, cy, r, color):
    # (Tu código de bresenham_circle va aquí...)
    x = 0
    y = r
    d = 3 - 2 * r
    def plot_circle_points(x, y):
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        for point in points:
            pygame.draw.circle(screen, color, point, 1)

    while x <= y: 
        plot_circle_points(x, y)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

# Algoritmo de Bézier 
def bezier(screen, p0, p1, p2, p3, steps, color):
    # (Tu código de bezier va aquí...)
    t_values = np.linspace(0, 1, steps)
    points = []
    for t in t_values:
        x = (1-t)**3 * p0[0] + 3 * (1-t)**2 * t * p1[0] + 3 * (1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3 * (1-t)**2 * t * p1[1] + 3 * (1-t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((int(x), int(y)))
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 2)
        
#Triangulos y Poligonos
def draw_triangle(screen, vertices, color):
    # (Tu código de draw_triangle va aquí...)
    if len(vertices) != 3: return
    draw_polygon(screen, vertices, color)
        
def draw_polygon(screen, vertices, color):
    # (Tu código de draw_polygon va aquí...)
    if len(vertices) < 2: return
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        dda(screen, x1, y1, x2, y2, color)
        
#Rectangulos
def draw_rectangle(screen, x, y, width, height, color):
    # (Tu código de draw_rectangle va aquí...)
    vertices = [
        (x, y), (x + width, y),
        (x + width, y + height), (x, y + height)
    ]
    draw_polygon(screen, vertices, color)

#Elipsis
def draw_ellipse(screen, cx, cy, rx, ry, color):
    # (Tu código de draw_ellipse va aquí...)
    t_values = np.linspace(0, 2 * math.pi, 100)
    points = []
    for t in t_values:
        x = cx + rx * math.cos(t)
        y = cy + ry * math.sin(t)
        points.append((int(x), int(y)))
    if len(points) > 1:
        # True para cerrar la elipse
        pygame.draw.lines(screen, color, True, points, 2)

# --- Fin de Algoritmos ---

pygame.init()

# Colores para panel y borde
PANEL_BG = (99, 99, 99)
PANEL_BORDER = (0, 0, 0)
PANEL_FBG = (234, 219, 255)
#- Colores para dibujar
COLOR_AZUL = (0, 120, 250)
COLOR_VERDE = (50, 200, 50)
COLOR_ROJO = (200, 50, 50)
COLOR_MORADO = (100, 50, 200)
COLOR_AMARILLO = (200, 200, 50)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
# Clase Boton
class Boton:
   def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, color_texto=(0, 0, 0), fuente=None, icon_surface=None):
      """Botón simple que puede mostrar texto o una Surface (icon_surface) centrada dentro."""
      self.rect = pygame.Rect(x, y, ancho, alto)
      self.texto = texto
      self.color_normal = color_normal
      self.color_hover = color_hover
      self.color_texto = color_texto
      self.fuente = fuente or pygame.font.Font(None, 36)
      self.hover = False
      # superficie opcional que se mostrará centrada dentro del botón (preescalada si se asigna así)
      self.icon_surface = icon_surface

   def dibujar(self, pantalla):
      """Dibuja el botón en pantalla; si tiene `icon_surface` la escala/centra dentro con padding."""
      color_actual = self.color_hover if self.hover else self.color_normal
      pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)

      # si hay un icon_surface, dibujarlo centrado dentro del botón
      if self.icon_surface:
         pad = 8
         inner_w = max(1, self.rect.width - pad*2)
         inner_h = max(1, self.rect.height - pad*2)
         icon = self.icon_surface
         # escalar icon a inner size (manteniendo aspecto o forzando llenar)
         scaled = pygame.transform.smoothscale(icon, (inner_w, inner_h))
         srect = scaled.get_rect(center=self.rect.center)
         pantalla.blit(scaled, srect)
      else:
         # Renderizar texto centrado (por si se usa)
         if self.texto:
            texto_render = self.fuente.render(self.texto, True, self.color_texto)
            texto_rect = texto_render.get_rect(center=self.rect.center)
            pantalla.blit(texto_render, texto_rect)

   def actualizar(self, eventos):
      """Actualiza el estado del botón (detecta hover y clics)."""
      mouse_pos = pygame.mouse.get_pos()
      self.hover = self.rect.collidepoint(mouse_pos)

      for evento in eventos:
         if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.hover:
               return True  # Retorna True si se hace clic sobre el botón
      return False

# ---------------------------
# Ejemplo de uso
# ---------------------------
if __name__ == "__main__":
   pantalla = pygame.display.set_mode((1000, 680))
   pygame.display.set_caption("Ejemplo de Botones con POO y Pygame")
   reloj = pygame.time.Clock()

   # ### NUEVO ### - Definir paneles y ÁREA DE DIBUJO
   panel_form_rect = pygame.Rect(20, 20, 140, 650)
   panel_color_rect = pygame.Rect(850, 20, 130, 650)
   
   # El área de dibujo es el espacio entre los paneles
   drawable_x = panel_form_rect.right + 10
   drawable_y = panel_form_rect.top
   drawable_w = panel_color_rect.left - drawable_x - 10
   drawable_h = panel_form_rect.height
   drawable_rect = pygame.Rect(drawable_x, drawable_y, drawable_w, drawable_h)   
   
   # - Crear el LIENZO para dibujar
   # Usamos (237, 237, 237) que es tu color de fondo
   lienzo_surface = pygame.Surface(drawable_rect.size)
   lienzo_surface.fill((237, 237, 237))
    
   # Crear botones de colores (columna)
   boton_azul = Boton(890, 30, 50, 50, "", COLOR_AZUL, (0, 180, 255))
   boton_verde = Boton(890, 100, 50, 50, "", COLOR_VERDE, (80, 255, 80))
   boton_rojo = Boton(890, 170, 50, 50, "", COLOR_ROJO, (255, 80, 80))
   boton_morado = Boton(890, 240, 50, 50, "", COLOR_MORADO, (150, 80, 255))
   boton_amarillo = Boton(890, 310, 50, 50, "", COLOR_AMARILLO, (255, 255, 80))
   boton_blanco = Boton(890, 380, 50, 50, "", COLOR_BLANCO, (200, 200, 200)) # hover gris claro
   boton_negro = Boton(890, 450, 50, 50, "", COLOR_NEGRO, (80, 80, 80))

   # Agrupar botones para calcular el área de fondo automáticamente
   botones_columna = [boton_azul, boton_verde, boton_rojo, boton_morado, boton_amarillo, boton_blanco, boton_negro]


   boton_linea = Boton(50, 30, 80, 70, "LINEA", PANEL_FBG, PANEL_FBG)
   linea_ruta = os.path.join(os.path.dirname(__file__), 'linea.png')
   if os.path.exists(linea_ruta):
      try:
         img = pygame.image.load(linea_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_linea.rect.width - pad*2)
         inner_h = max(1, boton_linea.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_linea.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", linea_ruta, e)

   boton_curva = Boton(50, 130, 80, 70, "CURVA", PANEL_FBG, PANEL_FBG)
   curva_ruta = os.path.join(os.path.dirname(__file__), 'curva.png')
   if os.path.exists(curva_ruta):
      try:
         img = pygame.image.load(curva_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_curva.rect.width - pad*2)
         inner_h = max(1, boton_curva.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_curva.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", curva_ruta, e)

   boton_rect = Boton(50, 220, 80, 70, "RECTANGULO", PANEL_FBG, PANEL_FBG)
   recta_ruta = os.path.join(os.path.dirname(__file__), 'rectangulo.png')
   if os.path.exists(recta_ruta):
      try:
         img = pygame.image.load(recta_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_rect.rect.width - pad*2)
         inner_h = max(1, boton_rect.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_rect.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", recta_ruta, e)

   boton_circ = Boton(50, 310, 80, 70, "CIRCULO", PANEL_FBG, PANEL_FBG)
   circ_ruta = os.path.join(os.path.dirname(__file__), 'circulo.png')
   if os.path.exists(circ_ruta):
      try:
         img = pygame.image.load(circ_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_circ.rect.width - pad*2)
         inner_h = max(1, boton_circ.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_circ.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", circ_ruta, e)

   boton_tri = Boton(50, 400, 80, 70, "TRIANGULO", PANEL_FBG, PANEL_FBG)
   triangulo_ruta = os.path.join(os.path.dirname(__file__), 'triangulo.png')
   if os.path.exists(triangulo_ruta):
      try:
         img = pygame.image.load(triangulo_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_tri.rect.width - pad*2)
         inner_h = max(1, boton_tri.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_tri.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", triangulo_ruta, e)

   boton_elipse = Boton(50, 490, 80, 70, "ELIPSE", PANEL_FBG, PANEL_FBG)
   elipse_ruta = os.path.join(os.path.dirname(__file__), 'elipse.png')
   if os.path.exists(elipse_ruta):
      try:
         img = pygame.image.load(elipse_ruta).convert_alpha()
         pad = 8
         inner_w = max(1, boton_elipse.rect.width - pad*2)
         inner_h = max(1, boton_elipse.rect.height - pad*2)
         iw, ih = img.get_size()
         scale = min(inner_w / iw, inner_h / ih)
         new_w = max(1, int(iw * scale))
         new_h = max(1, int(ih * scale))
         img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
         icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
         ox = (inner_w - new_w) // 2
         oy = (inner_h - new_h) // 2
         icon_surface.blit(img_scaled, (ox, oy))
         boton_elipse.icon_surface = icon_surface
      except Exception as e:
            print("Error cargando", elipse_ruta, e)

   boton_poligono = Boton(50, 580, 80, 70, "POLIGONO", PANEL_FBG, PANEL_FBG)
   boton_limpiar = Boton(865, 580, 100, 50, "LIMPIAR", PANEL_FBG, PANEL_FBG)

   botones_formas = [boton_linea, boton_curva, boton_rect, boton_circ, boton_tri, boton_elipse, boton_poligono, boton_limpiar]
# - Variables de Estado
   current_tool = None
   current_color = COLOR_NEGRO # Color por defecto
   points = [] # Lista para guardar los clics del usuario

   ejecutando = True
   while ejecutando:
      eventos = pygame.event.get()
      for evento in eventos:
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            # ### NUEVO ### - Lógica de CLICS EN EL LIENZO
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_pantalla = evento.pos
                
                # Comprobar si el clic fue DENTRO del área de dibujo
                if drawable_rect.collidepoint(pos_pantalla):
                    # Convertir coordenadas de pantalla a coordenadas de LIENZO
                    pos_lienzo = (pos_pantalla[0] - drawable_rect.x,
                                  pos_pantalla[1] - drawable_rect.y)
                    
                    points.append(pos_lienzo)
                    
                    # Dibujar un punto de feedback
                    pygame.draw.circle(lienzo_surface, current_color, pos_lienzo, 3)
                    
                    # --- LÓGICA DE DIBUJO SEGÚN HERRAMIENTA ---
                    
                    if current_tool == 'LINEA' and len(points) == 2:
                        dda(lienzo_surface, *points[0], *points[1], current_color)
                        points = [] # Reiniciar puntos
                    
                    elif current_tool == 'CIRCULO' and len(points) == 2:
                        cx, cy = points[0]
                        px, py = points[1]
                        radius = int(((px - cx)**2 + (py - cy)**2) ** 0.5)
                        if radius > 0:
                            bresenham_circle(lienzo_surface, cx, cy, radius, current_color)
                        points = []
                    
                    elif current_tool == 'RECTANGULO' and len(points) == 2:
                        x1, y1 = points[0]
                        x2, y2 = points[1]
                        width = abs(x2 - x1)
                        height = abs(y2 - y1)
                        rect_x = min(x1, x2)
                        rect_y = min(y1, y2)
                        draw_rectangle(lienzo_surface, rect_x, rect_y, width, height, current_color)
                        points = []

                    elif current_tool == 'TRIANGULO' and len(points) == 3:
                        draw_triangle(lienzo_surface, points, current_color)
                        points = []
                        
                    elif current_tool == 'BEZIER' and len(points) == 4:
                        bezier(lienzo_surface, *points, 100, current_color)
                        points = []
                    
                    elif current_tool == 'ELIPSE' and len(points) == 2:
                        cx, cy = points[0]
                        px, py = points[1]
                        rx = abs(px - cx)
                        ry = abs(py - cy)
                        if rx > 0 and ry > 0:
                            draw_ellipse(lienzo_surface, cx, cy, rx, ry, current_color)
                        points = []

                    elif current_tool == 'POLIGONO':
                        # Lógica simple: 5 puntos para un pentágono
                        if len(points) == 5:
                            draw_polygon(lienzo_surface, points, current_color)
                            points = []


        # --- Actualizar botones de COLOR ---
        # ### MODIFICADO ### - Actualiza el estado en lugar de imprimir
      if boton_azul.actualizar(eventos): current_color = COLOR_AZUL
      if boton_verde.actualizar(eventos): current_color = COLOR_VERDE
      if boton_rojo.actualizar(eventos): current_color = COLOR_ROJO
      if boton_morado.actualizar(eventos): current_color = COLOR_MORADO
      if boton_amarillo.actualizar(eventos): current_color = COLOR_AMARILLO
      if boton_blanco.actualizar(eventos): current_color = COLOR_BLANCO
      if boton_negro.actualizar(eventos): current_color = COLOR_NEGRO

      # --- Actualizar botones de FORMA ---
      # ### MODIFICADO ### - Actualiza el estado y resetea los puntos
      if boton_linea.actualizar(eventos): current_tool = 'LINEA'; points = []
      if boton_rect.actualizar(eventos): current_tool = 'RECTANGULO'; points = []
      if boton_circ.actualizar(eventos): current_tool = 'CIRCULO'; points = []
      if boton_tri.actualizar(eventos): current_tool = 'TRIANGULO'; points = []
      if boton_curva.actualizar(eventos): current_tool = 'BEZIER'; points = []
      if boton_elipse.actualizar(eventos): current_tool = 'ELIPSE'; points = []
      if boton_poligono.actualizar(eventos): current_tool = 'POLIGONO'; points = []
        
      # --- Botón LIMPIAR ---
      if boton_limpiar.actualizar(eventos):
            lienzo_surface.fill((237, 237, 237)) # Limpia el lienzo
            points = []

      # Dibujar fondo y botones
      pantalla.fill((237, 237, 237))

      # 2. ### NUEVO ### - Dibujar el LIENZO en la pantalla
      pantalla.blit(lienzo_surface, drawable_rect.topleft)
      # (Opcional) Dibujar un borde alrededor del lienzo
      pygame.draw.rect(pantalla, PANEL_BORDER, drawable_rect, width=2, border_radius=5)

      # 3. Dibujar los PANELES
      pygame.draw.rect(pantalla, PANEL_BG, panel_color_rect, border_radius=12)
      pygame.draw.rect(pantalla, PANEL_BORDER, panel_color_rect, width=3, border_radius=12)

      pygame.draw.rect(pantalla, PANEL_BG, panel_form_rect, border_radius=12)
      pygame.draw.rect(pantalla, PANEL_BORDER, panel_form_rect, width=3, border_radius=12)

      # Dibujar botones encima del panel
      for b in botones_columna:
         b.dibujar(pantalla)
      
      for b in botones_formas:
         b.dibujar(pantalla)


      pygame.display.flip()
      reloj.tick(60)

   pygame.quit()