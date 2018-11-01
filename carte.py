# -*-coding:Utf-8 -*

# Ce module contient la classe Carte
# Une carte est composée d'un nom et d'un tableau (matrice représentant la carte)
# La classe contient également plusieurs méthodes pour agir sur l'objet Carte

import os
from gestion import saisieLigneOK,formatLigneOK,choixValide,nbCoupsJoue,sensJoue,supprimerFichierCarte

CASE_MUR="O"
CASE_PORTE_OUVERTE="."
CASE_PORTE_FERMEE="-"
CASE_SORTIE="U"
CASE_VIDE=" "

class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, tableau):
        self.nom = nom
        self.labyrinthe = tableau

    def chargerCarte(self,nomcomplet) :
        chemin = os.path.join("cartes", self.nom)

    def chaineEnCarte(self,chaine) :
        return(chaine.split("\n"))

    def supprimerCarte(self):
        chemin = os.path.join("cartes", self.nom)
        chemin=chemin + ".txt"
        supprimerFichierCarte(chemin)
        print("La carte " + self.nom + " a été supprimée")

    def afficherCarte(self):
        for elt in self.labyrinthe :
            print(elt)

    def editerCarte(self) :
        laNouvelleCarte=Carte(self.nom,self.labyrinthe)
        finEdition=False
        while finEdition==False :
            # On commence par afficher la carte
            i=1
            for elt in laNouvelleCarte.labyrinthe :
                print("Ligne " + str(i) + " : " + elt)
                i=i+1
            choix=input("Quelle ligne souhaitez vous modifier ? (0 pour fin) ")
            try :
                int(choix)
                if choix=="0" :
                    finEdition=True
                else :
                    if int(choix)>0 and int(choix)<=len(laNouvelleCarte.labyrinthe) :
                        print(laNouvelleCarte.labyrinthe[int(choix)-1])
                        finSaisieLigne=False
                        while finSaisieLigne==False :
                            nouvelleLigne=input("Saisie de la nouvelle ligne (" + str(len(laNouvelleCarte.labyrinthe[int(choix)-1])) + " caractère(s)) :")
                            if saisieLigneOK(len(laNouvelleCarte.labyrinthe[int(choix)-1]),nouvelleLigne) :
                                # On enlève le dernier retour à la ligne inutile
                                laNouvelleCarte.labyrinthe[int(choix)-1]=nouvelleLigne
                                finSaisieLigne=True
                    else :
                        print("La ligne n'existe pas")
            except ValueError:
                print("Vous devez saisir une valeur numérique")

        # Deversement de la nouvelle carte dans l'objet associé


        if laNouvelleCarte.carteValide() :
            print("Carte Valide")
            self.labyrinthe=laNouvelleCarte.labyrinthe
            self.enregistrerNouvelleCarte()
        else :
            print("Erreur dans le format (il faut au moins un U)")
        return True

    def carteValide(self) :
        # Une carte doit obligatoirement contenir au moins un U
        nbU=0
        for elt in self.labyrinthe :
            for i in range(0,int(len(elt))) :
                if elt[i]==CASE_SORTIE :
                    nbU=nbU+1
        if nbU>=1 :
            return True
        return False

    def enregistrerNouvelleCarte(self):
        chemin = os.path.join("cartes", self.nom)
        chemin=chemin + ".txt"
        nouveauFichier=open(chemin, "w")
        map=""
        for elt in self.labyrinthe :
            map=map+elt+"\n"
        # On enlève le dernier retour à la ligne inutile
        map=map[0:int(len(map))-1]
        nouveauFichier.write(map)
        nouveauFichier.close()

