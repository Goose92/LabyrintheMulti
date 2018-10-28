# -*-coding:Utf-8 -*

# Ce module contient la classe Partie
# Une carte est composée d'une grille (carte), différentes valeurs, la position du robot
# La classe contient également plusieurs méthodes pour agir sur l'objet Partie

import os,socket,select,time
from random import randint

class Partie:

    """Classe représentant un partie"""

    def __init__(self, carte):
        self.grille = carte.split("\n")
        self.joueur=[]
        self.lesJoueurs=dict() # un dictionnaire avec nom, puis connection, puis tour (si true c'est à son tour)
        self.nbCoups=0
        self.tailleGrille=[0,0]
        self.robot=[0,0]
        self.gagne=False
        self.pointDeVie=100
        self.listeJoueurs=[]

    def nomJoueur(self,num) :
        indice=0
        for elt in self.lesJoueurs :
            if indice==num :
                return self.lesJoueurs[elt][0]
            indice=indice+1
        return "bizarre"

    def afficherCartePartie(self) :
        for elt in self.grille :
            print(elt)

    def ajouterUnJoueur(self,ID,nom,connection) :
        leJoueur=[nom,connection,False,[0,0]]
        self.lesJoueurs[int(ID)]=leJoueur

    def supprimerUnJoueur(self,ID) :
        del self.lesJoueurs[ID]

    def afficherListeJoueurs(self) :
        print("Liste des joueurs connectés : ")
        if len(self.lesJoueurs) == 0 :
            print("Il n'y pas pas de joueur connecté")
        else :
            for elt in self.lesJoueurs :
                print("     " + str(self.lesJoueurs[elt][0]))

    def initialiserToursjoueurs(self) :
        self.listeJoueurs=[]
        for elt in self.lesJoueurs :
            nouvelleLigne=[self.lesJoueurs[elt][0],self.lesJoueurs[elt][2]]
            self.listeJoueurs.append(nouvelleLigne)

    def donnerLaMain(self,joueurProchain,connection) :
        for elt in self.listeJoueurs :
            elt[1]=False
        self.listeJoueurs[joueurProchain][1]=True
        #print("On donne la main à " + str(self.listeJoueurs[joueurProchain][0]))
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        num=0
        for client in connection:
            if num==int(joueurProchain) :
                client.send(b"[ACTIF]")
                #print("envoi ACTIF")
            else :
                client.send(b"[PASSIF]")
                #print("envoi PASSIF")
            num=num+1

    def toutLeMondePassif(self,connection) :
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        for client in connection:
            client.send(b"[PASSIF]")

    def messageAuxPassifs(self,joueurActif,connection,messageAEnvoyer) :
         clients_a_lire = []
         try:
             clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
         except select.error:
             pass
         num=0
         for client in connection:
             if num!=int(joueurActif) :
                client.send(messageAEnvoyer.encode())
             num=num+1

    def afficherCarteATous(self,connection,nbCoups) :
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        laCarte=""
        for elt in self.grille :
            laCarte=laCarte + elt + "\n"
        # On enlève le dernier retour à la ligne inutile
        laCarte=laCarte[0:int(len(laCarte))-1]
        for client in connection:
            #chaineAEnvoyer="Voici la carte après coup " + str(nbCoups)
            client.send(laCarte.encode())

    def nbJoueurs(self):
        return len(self.lesJoueurs)

    def mettreAJourNomJoueur(self,ID,nom) :
        ancienJoueur=self.lesJoueurs[ID]
        ancienJoueur[0]=nom
        self.lesJoueurs[ID]=ancienJoueur

    def effacerRobot(self,ligne,colonne) :
        CptLigne=0
        nouvelleLigne=""
        nouvelleGrille=[]
        for elt in self.grille:
            if CptLigne==ligne :
                for i in range(len(elt)):
                    if elt[i]=="X" :
                        # On avait un X majuscule, donc pas de porte
                        nouvelleLigne=nouvelleLigne + " "
                    else :
                        if elt[i]=="x" :
                            # on avait un petit x, on etait donc sur une porte, on l'affiche pour restaurer l'état initial
                            nouvelleLigne=nouvelleLigne + "."
                        else :
                            nouvelleLigne=nouvelleLigne + elt[i]

                nouvelleGrille.append(nouvelleLigne)
            else :
                nouvelleGrille.append(elt)
            CptLigne=CptLigne+1
        self.grille=nouvelleGrille


    def positionnerRobot(self,ligne,colonne) :
        CptLigne=0
        sortie=False
        numColonne=0
        nouvelleLigne=""
        nouvelleGrille=[]
        for elt in self.grille:
            if CptLigne==ligne :
                for i in range(len(elt)):
                    if numColonne==colonne :
                        if elt[i]=="U" :
                            self.gagne=True
                            nouvelleLigne=nouvelleLigne + "$"
                        else :
                            if elt[i]=="." :
                                # On est sur une porte, on indique un petit x pour conserver cette information
                                nouvelleLigne=nouvelleLigne + "x"
                            else :
                                # On n'est pas sur une porte, on peut afficher un X classique
                                nouvelleLigne=nouvelleLigne + "X"
                    else :
                        nouvelleLigne=nouvelleLigne + elt[i]
                    numColonne=numColonne+1

                nouvelleGrille.append(nouvelleLigne)
            else :
                nouvelleGrille.append(elt)
            CptLigne=CptLigne+1
        self.grille=nouvelleGrille
        self.robot=[ligne,colonne]

    def presenceRobot(self,ligne,colonne) :

        for elt in self.lesJoueurs :
            print(str(ligne) +"/"+str(colonne) + " " + str(self.lesJoueurs[elt][3]))
            if self.lesJoueurs[elt][3][0]==ligne and self.lesJoueurs[elt][3][1]==colonne :
                return True
        return False

    def coupValide(self,ligne,colonne) :
        # On regarde si on sort du cadre
        if ligne>self.tailleGrille[0] or ligne<0 :
            return False
        if colonne>self.tailleGrille[1] or colonne<0 :
            return False
        # Puis on regarde si la case est "disponible"
        ch=self.grille[int(ligne)]

        if ch[colonne]==" " or ch[colonne]=="." or ch[colonne]=="U" :
            return True
        else :
            return False


    def chargerSauvegarde(self) :
        chemin = os.path.join("sauvegardes", "sauvegardes.txt")
        if os.path.exists(chemin) == True :
            nouveauFichier=open(chemin, "r")
            svgLu=nouveauFichier.read()
            nouveauFichier.close()
            self.grille=svgLu.split("\n")

            chemin = os.path.join("sauvegardes", "joueur.txt")
            if os.path.exists(chemin) == True :
               nouveauFichier=open(chemin, "r")
               joueur=nouveauFichier.read()
               nouveauFichier.close()
               self.pointDeVie=int(joueur)
            else :
                self.pointDeVie=100
            return True
        else :
           return False

    def initialiserPositionRobot(self) :
        numLigne=0
        for ligne in self.grille :
            for numColonne in range(0,int(len(ligne))) :
                if ligne[numColonne]=="X" :
                    self.robot[0]=numLigne
                    self.robot[1]=numColonne
            if ligne[numColonne]=="x" :
                self.robot[0]=numLigne
                self.robot[1]=numColonne
            numLigne=numLigne+1

    def initialiserTailleMaxGrille(self) :
        numLigne=0
        for ligne in self.grille :
            numColonne=int(len(ligne)-1)
            numLigne=numLigne+1
        self.tailleGrille[0]=numLigne-1
        self.tailleGrille[1]=numColonne

    def afficherPartie(self):
        for ligne in self.grille :
            print(ligne)

    def initialisationPositionJoueurs(self) :
        print("On initialise les positions")
        for elt in self.lesJoueurs :
            ok=False
            while ok==False:
                ligneInit=randint(0,self.tailleGrille[0])
                colonneInit=randint(0,self.tailleGrille[1])
                if self.coupValide(ligneInit,colonneInit) and self.presenceRobot(ligneInit,colonneInit)==False :
                    self.lesJoueurs[elt][3][0]=ligneInit
                    self.lesJoueurs[elt][3][1]=colonneInit
                    ok=True
            print("Position initiale trouvée : " + str(ligneInit) + " " + str(colonneInit))

    def afficherPositionDesRobots(self) :
        for elt in self.lesJoueurs :
            print("Joueur " + str(self.lesJoueurs[elt][0]) + " en " + str(self.lesJoueurs[elt][3][0])+ "/" + str(self.lesJoueurs[elt][3][1]))
