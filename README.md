# Attracteurs & champs de vecteurs

Deux visualisations dynamiques en Python : l'attracteur de Lorenz (3D,
vidéo) et le transport d'un réseau de points par un champ polynomial
complex (animation interactive).

> **Dépendance commune : ce projet nécessite le dépôt [`lib`](../lib).**
> Voir [Installation](#installation).

## Scripts

| Script | Description | Sortie |
|---|---|---|
| `Lorenz.py` | 125 000 points intégrés selon les équations de Lorenz, écrits directement en MP4 | `Lorenz_video.mp4` (1200×1200, 400 img, 60 fps) |
| `vector.py` | Animation du champ `ż = z⁴ + 1` sur une grille 40×40 du plan complexe, intégré en RK4 | fenêtre matplotlib interactive |

### `Lorenz.py`

Les équations de Lorenz (régime chaotique, « papillon ») :

```
dx/dt = σ (y − x)
dy/dt = x (ρ − z) − y
dz/dt = x y − β z
```

avec les valeurs classiques `σ = 10`, `ρ = 28`, `β = 8/3`.

Points clés de l'implémentation :

- la grille initiale `[-10, 10]³` est intégrée **en une seule fois** par
  `lib.integrate_lorenz` (Numba, parallèle) ;
- la couleur de chaque point est figée sur sa position de départ : on voit
  la divergence des trajectoires ;
- une **seule** `Figure` matplotlib est réutilisée pour toutes les images,
  écrites en direct dans le `VideoWriter` OpenCV — aucun PNG intermédiaire.

Réglages en tête de fichier : `n` (points par axe), `frames`, `fps`, `dt`.

### `vector.py`

Pose 1 600 points dans le plan complexe, puis anime leur déplacement par
`lib.rk4_step` (Runge–Kutta d'ordre 4). Chaque point garde la couleur de sa
position initiale, ce qui rend visible la déformation du champ.

## Installation

```bash
git clone https://github.com/<ton_compte>/lib.git
cd lib && pip install numpy numba
```

Puis, à côté du dépôt courant :

```bash
ln -s ../lib/lib.py .
```

Dépendances du projet lui-même :

```bash
pip install numpy matplotlib opencv-python tqdm
```

## Utilisation

```bash
python Lorenz.py      # génère Lorenz_video.mp4 (quelques dizaines de secondes)
python vector.py      # fenêtre d'animation, fermer pour quitter
```

Premier lancement : Numba compile les fonctions JIT, ajoute quelques
secondes. Les suivants sont rapides (cache).

## Licence

Projet personnel — Paul Fournier.
