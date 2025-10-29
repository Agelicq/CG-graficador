import pygame 
import math
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