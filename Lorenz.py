"""Lorenz.py — vidéo 3D de l'attracteur de Lorenz.

Simule un réseau de 50³ = 125 000 points issus d'une grille 3D, chacun
intégré selon les équations de Lorenz, puis écrit directement une vidéo MP4
(un seul objet ``Figure`` réutilisé d'une image à l'autre, aucune image
intermédiaire sur le disque).

Équations (σ, ρ, β) :
    dx/dt = σ (y − x)
    dy/dt = x (ρ − z) − y
    dz/dt = x y − β z

Sortie : `Lorenz_video.mp4` (1200×1200, 400 images à 60 fps).

Dépendances : numpy, matplotlib, opencv-python, tqdm, **lib**
    (fournit `integrate_lorenz` et `figure_to_bgr`)

Usage :
    python Lorenz.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import cv2
from tqdm import tqdm

from lib import figure_to_bgr, integrate_lorenz

# ==========================
# PARAMÈTRES
# ==========================
# Constantes de Lorentz classiques : le régime chaotique (papillon).
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

dt = 0.01          # pas d'intégration
n = 50             # points par axe -> n**3 points au total
steps_per_frame = 1
frames = 400       # nombre d'images de la vidéo
fps = 60

# Figure 8x8 pouces à 150 dpi → frames de 1200x1200
FIGSIZE, DPI = (8, 8), 150
VIDEO_SIZE = (int(FIGSIZE[0] * DPI), int(FIGSIZE[1] * DPI))
output_video = "Lorenz_video.mp4"


def main():
    # ==========================
    # CONDITIONS INITIALES
    # ==========================
    # Grille cubique [-10, 10]³ : chaque point part d'une position différente,
    # ce qui rend visible la divergence des trajectoires (sensibilité aux
    # conditions initiales).
    grid = np.linspace(-10, 10, n, dtype=np.float32)
    X, Y, Z = np.meshgrid(grid, grid, grid, indexing="ij")
    points = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()]).astype(np.float32)

    # Couleurs figées sur la position de départ
    mins = points.min(axis=0)
    ranges = np.ptp(points, axis=0)
    ranges[ranges == 0] = 1.0
    colors = np.clip((points - mins) / ranges, 0.0, 1.0)

    # ==========================
    # FIGURE UNIQUE (CRUCIAL)
    # ==========================
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_axis_off()
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_zlim(0, 50)

    scat = ax.scatter(
        points[:, 0],
        points[:, 1],
        points[:, 2],
        c=colors,
        s=5,
        alpha=0.9,
        linewidths=0
    )

    # ==========================
    # VIDÉO ÉCRITE DIRECTEMENT
    # (plus de PNG intermédiaires à écrire puis à relire)
    # ==========================
    cv2.setNumThreads(0)
    cv2.useOptimized()
    writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        VIDEO_SIZE,
        isColor=True
    )
    if not writer.isOpened():
        raise RuntimeError("Impossible d'ouvrir le flux vidéo (codec mp4v)")

    # FRAME 0 : ÉTAT INITIAL
    writer.write(figure_to_bgr(fig))

    # ==========================
    # BOUCLE PRINCIPALE
    # ==========================
    for _ in tqdm(range(1, frames), desc="Simulation"):
        integrate_lorenz(points, steps_per_frame, dt, sigma, rho, beta)
        scat._offsets3d = (points[:, 0], points[:, 1], points[:, 2])
        writer.write(figure_to_bgr(fig))

    writer.release()
    plt.close(fig)
    print(f"✓ Vidéo créée : {output_video}")


if __name__ == "__main__":
    main()
