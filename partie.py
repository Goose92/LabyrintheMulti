# -*-coding:Utf-8 -*

# Ce module contient la classe Partie
# Une carte est composée d'une grille (carte), différentes valeurs, la position du robot
# La classe contient également plusieurs méthodes pour agir sur l'objet Partie

import os,socket,select,time,copy
from random import randint

CASE_MUR="O"
CASE_PORTE_OUVERTE="."
CASE_PORTE_FERMEE="-"
CASE_SORTIE="U"
CASE_VIDE=" "

class Partie:

    """Classe représentant un partie"""

    def __init__(self, carte):
        self.grille = carte.split("\n")
        self.joueur=[]
            # Champ 0 : le nom du joueur
            # Champ 1 : le socket du client associé
            # Champ 2 : ??????????????
            # Champ 3 : Le robot (ligne, colonne)
            # Champ 4 : Le caractère pour afficher le robot du joueur (1 à 9)
            # Champ 5 : le nb de points de vie

        self.lesJoueurs=dict() # un dictionnaire avec nom, puis connection, puis tour (si true c'est à son tour)
        #self.nbCoups=0
        self.tailleGrille=[0,0]
        #self.robot=[0,0]
        self.gagne=False
        #self.pointDeVie=100
        self.listeJoueurs=[]

    def resteDesVivants(self) :
        reste=False
        for elt in self.lesJoueurs :
            if self.lesJoueurs[elt][5]>0 :
                reste = True
        return reste

    def nbCasesLibres(self) :
        # permet de connaitre le nombre de places libres sur une carte afin de ne pas l'autoriser si le nombre de joueurs est supérieur
        nbVide=0
        for elt in self.grille :
            for i in range(0,int(len(elt))) :
                if elt[i]==CASE_VIDE or elt[i]==CASE_PORTE_OUVERTE:
                    nbVide=nbVide+1
        return nbVide

    def estVivant(self,num) :
        indice=0
        for elt in self.lesJoueurs :
            if indice==num :
                if self.lesJoueurs[elt][5]>0 :
                    return True
                else :
                    return False
            indice=indice+1

    def tuerJoueur(self,joueur):
        indice=0
        for elt in self.lesJoueurs :
            if indice==joueur :
                self.lesJoueurs[elt][5]=0
            indice=indice+1

    def joueurSuivant(self,num,max) :
        trouve=False
        if self.resteDesVivants()==False :
            return -1
        else :
            suivant=num+1
            while trouve==False :
                if suivant>=max :
                    suivant=0
                if self.estVivant(suivant) == True :
                    trouve=True
                    return suivant
                else :
                    suivant=suivant+1

    def nomJoueur(self,num) :
        indice=0
        for elt in self.lesJoueurs :
            if indice==num :
                return str(self.lesJoueurs[elt][0])
            indice=indice+1

    def nbPtsJoueur(self,num) :
          indice=0
          for elt in self.lesJoueurs :
              if indice==num :
                  return self.lesJoueurs[elt][5]
              indice=indice+1

    def afficherChampsjoueur(self) :
        for elt in self.lesJoueurs :
            print("Un joueur")
            print(self.lesJoueurs[elt][0])
            print(self.lesJoueurs[elt][1])
            print(self.lesJoueurs[elt][2])
            print(self.lesJoueurs[elt][3])
            print(self.lesJoueurs[elt][4])
    def afficherCartePartie(self) :
        for elt in self.grille :
            print(elt)

    def ajouterUnJoueur(self,ID,nom,connection,caractere,PtsDeVieInit) :
        leJoueur=[nom,connection,False,[0,0],caractere,PtsDeVieInit]
        self.lesJoueurs[int(ID)]=leJoueur

    def supprimerUnJoueur(self,ID) :
        del self.lesJoueurs[ID]

    def afficherListeJoueurs(self) :
        if len(self.lesJoueurs) == 0 :
            print("Il n'y pas pas de joueur connecté")
        else :
            laListe=""
            for elt in self.lesJoueurs :
                laListe=laListe + " " + str(self.lesJoueurs[elt][0])
            print("Liste des joueurs connectés : " + laListe)

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

    def messageNbVies(self,joueurActif,connection) :
        clients_a_lire = []
        messageAEnvoyer="[VIE]" + str(self.nbPtsJoueur(joueurActif))
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        num=0
        for client in connection:
            if num==int(joueurActif) :
                client.send(messageAEnvoyer.encode())
            num=num+1

    def annoncerNumeroAuxJoueurs(self,connection) :
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        num=1
        for client in connection:
            messageAEnvoyer="[DOSSARD]" + str(num)
            client.send(messageAEnvoyer.encode())
            num=num+1


    def messageATous(self,connection,messageAEnvoyer) :
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass
        for client in connection:
            client.send(messageAEnvoyer.encode())


    def afficherCarteATous(self,connection,nbCoups) :
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(connection,[], [], 0.05)
        except select.error:
            pass

        laCarte=self.carteAvecRobot()
        for client in connection:
            client.send(laCarte.encode())

    def carteAvecRobot(self) :
        laCarte=""
        copieGrille=[]
        copieGrille=copy.copy(self.grille)

        num=0
        for elt in self.lesJoueurs :
            if self.estVivant(num)==True :
                laLigneAModifier=copieGrille[self.lesJoueurs[elt][3][0]]

                laLigne=laLigneAModifier[:self.lesJoueurs[elt][3][1]] + self.lesJoueurs[elt][4] + laLigneAModifier[self.lesJoueurs[elt][3][1]+1:]
                copieGrille[self.lesJoueurs[elt][3][0]]=laLigne
            num=num+1

        for elt in copieGrille :
            laCarte=laCarte + elt + "\n"
        # On enlève le dernier retour à la ligne inutile
        laCarte=laCarte[0:int(len(laCarte))-1]
        return laCarte

    def mettreAJourNomJoueur(self,ID,nom) :
        ancienJoueur=self.lesJoueurs[ID]
        ancienJoueur[0]=nom
        self.lesJoueurs[ID]=ancienJoueur

    def presenceRobot(self,ligne,colonne) :
        num=0
        for elt in self.lesJoueurs :
            if self.estVivant(num) == True :
                if self.lesJoueurs[elt][3][0]==ligne and self.lesJoueurs[elt][3][1]==colonne :
                    return True
            num=num+1
        return False

    def coupValide(self,ligne,colonne) :
        # On regarde si on sort du cadre
        if ligne>self.tailleGrille[0] or ligne<0 :
            return False
        if colonne>self.tailleGrille[1] or colonne<0 :
            return False

        # Puis on regarde si la case est "disponible"
        ch=self.grille[int(ligne)]

        if ch[colonne]==CASE_VIDE or ch[colonne]==CASE_PORTE_OUVERTE or ch[colonne]==CASE_SORTIE :
            return True
        else :
            return False

    def estUneSortie(self,ligne,colonne) :
        # Puis on regarde si la case est "disponible"
        ch=self.grille[int(ligne)]

        if ch[colonne]==CASE_SORTIE :
            return True
        else :
            return False

    def creerMur(self,clientID,sens) :
        # On commence par trouver la position du robot
        for elt in self.lesJoueurs :
            if elt==clientID :
                ligneRobot=self.lesJoueurs[elt][3][0]
                colonneRobot=self.lesJoueurs[elt][3][1]
                ligneAMurer=ligneRobot
                colonneAMurer=colonneRobot
                if sens=="N" :
                    ligneAMurer=ligneAMurer-1
                if sens=="S" :
                    ligneAMurer=ligneAMurer+1
                if sens=="E" :
                    colonneAMurer=colonneAMurer+1
                if sens=="O" :
                    colonneAMurer=colonneAMurer-1
                if self.estUnePorte(ligneAMurer,colonneAMurer) :
                    ligneAModifier=self.grille[int(ligneAMurer)]
                    self.grille[int(ligneAMurer)]=ligneAModifier[:colonneAMurer] + CASE_PORTE_FERMEE + ligneAModifier[colonneAMurer+1:]

    def supprimerMur(self,clientID,sens) :
        # On commence par trouver la position du robot
        for elt in self.lesJoueurs :
            if elt==clientID :
                ligneRobot=self.lesJoueurs[elt][3][0]
                colonneRobot=self.lesJoueurs[elt][3][1]
                ligneAMurer=ligneRobot
                colonneAMurer=colonneRobot
                if sens=="N" :
                    ligneAMurer=ligneAMurer-1
                if sens=="S" :
                    ligneAMurer=ligneAMurer+1
                if sens=="E" :
                    colonneAMurer=colonneAMurer+1
                if sens=="O" :
                    colonneAMurer=colonneAMurer-1
                if self.estUnePorte(ligneAMurer,colonneAMurer) :
                    ligneAModifier=self.grille[int(ligneAMurer)]
                    self.grille[int(ligneAMurer)]=ligneAModifier[:colonneAMurer] + CASE_PORTE_OUVERTE + ligneAModifier[colonneAMurer+1:]


    def estUnePorte(self,ligne,colonne) :
        # On regarde si on sort du cadre
        if ligne>self.tailleGrille[0] or ligne<0 :
            return False
        if colonne>self.tailleGrille[1] or colonne<0 :
            return False
        # Puis on regarde si la case est "disponible"
        ch=self.grille[int(ligne)]

        if ch[colonne]==CASE_PORTE_OUVERTE or ch[colonne]==CASE_PORTE_FERMEE :
            return True
        else :
            return False

    def jouerUnCoup(self, joueur, sens) :
        # On commence par trouver la position du robot
        for elt in self.lesJoueurs :
            if elt==joueur :
                ligneRobot=self.lesJoueurs[elt][3][0]
                colonneRobot=self.lesJoueurs[elt][3][1]

                if sens=="N" :
                    # Test de la case cible pour voir si on peut y aller
                    if self.coupValide(ligneRobot-1,colonneRobot)==True and self.presenceRobot(ligneRobot-1,colonneRobot)==False :
                        self.lesJoueurs[elt][3][0]=self.lesJoueurs[elt][3][0]-1
                    else :
                        self.lesJoueurs[elt][5]=self.lesJoueurs[elt][5]-1
                    return 1

                if sens=="S" :
                    # Test de la case cible pour voir si on peut y aller
                    if self.coupValide(ligneRobot+1,colonneRobot)==True and self.presenceRobot(ligneRobot+1,colonneRobot)==False :
                        self.lesJoueurs[elt][3][0]=self.lesJoueurs[elt][3][0]+1
                    else :
                        self.lesJoueurs[elt][5]=self.lesJoueurs[elt][5]-1
                    return 1

                if sens=="E" :
                    # Test de la case cible pour voir si on peut y aller
                    if self.coupValide(ligneRobot,colonneRobot+1)==True and self.presenceRobot(ligneRobot,colonneRobot+1)==False :
                        self.lesJoueurs[elt][3][1]=self.lesJoueurs[elt][3][1]+1
                    else :
                        self.lesJoueurs[elt][5]=self.lesJoueurs[elt][5]-1
                    return 1

                if sens=="O" :
                    # Test de la case cible pour voir si on peut y aller
                    if self.coupValide(ligneRobot,colonneRobot-1)==True and self.presenceRobot(ligneRobot,colonneRobot-1)==False :
                        self.lesJoueurs[elt][3][1]=self.lesJoueurs[elt][3][1]-1
                    else :
                        self.lesJoueurs[elt][5]=self.lesJoueurs[elt][5]-1
                    return 1
        return -1

    def placeLibre(self,ligne,colonne) :
        # On regarde si on sort du cadre
        if ligne>self.tailleGrille[0] or ligne<0 :
            return False
        if colonne>self.tailleGrille[1] or colonne<0 :
            return False
        # Puis on regarde si la case est "disponible"
        ch=self.grille[int(ligne)]

        if ch[colonne]==CASE_VIDE or ch[colonne]==CASE_PORTE_OUVERTE :
            return True
        else :
            return False

    def initialiserTailleMaxGrille(self) :
        numLigne=0
        for ligne in self.grille :
            numColonne=int(len(ligne)-1)
            numLigne=numLigne+1
        self.tailleGrille[0]=numLigne-1
        self.tailleGrille[1]=numColonne

    def initialisationPositionJoueurs(self) :
        for elt in self.lesJoueurs :
            ok=False
            while ok==False:
                ligneInit=randint(0,self.tailleGrille[0])
                colonneInit=randint(0,self.tailleGrille[1])
                if self.placeLibre(ligneInit,colonneInit) and self.presenceRobot(ligneInit,colonneInit)==False :
                    self.lesJoueurs[elt][3][0]=ligneInit
                    self.lesJoueurs[elt][3][1]=colonneInit
                    ok=True
