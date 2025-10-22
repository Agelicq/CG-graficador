import pygame 
import math
"""
PROBAR DDA Y BRESENHAM 
import pygame

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prueba algoritmo Bresenham")
clock = pygame.time.Clock()

# --- Algoritmo Bresenham para líneas ---
def bresenham(screen, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            pygame.draw.circle(screen, color, (x, y), 1)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            pygame.draw.circle(screen, color, (x, y), 1)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    pygame.draw.circle(screen, color, (x, y), 1)

----------------------------------------------------------------
BESENHAM CIRCULO
# --- Modo prueba: dibujar líneas con clics ---
running = True
start = None
screen.fill(WHITE)
while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start is None:
                start = event.pos  # primer clic
            else:
                end = event.pos    # segundo clic
                bresenham(screen, *start, *end, BLUE)
                start = None       # reiniciar

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

PROBAR BRESENHAM CIRCULOS
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prueba algoritmo DDA")
clock = pygame.time.Clock()


# --- Modo prueba: dibujar líneas ---
running = True
center = None
radius = 0
screen.fill(WHITE)
while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            center = event.pos  # clic define el centro
        elif event.type == pygame.MOUSEBUTTONUP:
            if center:
                # calcula el radio según la distancia al punto donde soltaste
                mx, my = event.pos
                cx, cy = center
                radius = int(((mx - cx)**2 + (my - cy)**2) ** 0.5)
                bresenham_circle(screen, cx, cy, radius, BLACK)
                center = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


def bezier(screen, p0, p1, p2, p3, steps, color):
    t_values = np.linspace(0, 1, steps)
    for i in t_values:
        t = i
        x = (1-t)**3 * p0[0] + 3 * (1-t)**2 * t * p1[0] + 3 * (1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3 * (1-t)**2 * t * p1[1] + 3 * (1-t) * t**2 * p2[1] + t**3 * p3[1]
        pygame.draw.circle(screen, color, (int(x), int(y)), 1)
"""

def dda(screen, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        pygame.draw.circle(screen, color, (round(x), round(y)), 1)
        x += x_inc
        y += y_inc

def bresenham(screen, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1
    sx = 1 if  x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            pygame.draw.circle(screen, color, (x,y), 1)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            pygame.draw.circle(screen, color, (x,y), 1)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    pygame.draw.circle(screen, color, (x,y), 1)


def bresenham_circle(screen, cx, cy, r, color):
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


def bezier(screen, p0, p1, p2, p3, steps, color):
    t_values = np.linspace(0, 1, steps)
    points = []
    for t in t_values:
        x = (1-t)**3 * p0[0] + 3 * (1-t)**2 * t * p1[0] + 3 * (1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3 * (1-t)**2 * t * p1[1] + 3 * (1-t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((int(x), int(y)))

    # Dibuja la curva conectando los puntos
    for i in range(1, len(points)):
        pygame.draw.line(screen, color, points[i-1], points[i], 2)
#--------------------------------------------------------------------------
#Faltantes
#Triangulos y Poligonos
def draw_triangle(screen, vertices, color):
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        dda(screen, x1, y1, x2, y2, color)
        
def draw_polygon(screen, vertices, color):
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        dda(screen, x1, y1, x2, y2, color)

#--------------------------------------------------------------------------
#Rectangulos
def draw_rectangle(screen, x, y, width, height, color):
    vertices = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]
    draw_polygon(screen, vertices, color)  # Dibujar el rectangulo como un poligono

#---------------------------------------------------------------------------
#Elipsis
def draw_ellipse(screen, cx, cy, rx, ry, color):
    t_values = np.linspace(0, 2 * math.pi, 100)
    for t in t_values:
        x = cx + rx * math.cos(t)
        y = cy + ry * math.sin(t)
        pygame.draw.circle(screen, color, (int(x), int(y)), 1)  
      
import pygame
import numpy as np

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, BLUE, RED, GRAY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prueba Curvas Bézier")
clock = pygame.time.Clock()

# --- Función Bézier cúbica ---


# --- Prueba interactiva ---
running = True
points = []  # almacenará los 4 puntos de control
screen.fill(WHITE)
while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(points) < 4:
                points.append(event.pos)

    # Dibuja los puntos de control
    for p in points:
        pygame.draw.circle(screen, RED, p, 5)

    # Dibuja líneas guía entre puntos de control
    if len(points) >= 2:
        pygame.draw.lines(screen, GRAY, False, points, 1)

    # Dibuja la curva cuando ya hay 4 puntos
    if len(points) == 4:
        bezier(screen, points[0], points[1], points[2], points[3], 200, BLUE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
