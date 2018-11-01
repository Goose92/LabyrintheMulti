# -*-coding:Utf-8 -*


class Joueur:

    """Classe représentant un joueur"""

    def __init__(self, nom,ID,connection) :
        self.nom = nom
        self.ID = ID
        self.connection=connection
        self.pointDeVie=100
        self.robot=[0,0]
        self.nbCoups=0
        self.gagne=False

    def SUPPRretournerID(self) :
        return self.ID

    def SUPPRmettreAJoueurNom(self,ID,nom) :
        self.nom=nom
