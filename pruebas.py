import pygame
import os
#archivo de prueba con la interfaz
# Inicializar pygame
pygame.init()

# Colores para panel y borde
PANEL_BG = (99, 99, 99)
PANEL_BORDER = (0, 0, 0)
PANEL_FBG = (234, 219, 255)

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

   # Crear botones de colores (columna)
   boton_azul = Boton(890, 30, 50, 50, "", (0, 120, 250), (0, 180, 255))
   boton_verde = Boton(890, 100, 50, 50, "", (50, 200, 50), (80, 255, 80))
   boton_rojo = Boton(890, 170, 50, 50, "", (200, 50, 50), (255, 80, 80))
   boton_morado = Boton(890, 240, 50, 50, "", (100, 50, 200), (150, 80, 255))
   boton_amarillo = Boton(890, 310, 50, 50, "", (200, 200, 50), (255, 255, 80))
   boton_blanco = Boton(890, 380, 50, 50, "", (255, 255, 255), (255, 255, 255))
   boton_negro = Boton(890, 450, 50, 50, "", (0, 0, 0), (80, 80, 80))

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


   ejecutando = True
   while ejecutando:
      eventos = pygame.event.get()
      for evento in eventos:
         if evento.type == pygame.QUIT:
            ejecutando = False

      # Actualizar botones
      if boton_azul.actualizar(eventos):
         print("Has hecho clic en AZUL 🎮")

      if boton_rojo.actualizar(eventos):
         print("Has hecho clic en ROJO 🎮")

      if boton_verde.actualizar(eventos):
         print("Has hecho clic en VERDE 🎮")

      if boton_morado.actualizar(eventos):
         print("Has hecho clic en MORADO 🎮")

      if boton_amarillo.actualizar(eventos):
         print("Has hecho clic en AMARILLO 🎮")

      if boton_blanco.actualizar(eventos):
         print("Has hecho clic en BLANCO 🎮")

      if boton_negro.actualizar(eventos):
         print("Has hecho clic en NEGRO 🎮")

      if boton_linea.actualizar(eventos):
         print("Has hecho clic en LINEA 🎮")

      if boton_rect.actualizar(eventos):
         print("Has hecho clic en RECTANGULO 🎮")

      if boton_circ.actualizar(eventos):
         print("Has hecho clic en CIRCULO 🎮")

      if boton_tri.actualizar(eventos):
         print("Has hecho clic en TRIANGULO 🎮")

      # Dibujar fondo y botones
      pantalla.fill((237, 237, 237))

      panel_rect = pygame.Rect(850, 20, 130, 650)
      panel_form = pygame.Rect(20, 20, 140, 650)

      # Fondo del panel y borde (border separate color)
      pygame.draw.rect(pantalla, PANEL_BG, panel_rect, border_radius=12)
      pygame.draw.rect(pantalla, PANEL_BORDER, panel_rect, width=3, border_radius=12)

      pygame.draw.rect(pantalla, PANEL_BG, panel_form, border_radius=12)
      pygame.draw.rect(pantalla, PANEL_BORDER, panel_form, width=3, border_radius=12)

      # Dibujar botones encima del panel
      for b in botones_columna:
         b.dibujar(pantalla)
      
      for b in botones_formas:
         b.dibujar(pantalla)


      pygame.display.flip()
      reloj.tick(60)

   pygame.quit()