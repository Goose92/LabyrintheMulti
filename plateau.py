# -*-coding:Utf-8 -*

# Ce module contient la classe plateau
# La classe Plateau permet de gérer l'objet plateau qui contient des cartes et une partie
# La classe contient également plusieurs actions (méthodes) pour le manipuler

import os
import socket
import select
from carte import Carte
from gestion import saisieLigneOK,formatLigneOK,choixValide,nbCoupsJoue,sensJoue,saisieNombre

class Plateau:

    """Classe représentant un plateau"""

    def __init__(self, desCartes,unePartie):
        self.cartes = desCartes
        self.partie = unePartie

    def reinitialiserPartie(self) :
        self.partie.pointDeVie=100
        self.partie.gagne=False
        self.partie.nbCoups=0

    def afficherLesCartes(self) :
        print("On affiche le plateau au complet")
        print(self.nombreDeCartes())
        for elt in self.cartes :
            print("Carte : " + elt.nom)
            elt.afficherCarte()

    def sauvegarderPartie(self) :
        # On sauvegarde la carte de la partie
        chemin = os.path.join("sauvegardes", "sauvegardes.txt")
        nouveauFichier=open(chemin, "w")
        chaineSvg=""
        for elt in self.partie.grille:
            chaineSvg=chaineSvg + elt + "\n"
        nouveauFichier.write(chaineSvg[0:int(len(chaineSvg))-1])
        # On enlève le dernier caractère qui est un retour a la ligne inutile
        nouveauFichier.close()
        # On sauvegarde les caractéristique de la partie (nb de vies pour l'instant)
        chemin = os.path.join("sauvegardes", "joueur.txt")
        nouveauFichier=open(chemin, "w")
        chaineSvg=str(self.partie.pointDeVie)
        nouveauFichier.write(chaineSvg)
        nouveauFichier.close()

    def supprimerSauvegarde(self) :
        chemin = os.path.join("sauvegardes", "sauvegardes.txt")
        if os.path.exists(chemin) == True :
            os.remove(chemin)
        chemin = os.path.join("sauvegardes", "joueur.txt")
        if os.path.exists(chemin) == True :
            os.remove(chemin)


    def chargerPlateau(self) :
        self.cartes=[]
        for nom_fichier in os.listdir("cartes"):
            if nom_fichier.endswith(".txt"):
                chemin = os.path.join("cartes", nom_fichier)
                nom_carte = nom_fichier[:-4].lower()
                with open(chemin, "r") as fichier:
                    contenu = fichier.read()
                # On transforme la chaine en tableau (carte)
                map=contenu.split("\n")
                # On crée un objet carte

                uneCarte=Carte(nom_carte,map)
                # On l'ajoute à notre tableau de carte (cartes)
                self.cartes.append(uneCarte)

    def choisirCartePartie(self) :
        choixUtilisateurValide=False

        while choixUtilisateurValide==False :
            choixCarte=saisieNombre("Avec quel carte souhaitez vous jouer ? ( 0 pour quitter) ")

            if choixCarte >0 and choixCarte<=self.nombreDeCartes() :
                print("Vous souhaitez jouer avec la carte " + self.cartes[choixCarte-1].nom)
                choixUtilisateurValide=True
                # On initialise la partie avec la grille correspondante à la carte choisie
                self.partie.grille=self.cartes[int(choixCarte)-1].labyrinthe
            else :
                if choixCarte==0 :
                    # On revient au menu précédent
                    choixUtilisateurValide=True
                    return False
                else :
                    print("Le numéro ne correspond pas à un numéro de carte existant")
        return True

    def listerCartes(self) :
        print("Voici la liste des cartes : ")
        for i, carte in enumerate(self.cartes):
            print("  {} - {}".format(i + 1, carte.nom))

    def nombreDeCartes(self) :
        i=0
        for i, carte in enumerate(self.cartes):
            i=i+1
        return i

    def joueurGagne(self, joueur) :
        # On commence par trouver la position du robot
        for elt in self.partie.lesJoueurs :
            if elt==joueur :
                ligneRobot=self.partie.lesJoueurs[elt][3][0]
                colonneRobot=self.partie.lesJoueurs[elt][3][1]
        if self.partie.estUneSortie(ligneRobot,colonneRobot) :
            return True
        else :
            return False

    def nomCarteExiste(self,nom) :
        chemin = os.path.join("cartes", nom)
        chemin=chemin + ".txt"
        if os.path.exists(chemin) == True :
           return True
        else :
           return False

    def creerCarte(self,nomCarte,map) :
        # Il faut vérifier si le format de la carte est bien correct
        nouvelleCarte=Carte(nomCarte,map)
        if nouvelleCarte.carteValide() :
            # On enlève le dernier retour à la ligne inutile
            nouvelleCarte.labyrinthe=nouvelleCarte.labyrinthe[0:int(len(nouvelleCarte.labyrinthe))-1]
            print("Carte valide et créée.")
            self.cartes.append(nouvelleCarte)
            nouvelleCarte.enregistrerNouvelleCarte()
        else :
            print("Erreur dans le format (il faut au moins un U)")
        finEditionMenu=True

    def presentationDesJoueurs(self, nbJoueursConnectes,clients_connectes) :
        nomsOk=0
        while int(nomsOk)<int(nbJoueursConnectes) :
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
            except select.error:
                pass
            else:
                # On parcourt la liste des clients à lire
                for client in clients_connectes:
                    msg_recu = client.recv(1024)
                    # Peut planter si le message contient des caractères spéciaux
                    msg_recu = msg_recu.decode()
                    clientID=client.getpeername()[1]
                    if str(msg_recu[:5])=="[NOM]" :
                        self.partie.mettreAJourNomJoueur(int(client.getpeername()[1]),str(msg_recu[5:]))
                        nomsOk=nomsOk+1
                        print("Le joueur " + str(msg_recu[5:]) + " s'est présenté")

    def enAttenteConnexionJoueurs(self,nbJoueurs,connexion_principale,NbPtsDeVieInit) :
        nbJoueursConnectes=0
        clients_connectes=[]
        while nbJoueursConnectes!= int(nbJoueurs):

            # Vérifie que de nouveaux clients ne demandent pas à se connecter
            connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)
            for connexion in connexions_demandees:

                connexion_avec_client, infos_connexion = connexion.accept()
                # On ajoute le socket connecté à la liste des clients
                clients_connectes.append(connexion_avec_client)

                print("Un nouveau joueur s'est connecté (" + str(infos_connexion[1]) + ")")
                # On crée le nouveau joueur sur le plateau
                self.partie.ajouterUnJoueur(str(infos_connexion[1]),"vide",connexion_avec_client,str(nbJoueursConnectes+1),NbPtsDeVieInit)
                nbJoueursConnectes=nbJoueursConnectes+1
                print(str(nbJoueursConnectes) + " joueur(s) connecté(s) sur les " + str(nbJoueurs) + " attendu(s)")
        return clients_connectes