#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Script pour faire des trous à des endroits particuliers sur une plaque.

Premier jet, ligne de commande.

Created on Wed Oct 13 09:46:37 2021

@author: ejetzer
"""

from datetime import date
from pathlib import Path
from tkinter import Tk, Frame, filedialog, Button

import pandas

import matplotlib
from matplotlib import pyplot

import script_xlsx, script_svg


def conv(x):
    if isinstance(x, str):
        x = x.replace(',', '.')

    return float(x)


class Assistant(Frame):

    def ouvrir(self):
        self.bouton.config(fg='red', text='Sélection de fichier...')
        fichier_table = filedialog.askopenfilename(initialdir='.',
                                                   title='Sélectionnez le fichier *.xlsx contenant les positions des points.',
                                                   filetypes=(('Excel récent', '*.xlsx'),
                                                              ('Excel ancien', '*.xls'),
                                                              ('Dessin SVG', '*.svg')))
        self.fichier_source = Path(fichier_table)
        self.fichier_programme = self.fichier_source.with_suffix(f'.{date.today()}.iso')
        self.fichier_graphique = self.fichier_source.with_suffix(f'.{date.today()}.svg')

        self.bouton.config(fg='red', text='Ouverture de fichier...')

        if self.fichier_source.suffix in ('.xlsx', '.xls'):
            source = script_xlsx.extraire_trous(self.fichier_source)
            programme = script_xlsx.extraire_gcode(*source)
        elif self.fichier_source.suffix == '.svg':
            source = script_svg.extraire_chemins(self.fichier_source)
            programme = script_svg.extraire_gcode(source)

        self.bouton.config(fg='red', text='Écriture de fichier...')
        with self.fichier_programme.open('w') as f:
            print(programme, file=f)

        self.bouton.config(fg='red', text='Dessin...')

        matplotlib.style.use('seaborn')
        pyplot.gca().set_aspect('equal')
        
        if self.fichier_source.suffix in ('.xlsx', '.xls'):
            script_xlsx.extraire_graphique(*source[:2])
        elif self.fichier_source.suffix == '.svg':
            script_svg.extraire_graphique(source)
            
        pyplot.savefig(self.fichier_graphique)
        pyplot.show()

        self.bouton.config(fg='green', text='Lancer')

    def pack(self, *args, **kargs):
        self.bouton = Button(self, text='Lancer', fg='green',
                             command=self.ouvrir)
        self.bouton.pack()

        super().pack(*args, **kargs)


if __name__ == '__main__':
    racine = Tk()
    racine.geometry('400x100')
    racine.title('Assistant de pré-perçage')
    assistant = Assistant(racine)
    assistant.pack()
    racine.mainloop()
