"""Algoritmos de rasterización y primitivas geométricas.

Este módulo contiene implementaciones de algoritmos clásicos:
Bresenham para líneas y círculos, DDA, curvas de
Bézier y rutinas para polígonos, rectángulos y elipses. Las funciones
dibujan directamente sobre una surface de Pygame.
"""

import pygame
import math
import numpy as np

# --- Algoritmo Bresenham para líneas ---
def bresenham(screen, x1, y1, x2, y2, color):
    """Dibuja una línea entre (x1, y1) y (x2, y2) usando Bresenham.

    Los puntos se dibujan como círculos de radio 1 sobre la surface
    proporcionada. Esta implementación soporta líneas en cualquier
    octante.

    Args:
        screen: Surface de Pygame donde se dibuja.
        x1, y1: Coordenadas del punto inicial (enteros).
        x2, y2: Coordenadas del punto final (enteros).
        color: Tupla RGB con el color a usar.
    """
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
    """Dibuja una línea entre dos puntos usando el algoritmo DDA.

    Este algoritmo interpola los puntos entre las coordenadas inicial y
    final y dibuja un punto por paso.
    """
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
    """Dibuja un círculo centrado en (cx, cy) de radio r usando Bresenham.

    Los ocho puntos simétricos se calculan y se pintan con radio 1.
    """
    x = 0
    y = r
    d = 3 - 2 * r

    def plot_circle_points(x_offset, y_offset):
        points = [
            (cx + x_offset, cy + y_offset),
            (cx - x_offset, cy + y_offset),
            (cx + x_offset, cy - y_offset),
            (cx - x_offset, cy - y_offset),
            (cx + y_offset, cy + x_offset),
            (cx - y_offset, cy + x_offset),
            (cx + y_offset, cy - x_offset),
            (cx - y_offset, cy - x_offset),
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
    """Dibuja una curva cúbica de Bézier definida por 4 puntos de control.

    Args:
        screen: Surface donde dibujar.
        p0..p3: Tuplas (x, y) con los puntos de control.
        steps: Número de muestras a calcular entre 0 y 1.
        color: Tupla RGB.
    """
    t_values = np.linspace(0, 1, steps)
    points = []
    for t in t_values:
        x = (
            (1 - t) ** 3 * p0[0]
            + 3 * (1 - t) ** 2 * t * p1[0]
            + 3 * (1 - t) * t ** 2 * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            (1 - t) ** 3 * p0[1]
            + 3 * (1 - t) ** 2 * t * p1[1]
            + 3 * (1 - t) * t ** 2 * p2[1]
            + t ** 3 * p3[1]
        )
        points.append((int(x), int(y)))
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 2)
        
#Triangulos y Poligonos
def draw_triangle(screen, vertices, color):
    """Dibuja un triángulo a partir de una lista de 3 vértices.

    Esta función delega en draw_polygon para rasterizar los lados.
    """
    if len(vertices) != 3:
        return
    draw_polygon(screen, vertices, color)
        
def draw_polygon(screen, vertices, color):
    """Dibuja un polígono conectado por los vértices en orden.

    Los lados se rasterizan usando el algoritmo DDA.
    """
    if len(vertices) < 2:
        return
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        dda(screen, x1, y1, x2, y2, color)
        
#Rectangulos
def draw_rectangle(screen, x, y, width, height, color):
    """Dibuja un rectángulo con esquina superior izquierda en (x, y).

    Los cuatro lados se rasterizan con draw_polygon.
    """
    vertices = [
        (x, y), (x + width, y),
        (x + width, y + height), (x, y + height),
    ]
    draw_polygon(screen, vertices, color)

#Elipsis
def draw_ellipse(screen, cx, cy, rx, ry, color):
    """Dibuja una elipse centrada en (cx, cy) con radios rx, ry.

    La elipse se aproxima con una polilínea de 100 muestras.
    """
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