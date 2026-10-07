"""vector.py — animation d'un champ de vecteurs complexes z → z⁴ + 1.

Pose une grille 40×40 de points dans le plan complexe, puis anime leur
transport par le champ polynomiale ``f(z) = z⁴ + 1`` via une intégration
Runge–Kutta d'ordre 4 (`lib.rk4_step`). Chaque point conserve sa couleur
(définie par sa position de départ) : on voit le champ déformer le réseau.

Sortie : fenêtre matplotlib interactive (animation en temps réel).

Dépendances : numpy, matplotlib, **lib** (fournit `rk4_step`)

Usage :
    python vector.py      # puis fermer la fenêtre pour terminer
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from lib import rk4_step


def f(z):
    """Champ de vecteurs intégré : ż = z⁴ + 1 (scalaire ou tableau numpy)."""
    return z ** 4 + 1


def main():
    n = 40
    x = np.linspace(-1.5, 1.5, n, dtype=np.float64)
    y = np.linspace(-1.5, 1.5, n, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    z = (X + 1j * Y).ravel()

    # Couleur figée sur la position initiale (rouge → droite, bleu → haut)
    color_min, color_max = -1.5, 1.5
    norm_x = (z.real - color_min) / (color_max - color_min)
    norm_y = (z.imag - color_min) / (color_max - color_min)
    colors = np.column_stack((norm_x, norm_y, 1 - norm_x))

    fig, ax = plt.subplots(figsize=(8, 8))
    scat = ax.scatter(z.real, z.imag, c=colors, s=60)
    ax.set_aspect("equal")
    ax.grid(True)

    dt = 0.01

    def update(_frame):
        nonlocal z
        z = rk4_step(z, dt, f)          # un pas RK4 sur tout le réseau
        scat.set_offsets(np.column_stack((z.real, z.imag)))
        return scat,

    # interval=1 ms : l'animation tourne le plus vite possible
    anim = FuncAnimation(fig, update, interval=1, blit=False)
    plt.show()


if __name__ == "__main__":
    main()
