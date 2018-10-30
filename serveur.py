import socket,select, sys,time

from random import randint
from joueur import Joueur
from gestion import lancementServeur,nbJoueursAttendu,choixValide,nbCoupsJoue,sensJoue,saisieNombre,saisieLigneOK
from carte import Carte
from partie import Partie
from plateau import Plateau

# Definition des variables pour les connexions et le fonctionnement du serveur
hote = ''
port = 12800

listeJoueurs=[]
serveur_lance = True
clients_connectes = []
clients_a_lire = []
nbCoups=1

CASE_MUR="O"
CASE_PORTE_OUVERTE="."
CASE_PORTE_FERMEE="-"
CASE_SORTIE="U"
CASE_VIDE=" "
NB_PTS_DE_VIE_INIT=100


print("****************************")
print("Il faut gérer les fin de vie pour les utilisateurs")
print("Il faut gérer les coups multiple en un par un (notion de buffer ?")
print("Voir pour creer l'objet joueur pour regrouper plein de chose")
print("Faire un readme qui explique le jeu et le programme ainsi que les ouvertes (gestion des étages")
print("Dire qu'on peut faire évoluer le menu pour recommencer une partie sans deconnecter les joueurs, etc. voir le mettre en place")
print("Faire le ménage dans fonction initilisé  = enlever celle que j'ai prémarqué par ASUPPR_")
print("Mettre les constants dans un fichier et l'importer où j'en ai besoin")
print("quand un joueur meurt, il ne faut plus l'qfficher")
print("Insister su rle fait qu'il faut lancer avec Python3 et non pas python")
print("il faut verifier que la carte choisie a bien le nb de case vide corresondant avec le nb de joueurs attendus")
print("****************************")

nbJoueurs=nbJoueursAttendu() # On regarde dans paramètres le nombre de joueurs attendus, on sort si problème
# Création du plateau de jeu
lePlateau=Plateau([],Partie(""))
lePlateau.chargerPlateau()

# Boucle sur le menu principal

sortieMenu=False
while sortieMenu==False :
    print("Menu du jeu : ")
    print("     J - Lancer le jeux avec les " + str(nbJoueurs) + " joueur(s) attendu(s)")
    print("     V - Voir les cartes existantes")
    print("     E - Editer les cartes")
    print("     Q - Quitter leu jeu")
    choixMenuPrincipal = input("Entrez votre choix : ")

    if choixMenuPrincipal=="J" or choixMenuPrincipal=="V" or choixMenuPrincipal=="E" or choixMenuPrincipal=="Q" or choixMenuPrincipal=="j" or choixMenuPrincipal=="v" or choixMenuPrincipal=="e" or choixMenuPrincipal=="q" :
        if choixMenuPrincipal=="Q" or choixMenuPrincipal=="q" :
            print("Au revoir, à bientôt")
            exit(0)

        if choixMenuPrincipal=="j" or choixMenuPrincipal=="J" :
            sortieMenu=True

        if choixMenuPrincipal=="V" or choixMenuPrincipal=="v" :
            finVoir=False
            while finVoir==False :
                lePlateau.listerCartes()
                valeur=saisieNombre("Quel numero de carte souhaitez vous afficher ? ( 0 pour revenir au menu précédent)")

                if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                    print("Voici la carte : " + str(lePlateau.cartes[int(valeur)-1].nom))
                    lePlateau.cartes[int(valeur)-1].afficherCarte()
                else :
                    if int(valeur) == 0 :
                        finVoir=True
                    else :
                        print("Le numéro ne correspond pas à un numéro de carte existant")

        if choixMenuPrincipal=="E" or choixMenuPrincipal=="e":
                    lePlateau.chargerPlateau()
                    finEditionMenu=False
                    while finEditionMenu==False :
                        lePlateau.chargerPlateau()
                        finMenuEdition=False
                        while finMenuEdition==False :
                            print("1 - Création d'une nouvelle carte")
                            print("2 - Edition / modification d'une carte existante")
                            print("0 - Supprimer une carte")
                            print("X - Revenir au menu principal")
                            choixEdition = input("Entrez votre choix : ")
                            if choixEdition=="1" or choixEdition=="2" or choixEdition=="0" or choixEdition=="X" or choixEdition=="x":
                                finMenuEdition=True

                                # Choix creation d'une carte
                                if choixEdition=="1" :
                                    finMenuCreation=False
                                    nouvelleCarte=""
                                    while finMenuCreation==False :
                                        nomNouvelleCarte=input("Nom de la carte que vous souhaitez créer ? (vide pour revenir au menu précédent)")
                                        if nomNouvelleCarte=="" :
                                            finMenuCreation=True
                                        else :
                                            # On regarde si le fichier existe déjà
                                            if lePlateau.nomCarteExiste(nomNouvelleCarte)==True :
                                                print("Cette carte existe déjà")
                                            else :
                                                finMenuCreation=True
                                                largeurNouveau= saisieNombre("Nombre de colonnes : ")
                                                hauteurNouveau= saisieNombre("Nombre de lignes : ")
                                                print("On va créer une nouvelle de carte de " + str(largeurNouveau) + " de large et de " + str(hauteurNouveau) + " de haut")
                                                controleNb=0
                                                while controleNb != int(hauteurNouveau) :
                                                    nouvelleLigne=input("Entrez une ligne de la carte (avec espace, -, . et 0 en caractères) d'une longueur de " + str(largeurNouveau) + " caractere(s)")
                                                    if saisieLigneOK(largeurNouveau,nouvelleLigne) == True :
                                                        controleNb=controleNb+1
                                                        nouvelleCarte=nouvelleCarte + nouvelleLigne + "\n"
                                                    else :
                                                        print("Ligne incorrecte : " + nouvelleLigne)
                                                finEdition=True

                                                # On peut à présent créer la carte
                                                map=nouvelleCarte.split("\n")
                                                lePlateau.creerCarte(nomNouvelleCarte,map)
                                    lePlateau.chargerPlateau()

                                # Choix Modification  d'une carte
                                if choixEdition=="2" :
                                    finEditionMenu=False
                                    while finEditionMenu==False :
                                        lePlateau.listerCartes()
                                        valeur=saisieNombre("Quel numero de carte souhaitez vous éditer ? (0 pour revenir au menu précédent)")
                                        if int(valeur) == 0 :
                                            finEditionMenu=True
                                        else :
                                            if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                                                lePlateau.cartes[int(valeur)-1].editerCarte()
                                                finEditionMenu=True
                                                # On met à jour la liste des cartes
                                                lePlateau.chargerPlateau()
                                            else :
                                                print("Le numéro ne correspond pas à un numéro de carte existant")

                                # Choix suppression d'une carte
                                if choixEdition=="0" :
                                    finSuppressionMenu=False
                                    while finSuppressionMenu==False :
                                        lePlateau.listerCartes()
                                        valeur=saisieNombre("Quel numero de carte souhaitez vous supprimer ? (0 pour annuler et revenir au menu précédent)")
                                        if int(valeur) == 0 :
                                            finSuppressionMenu=True
                                        else :
                                            if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                                                lePlateau.cartes[int(valeur)-1].supprimerCarte()
                                                finSuppressionMenu=True
                                                # On met à jour la liste des cartes
                                                lePlateau.chargerPlateau()
                                            else :
                                                print("Le numéro ne correspond pas à un numéro de carte existant")

                                if choixEdition=="X" or choixEdition=="x" :
                                    finEdition=True
                                    finMenuEdition=True
                                    finEditionMenu=True
                            else :
                                print("Vous n'avez pas fait un choix autorisé")
    else :
        print("choix incorrect")

lePlateau.listerCartes()

if lePlateau.choisirCartePartie()==False :
    print("Au revoir, à bientot")
    exit(0)

lePlateau.partie.initialiserTailleMaxGrille()
print("Taille de la grille : " + str(lePlateau.partie.tailleGrille[0]) + " par " +  str(lePlateau.partie.tailleGrille[1]))
print("Plateau créé, en attente de connexions de " + str(nbJoueurs) + " joueurs\n")

connexion_principale=lancementServeur(hote,port)   # Lancement du serveur

# Le serveur se met en écoute de nouvelles connexions jusqu'à atteindre le nombre attendu
clients_connectes=lePlateau.enAttenteConnexionJoueurs(int(nbJoueurs),connexion_principale,NB_PTS_DE_VIE_INIT)

# Les joueurs doivent se présenter (donner leur nom)
lePlateau.presentationDesJoueurs(nbJoueurs,clients_connectes)
lePlateau.partie.toutLeMondePassif(clients_connectes)

lePlateau.partie.initialisationPositionJoueurs()
print("La position des joueurs a été initialisée")

lePlateau.partie.afficherCarteATous(clients_connectes,nbCoups)
lePlateau.partie.initialiserToursjoueurs()

lePlateau.partie.afficherListeJoueurs()
print("la liste des tours de joueurs a été initialisée")
lePlateau.partie.messageAuxPassifs(-1,clients_connectes,"[MSG]" + "Tous les joueurs sont arrivés")

lePlateau.partie.annoncerNumeroAuxJoueurs(clients_connectes)

# Le serveur se met en dialogue avec les clients connectés


# On tire au sort celui qui commence
joueurActuel=randint(0,int(nbJoueurs)-1)
#print("C'est au joueur " + str(joueurActuel) + " de commencer")

lePlateau.partie.donnerLaMain(joueurActuel,clients_connectes)
lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + "C'est à " + str(lePlateau.partie.nomJoueur(joueurActuel)) + " de jouer")

lePlateau.partie.afficherPositionDesRobots()
print(lePlateau.partie.carteAvecRobot())

print("Début de la partie\n")


while serveur_lance:
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
    except select.error:
        pass
    else:

        # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            #print("Client actif numero : "+ str(joueurActuel))
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()
            clientID=client.getpeername()[1]

            if msg_recu == "fin":
                lePlateau.partie.supprimerUnJoueur(int(clientID))
                client.close()
                clients_connectes.remove(client)
                lePlateau.partie.afficherListeJoueurs()
                if lePlateau.partie.nbJoueurs()==0 :
                    serveur_lance=False
                #client.send(b"Votre message a ete recu par le serveur")
            else :
                if msg_recu != "" :
                    # On peut prendre en compte le coup
                    #print("On peut jouer le coup - " + str(lePlateau.partie.nomJoueur(joueurActuel)) + " (" + str(clientID) + ") : " + str(msg_recu) )
                    retour=choixValide(msg_recu)
                    if retour == 1 :
                        nbCoups=nbCoupsJoue(msg_recu)
                        sens=sensJoue(msg_recu)
                        for i in range(0,int(nbCoups)) :
                            lePlateau.partie.jouerUnCoup(clientID,sens)
                        lePlateau.partie.messageNbVies(joueurActuel,clients_connectes)
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joué " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 2 :
                        lePlateau.partie.creerMur(clientID,msg_recu[1])
                        nbCoups=0
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joué " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 3 :
                        lePlateau.partie.supprimerMur(clientID,msg_recu[1])
                        nbCoups=0
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joué " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 4 : # Abandon du joueur
                        lePlateau.partie.tuerJoueur(joueurActuel)
                        lePlateau.partie.messageNbVies(joueurActuel,clients_connectes)
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " vient d'abandonner")


                    #lePlateau.partie.afficherCartePartie()
                    lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joué")
                    lePlateau.partie.toutLeMondePassif(clients_connectes)
                    time.sleep(0.1)

                    lePlateau.partie.afficherCarteATous(clients_connectes,nbCoups)
                    if lePlateau.joueurGagne(clientID) == True :
                        lePlateau.partie.toutLeMondePassif(clients_connectes)
                        lePlateau.partie.messageATous(clients_connectes,"[GAGNE]" + "Victoire du joueur " + lePlateau.partie.nomJoueur(joueurActuel))
                        print(lePlateau.partie.carteAvecRobot())
                        print("Victoire du joueur " + lePlateau.partie.nomJoueur(joueurActuel))
                        serveur_lance = False
                    else :
                        joueurActuel=lePlateau.partie.joueurSuivant(joueurActuel,int(nbJoueurs))
                        if joueurActuel!=-1 :
                            lePlateau.partie.donnerLaMain(joueurActuel,clients_connectes)
                            lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + "C'est à " + lePlateau.partie.nomJoueur(joueurActuel) + " de jouer")
                            print(lePlateau.partie.carteAvecRobot())
                        else : # Tout le monde est mort
                            lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[FIN]")
                            print("Tout le monde est mort")
                            serveur_lance=False



            #print("Nombre de joueurs = " + str(lePlateau.partie.nbJoueurs()))

print("fin du jeu")
connexion_principale.close()




