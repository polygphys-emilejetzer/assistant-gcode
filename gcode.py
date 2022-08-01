# -*- coding: utf-8 -*-

class GProgramme(list):

    def __str__(self):
        return '\n'.join(self)


def initialiser(x_0: float = 0,
                y_0: float = 0,
                z_0: float = 0,
                vitesse_de_rotation: float = 10000,
                avance: float = 800):
    programme = GProgramme()
    programme.append('G71')  # Unités métriques (mmm)
    programme.append('T1')  # Outils 1 (seul outil permis sur une CHarly Robot)
    programme.append(f'S{vitesse_de_rotation}')  # tr/min
    programme.append(f'F{avance}')  # mm/min
    programme.append(f'G90')  # Coordonnées absolues

    programme.append(f'G0 X{x_0:.4f} Y{y_0:.4f} Z{z_0:.4f}')

    return programme


def déplacer(xs: list[float],
             ys: list[float],
             zs: list[float]):
    programme = [f'G0 X{x:.4f} Y{y:.4f} Z{z:.4f}' for x,
                 y, z in zip(xs, ys, zs)]
    return GProgramme(programme)


def perçage(x: float, y: float, z: float, dz: float):
    programme = GProgramme()
    programme.append(f'G0 X{x:.4f} Y{y:.4f} Z{z:.4f}')
    programme.append(f'G0 X{x:.4f} Y{y:.4f} Z{z-dz:.4f}')
    programme.append(f'G0 X{x:.4f} Y{y:.4f} Z{z:.4f}')

    return programme


def fraisage(xs: list[float], ys: list[float], zs: list[float]):
    return déplacer(xs[:1], ys[:1], [zs[0]+1]) +\
        déplacer(xs, ys, zs) +\
        déplacer(xs[-1:], ys[-1:], [zs[-1]+1])


def fin():
    return GProgramme(['M5',  # Arrêt de la broche
                       'M2'])  # Fin de programme
