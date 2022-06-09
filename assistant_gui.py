#!python3.9
# -*- coding: utf-8 -*-
"""
Script pour faire des trous à des endroits particuliers sur une plaque.

Premier jet, ligne de commande.

Created on Wed Oct 13 09:46:37 2021

@author: ejetzer
"""

from pathlib import Path
from tkinter import Tk, Frame, filedialog, Button

import pandas

from matplotlib import pyplot


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
                                                              ('Excel ancien', '*.xls')))
        self.fichier_table = Path(fichier_table)
        self.fichier_programme = self.fichier_table.with_suffix('.iso')

        self.bouton.config(fg='red', text='Ouverture de fichier...')
        self.df = pandas.read_excel(self.fichier_table,
                                    sheet_name=0,
                                    header=0,
                                    usecols=(1, 2),
                                    converters={0: conv,
                                                1: conv})

        self.bouton.config(fg='red', text='Écriture de fichier...')
        with self.fichier_programme.open('w') as f:
            print('G71', file=f)  # mm
            print('T1', file=f)  # Outil 1
            print('S10000', file=f)  # tr/min
            print('F800', file=f)  # mm/min

            modèle = """G0 X{} Y{} Z1.
G1 Z-1.
G4 F1
G1 Z1."""

            for _, (x, y) in self.df.iterrows():
                print(modèle.format(x, y), file=f)

        self.bouton.config(fg='red', text='Dessin...')

        self.df.plot(x=0, y=1, kind='scatter')
        pyplot.savefig(self.fichier_programme.with_suffix('.png'))
        pyplot.show()

        self.bouton.config(fg='green', text='Lancer')

    def pack(self, *args, **kargs):
        self.bouton = Button(self, text='Lancer', fg='green',
                             command=lambda: self.ouvrir())
        self.bouton.pack()

        super().pack(*args, **kargs)


if __name__ == '__main__':
    racine = Tk()
    racine.geometry('400x100')
    racine.title('Assistant de pré-perçage')
    assistant = Assistant(racine)
    assistant.pack()
    racine.mainloop()
