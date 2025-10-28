# -*- coding: utf-8 -*-
"""
Graficador sencillo con Pygame + POO
------------------------------------
- Integra el código base del usuario (línea/rectángulo/círculo) con una barra lateral de botones.
- Permite elegir herramienta: Línea, Rectángulo, Círculo.
- Incluye: Limpiar, mostrar/ocultar Ejes y Cuadrícula.

Requisitos:
    pip install pygame
"""

import pygame

pygame.init()

# -----------------------------
# Configuración general
# -----------------------------
ANCHO, ALTO = 1000, 680
ANCHO_PANEL = 230
FPS = 60

COLOR_BG = (28, 28, 32)
COLOR_PANEL = (20, 20, 24)
COLOR_TEXTO = (240, 240, 240)
COLOR_BORDE = (70, 70, 80)

COLOR_CANVAS = (255, 255, 255)
COLOR_GRID = (230, 230, 235)
COLOR_AXES = (120, 120, 120)


# -----------------------------
# Clase Boton (POO) - UI only
# -----------------------------
class Boton:
    def __init__(self, x, y, w, h, texto,
                 color=(60, 62, 68), color_hover=(80, 82, 90),
                 color_texto=(240, 240, 240), fuente=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 28)
        self.hover = False
        self.activo = False  # Para indicar selección visual

    def draw(self, surface):
        col = self.color_hover if (self.hover or self.activo) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BORDE, self.rect, width=1, border_radius=10)
        text_surf = self.fuente.render(self.texto, True, self.color_texto)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle(self, events):
        """Actualiza estado visual (hover). No ejecuta acciones: interfaz sin funcionalidad."""
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)


# -----------------------------
# Utilidades de dibujo (estéticas): grid y ejes estáticos
# -----------------------------
def draw_grid(surface, spacing=20, color=COLOR_GRID):
    w, h = surface.get_size()
    for x in range(0, w, spacing):
        pygame.draw.line(surface, color, (x, 0), (x, h), 1)
    for y in range(0, h, spacing):
        pygame.draw.line(surface, color, (0, y), (w, y), 1)


def draw_axes(surface, color=COLOR_AXES, width=1):
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    pygame.draw.line(surface, color, (0, cy), (w, cy), width)  # eje X
    pygame.draw.line(surface, color, (cx, 0), (cx, h), width)  # eje Y


# -----------------------------
# App Graficador (solo interfaz)
# -----------------------------
class GraficadorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Graficador - Interfaz (sin funcionalidad)")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Superficie de dibujo (canvas) estático
        self.canvas = pygame.Surface((ANCHO - ANCHO_PANEL - 20, ALTO - 40))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.topleft = (ANCHO_PANEL + 10, 20)

        # Estado de UI (no interactivo)
        self.herramienta = "Linea"   # solo etiqueta visual
        self.mostrando_grid = True
        self.mostrando_ejes = True

        # Inicializar canvas (estático)
        self.limpiar_canvas()

        # Botones (solo visual)
        self.botones = []
        self._crear_botones()

    def limpiar_canvas(self):
        """Rellena el canvas con apariencia (grid/ejes) sin mantener figuras."""
        self.canvas.fill(COLOR_CANVAS)
        if self.mostrando_grid:
            draw_grid(self.canvas, spacing=20)
        if self.mostrando_ejes:
            draw_axes(self.canvas)

    def _crear_botones(self):
        x, y = 15, 20
        w, h = ANCHO_PANEL - 30, 44
        sep = 10

        b_linea = Boton(x, y, w, h, "Linea")
        b_linea.activo = True
        b_rect = Boton(x, y + (h + sep), w, h, "Rectangulo")
        b_circ = Boton(x, y + 2 * (h + sep), w, h, "Circulo")

        y2 = y + 3 * (h + sep) + 10
        b_deshacer = Boton(x, y2, w, h, "Deshacer")
        b_limpiar = Boton(x, y2 + (h + sep), w, h, "Limpiar")

        y3 = y2 + 2 * (h + sep) + 10
        b_grid = Boton(x, y3, w, h, "Cuadrícula")
        b_axes = Boton(x, y3 + (h + sep), w, h, "Ejes")

        self.botones.extend([b_linea, b_rect, b_circ, b_deshacer, b_limpiar, b_grid, b_axes])

    def manejador_eventos(self):
        """Procesa solo cierre de ventana y actualiza hover de botones (sin acciones)."""
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                return False

        # Solo actualizar estado visual de botones (hover)
        for b in self.botones:
            b.handle(eventos)

        return True

    def run(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejador_eventos()

            # Fondo y panel
            self.screen.fill(COLOR_BG)
            panel_rect = pygame.Rect(0, 0, ANCHO_PANEL, ALTO)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)

            # Título panel
            titulo = self.font_title.render("Herramientas", True, COLOR_TEXTO)
            self.screen.blit(titulo, (15, 0))

            # Botones (solo visual)
            for b in self.botones:
                b.draw(self.screen)

            # Canvas estático
            self.screen.blit(self.canvas, self.canvas_rect)

            # Etiqueta de estado (visual)
            txt_tool = self.font_small.render(f"Herramienta: {self.herramienta}", True, (200, 200, 210))
            self.screen.blit(txt_tool, (ANCHO_PANEL + 14, ALTO - 24))

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    app = GraficadorApp()
    app.run()
