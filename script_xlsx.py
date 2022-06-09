#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour faire des trous à des endroits particuliers sur une plaque.

Premier jet, ligne de commande.

Created on Wed Oct 13 09:46:37 2021

@author: ejetzer
"""

from datetime import date

import pandas

from matplotlib import pyplot

# Régler l'origine
# On assume que l'origine est au coin supérieur gauche
# î
# .->---------------.
# |                 |
# |                 |
# .-----------------.

fichier = f'programme {date.today()}.iso'

with open(fichier, 'w') as f:
    print('G71', file=f)  # mm
    print('T1', file=f)  # Outil 1
    print('S10000', file=f)  # tr/min
    print('F800', file=f)  # mm/min

# Entrer les points
modèle = """
G0 X{} Y{} Z1.
G1 Z-1.
G4 F1
G1 Z1."""


def conv(x):
    if isinstance(x, str):
        x = x.replace(',', '.')

    return float(x)


fichier_excel = input('fichier: ')
if not fichier_excel:
    fichier_excel = 'eg/trous.xlsx'

df = pandas.read_excel(fichier_excel, sheet_name=0, header=0,
                       usecols=(1, 2), converters={0: conv, 1: conv})
print(df)


with open(fichier, 'a') as f:
    for _, (x, y) in df.iterrows():
        print(modèle.format(x, y), file=f)

df.plot(x=0, y=1, kind='scatter')
pyplot.show()
