"""Interfaz gráfica del graficador.

Este módulo proporciona una interfaz basada en Pygame que muestra
paneles de herramientas y colores, botones con iconos opcionales y un
área de dibujo (lienzo). Las rutinas de rasterización y primitivas se
encuentran en el módulo `figuras` y son invocadas desde la lógica de
herramientas cuando el usuario completa la selección de puntos.

El archivo está organizado como un script ejecutable. Ejecutar el
archivo abrirá una ventana Pygame con los controles y un lienzo.
"""

import pygame
import os
import math
import numpy as np
import figuras as f  # Importar los algoritmos desde figuras.py

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
COLOR_AMARILLO = (255, 243, 77)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
# Clase Boton
class Boton:
    """Representa un botón rectangular con texto o icono centrado.

    El botón detecta el estado hover y puede devolver True cuando se
    hace clic en él mediante el método `actualizar`.
    """

    def __init__(
        self,
        x,
        y,
        ancho,
        alto,
        texto,
        color_normal,
        color_hover,
        color_texto=(0, 0, 0),
        fuente=None,
        icon_surface=None,
    ):
        """Inicializa un nuevo botón.

        Args:
            x, y: Coordenadas de la esquina superior izquierda.
            ancho, alto: Dimensiones del botón.
            texto: Texto a mostrar (si no hay icono).
            color_normal: Color de fondo en reposo.
            color_hover: Color de fondo cuando el cursor está encima.
            color_texto: Color del texto.
            fuente: Objeto pygame.font.Font opcional.
            icon_surface: Surface opcional que se dibuja centrada.
        """
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
    pygame.display.set_caption("Graficador")
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
    lienzo_surface.fill(COLOR_BLANCO)
        
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
    curva_pol = os.path.join(os.path.dirname(__file__), 'poligono.png')
    if os.path.exists(curva_pol):
        try:
            img = pygame.image.load(curva_pol).convert_alpha()
            pad = 8
            inner_w = max(1, boton_poligono.rect.width - pad*2)
            inner_h = max(1, boton_poligono.rect.height - pad*2)
            iw, ih = img.get_size()
            scale = min(inner_w / iw, inner_h / ih)
            new_w = max(1, int(iw * scale))
            new_h = max(1, int(ih * scale))
            img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
            icon_surface = pygame.Surface((inner_w, inner_h), pygame.SRCALPHA)
            ox = (inner_w - new_w) // 2
            oy = (inner_h - new_h) // 2
            icon_surface.blit(img_scaled, (ox, oy))
            boton_poligono.icon_surface = icon_surface
        except Exception as e:
                print("Error cargando", curva_pol, e)

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
                        # Nota: no dibujamos el punto directamente en el lienzo para evitar que quede permanente.
                        
                        # --- LÓGICA DE DIBUJO SEGÚN HERRAMIENTA ---
                        
                        if current_tool == 'LINEA' and len(points) == 2:
                            f.dda(lienzo_surface, *points[0], *points[1], current_color)
                            points = [] # Reiniciar puntos
                        
                        elif current_tool == 'CIRCULO' and len(points) == 2:
                            cx, cy = points[0]
                            px, py = points[1]
                            radius = int(((px - cx)**2 + (py - cy)**2) ** 0.5)
                            if radius > 0:
                                f.bresenham_circle(lienzo_surface, cx, cy, radius, current_color)
                            points = []
                        
                        elif current_tool == 'RECTANGULO' and len(points) == 2:
                            x1, y1 = points[0]
                            x2, y2 = points[1]
                            width = abs(x2 - x1)
                            height = abs(y2 - y1)
                            rect_x = min(x1, x2)
                            rect_y = min(y1, y2)
                            f.draw_rectangle(lienzo_surface, rect_x, rect_y, width, height, current_color)
                            points = []

                        elif current_tool == 'TRIANGULO' and len(points) == 3:
                            f.draw_triangle(lienzo_surface, points, current_color)
                            points = []
                            
                        elif current_tool == 'BEZIER' and len(points) == 4:
                            f.bezier(lienzo_surface, *points, 100, current_color)
                            points = []
                        
                        elif current_tool == 'ELIPSE' and len(points) == 2:
                            cx, cy = points[0]
                            px, py = points[1]
                            rx = abs(px - cx)
                            ry = abs(py - cy)
                            if rx > 0 and ry > 0:
                                f.draw_ellipse(lienzo_surface, cx, cy, rx, ry, current_color)
                            points = []

                        elif current_tool == 'POLIGONO':
                            # Lógica simple: 5 puntos para un pentágono
                            if len(points) == 5:
                                f.draw_polygon(lienzo_surface, points, current_color)
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
                lienzo_surface.fill(COLOR_BLANCO) # Limpia el lienzo
                points = []

        # Dibujar fondo y botones
        pantalla.fill((237, 237, 237))

        # 2. Dibujar el LIENZO en la pantalla
        pantalla.blit(lienzo_surface, drawable_rect.topleft)
        # Dibujar un borde alrededor del lienzo
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

        # Dibujar marcadores temporales (puntos) sobre el lienzo — no se pintan en el lienzo_surface
        if points:
            for p in points:
                screen_pos = (drawable_rect.x + p[0], drawable_rect.y + p[1])
                pygame.draw.circle(pantalla, current_color, screen_pos, 3)


        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()