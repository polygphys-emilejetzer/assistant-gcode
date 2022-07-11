#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour faire des trous à des endroits particuliers sur une plaque.

Premier jet, ligne de commande.

Created on Wed Oct 13 09:46:37 2021

@author: ejetzer
"""

from pathlib import Path
from datetime import date

import pandas

import matplotlib
from matplotlib import pyplot

import gcode

# Régler l'origine
# On assume que l'origine est au coin supérieur gauche
# î
# .->---------------.
# |                 |
# |                 |
# .-----------------.

def conv(x):
    if isinstance(x, str):
        x = x.replace(',', '.')

    return float(x)

def extraire_trous(fichier_excel: Path = Path(__file__).parent / 'eg' / 'trous.xlsx'):
    df = pandas.read_excel(fichier_excel, sheet_name=0, header=0,
                           usecols=(1, 2, 3, 4),
                           converters={0: conv, 1: conv, 2: conv, 3: conv})
    xs, ys, zs, dzs = zip(*[(x, y, z, dz) for _, (x, y, z, dz) in df.iterrows()])
    return xs, ys, zs, dzs

def extraire_gcode(xs: list[float], ys: list[float], zs: list[float], dzs: list[float],
                   # Paramètres de programme
                   vitesse_de_rotation: float = 10000,  # tr/min
                   avance: float = 800):  # mm/min
    programme = gcode.initialiser(xs[0], ys[0], zs[0], vitesse_de_rotation, avance)

    for x, y, z, dz in zip(xs, ys, zs, dzs):
        programme += gcode.perçage(x, y, z, dz)

    programme += gcode.fin()

    return str(programme)

def extraire_graphique(xs: list[float], ys: list[float]):
    pyplot.plot(xs, ys, 'o')

def main():    
    fichier_excel = input('fichier: ')
    if not fichier_excel:
        fichier_excel = Path(__file__).parent / 'eg' / 'trous.xlsx'

    xs, ys, zs, dzs = extraire_trous(fichier_excel)
    programme = extraire_gcode(xs, ys, zs, dzs)

    matplotlib.style.use('seaborn')
    pyplot.gca().set_aspect('equal')
    
    extraire_graphique(xs, ys)

    with open(Path(__file__).parent / 'eg' / 'trous {date.today()}.iso', 'w') as f:
        print(programme, file=f)

    pyplot.savefig(Path(__file__).parent / 'eg' / 'trous {date.today()}.svg')
    pyplot.show()

if __name__ == '__main__':
    main()

