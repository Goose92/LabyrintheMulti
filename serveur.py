# -*-coding:Utf-8 -*
import socket,select, sys,time

from random import randint
from joueur import Joueur
from gestion import lancementServeur,nbJoueursAttendu,choixValide,nbCoupsJoue,sensJoue,saisieNombre,saisieLigneOK,gestionVersionPython
from carte import Carte
from partie import Partie
from plateau import Plateau
from constants import CASE_MUR,CASE_PORTE_OUVERTE,CASE_PORTE_FERMEE,CASE_SORTIE,CASE_VIDE,NB_PTS_DE_VIE_INIT,HOTE,PORT

listeJoueurs=[]
serveur_lance = True
clients_connectes = []
clients_a_lire = []
nbCoups=1

# Si la version Python utilisee est inferieure a 3, on sort (necessaire pour certaines fonctions)
gestionVersionPython()

print("****************************")
print("Faire le menage dans fonction initilisee  = enlever celle que j'ai premarque par ASUPPR_")
print("il faut verifier que la carte choisie a bien le nb de case vide corresondant avec le nb de joueurs attendus")
print("****************************")

nbJoueurs=nbJoueursAttendu() # On regarde dans parametres le nombre de joueurs attendus, on sort si probleme
# Creation du plateau de jeu
lePlateau=Plateau([],Partie(""))
lePlateau.chargerPlateau()

# Boucle sur le menu principal

sortieMenu=False
while sortieMenu==False :
    print("Menu du jeu : ")
    print("     J - Lancer le jeu avec les " + str(nbJoueurs) + " joueur(s) attendu(s)")
    print("     V - Voir les cartes existantes")
    print("     E - Editer les cartes")
    print("     Q - Quitter le jeu")
    choixMenuPrincipal = input("Entrez votre choix : ")

    if choixMenuPrincipal=="J" or choixMenuPrincipal=="V" or choixMenuPrincipal=="E" or choixMenuPrincipal=="Q" or choixMenuPrincipal=="j" or choixMenuPrincipal=="v" or choixMenuPrincipal=="e" or choixMenuPrincipal=="q" :
        if choixMenuPrincipal=="Q" or choixMenuPrincipal=="q" :
            print("Au revoir, a bientot")
            exit(0)

        if choixMenuPrincipal=="j" or choixMenuPrincipal=="J" :
            sortieMenu=True

        if choixMenuPrincipal=="V" or choixMenuPrincipal=="v" :
            finVoir=False
            while finVoir==False :
                lePlateau.listerCartes()
                valeur=saisieNombre("Quel numero de carte souhaitez vous afficher ? ( 0 pour revenir au menu precedent)")

                if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                    print("Voici la carte : " + str(lePlateau.cartes[int(valeur)-1].nom))
                    lePlateau.cartes[int(valeur)-1].afficherCarte()
                else :
                    if int(valeur) == 0 :
                        finVoir=True
                    else :
                        print("Le numero ne correspond pas a un numero de carte existant")

        if choixMenuPrincipal=="E" or choixMenuPrincipal=="e":
                    lePlateau.chargerPlateau()
                    finEditionMenu=False
                    while finEditionMenu==False :
                        lePlateau.chargerPlateau()
                        finMenuEdition=False
                        while finMenuEdition==False :
                            print("1 - Creation d'une nouvelle carte")
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
                                        nomNouvelleCarte=input("Nom de la carte que vous souhaitez creer ? (vide pour revenir au menu precedent)")
                                        if nomNouvelleCarte=="" :
                                            finMenuCreation=True
                                        else :
                                            # On regarde si le fichier existe deja
                                            if lePlateau.nomCarteExiste(nomNouvelleCarte)==True :
                                                print("Cette carte existe deja")
                                            else :
                                                finMenuCreation=True
                                                largeurNouveau= saisieNombre("Nombre de colonnes : ")
                                                hauteurNouveau= saisieNombre("Nombre de lignes : ")
                                                print("On va creer une nouvelle de carte de " + str(largeurNouveau) + " de large et de " + str(hauteurNouveau) + " de haut")
                                                controleNb=0
                                                while controleNb != int(hauteurNouveau) :
                                                    nouvelleLigne=input("Entrez une ligne de la carte (avec espace, -, . et 0 en caracteres) d'une longueur de " + str(largeurNouveau) + " caractere(s)")
                                                    if saisieLigneOK(largeurNouveau,nouvelleLigne) == True :
                                                        controleNb=controleNb+1
                                                        nouvelleCarte=nouvelleCarte + nouvelleLigne + "\n"
                                                    else :
                                                        print("Ligne incorrecte : " + nouvelleLigne)
                                                finEdition=True

                                                # On peut a present creer la carte
                                                map=nouvelleCarte.split("\n")
                                                lePlateau.creerCarte(nomNouvelleCarte,map)
                                    lePlateau.chargerPlateau()

                                # Choix Modification  d'une carte
                                if choixEdition=="2" :
                                    finEditionMenu=False
                                    while finEditionMenu==False :
                                        lePlateau.listerCartes()
                                        valeur=saisieNombre("Quel numero de carte souhaitez vous editer ? (0 pour revenir au menu precedent)")
                                        if int(valeur) == 0 :
                                            finEditionMenu=True
                                        else :
                                            if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                                                lePlateau.cartes[int(valeur)-1].editerCarte()
                                                finEditionMenu=True
                                                # On met a jour la liste des cartes
                                                lePlateau.chargerPlateau()
                                            else :
                                                print("Le numero ne correspond pas a un numero de carte existant")

                                # Choix suppression d'une carte
                                if choixEdition=="0" :
                                    finSuppressionMenu=False
                                    while finSuppressionMenu==False :
                                        lePlateau.listerCartes()
                                        valeur=saisieNombre("Quel numero de carte souhaitez vous supprimer ? (0 pour annuler et revenir au menu precedent)")
                                        if int(valeur) == 0 :
                                            finSuppressionMenu=True
                                        else :
                                            if int(valeur) >0 and int(valeur)<=lePlateau.nombreDeCartes() :
                                                lePlateau.cartes[int(valeur)-1].supprimerCarte()
                                                finSuppressionMenu=True
                                                # On met a jour la liste des cartes
                                                lePlateau.chargerPlateau()
                                            else :
                                                print("Le numero ne correspond pas a un numero de carte existant")

                                if choixEdition=="X" or choixEdition=="x" :
                                    finEdition=True
                                    finMenuEdition=True
                                    finEditionMenu=True
                            else :
                                print("Vous n'avez pas fait un choix autorise")
    else :
        print("choix incorrect")

lePlateau.listerCartes()

carteOk=False
while carteOk==False :
    if lePlateau.choisirCartePartie()==False :
        print("Au revoir, a bientot")
        exit(0)
    if int(lePlateau.partie.nbCasesLibres())>int(nbJoueurs) :
        carteOk=True
    else :
        print("La carte que vous avez choisi n'a pas assez de places libres pour accueillir les joueurs attendus")

lePlateau.partie.initialiserTailleMaxGrille()
print("Taille de la grille : " + str(lePlateau.partie.tailleGrille[0]) + " par " +  str(lePlateau.partie.tailleGrille[1]))
print("Plateau cree, en attente de connexions de " + str(nbJoueurs) + " joueurs\n")

connexion_principale=lancementServeur(HOTE,PORT)   # Lancement du serveur

# Le serveur se met en ecoute de nouvelles connexions jusqu'a atteindre le nombre attendu
clients_connectes=lePlateau.enAttenteConnexionJoueurs(int(nbJoueurs),connexion_principale,NB_PTS_DE_VIE_INIT)

# Les joueurs doivent se presenter (donner leur nom)
lePlateau.presentationDesJoueurs(nbJoueurs,clients_connectes)
lePlateau.partie.toutLeMondePassif(clients_connectes)

lePlateau.partie.initialisationPositionJoueurs()
print("La position des joueurs a ete initialisee")

lePlateau.partie.afficherCarteATous(clients_connectes,nbCoups)
lePlateau.partie.initialiserToursjoueurs()

lePlateau.partie.afficherListeJoueurs()
print("la liste des tours de joueurs a ete initialisee")
lePlateau.partie.messageAuxPassifs(-1,clients_connectes,"[MSG]" + "Tous les joueurs sont arrives")

lePlateau.partie.annoncerNumeroAuxJoueurs(clients_connectes)

# Le serveur se met en dialogue avec les clients connectes


# On tire au sort celui qui commence
joueurActuel=randint(0,int(nbJoueurs)-1)
#print("C'est au joueur " + str(joueurActuel) + " de commencer")

lePlateau.partie.donnerLaMain(joueurActuel,clients_connectes)
lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + "C'est a " + str(lePlateau.partie.nomJoueur(joueurActuel)) + " de jouer")

lePlateau.partie.afficherPositionDesRobots()
print(lePlateau.partie.carteAvecRobot())

print("Debut de la partie\n")


while serveur_lance:
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
    except select.error:
        pass
    else:

        # On parcourt la liste des clients a lire
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
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joue " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 2 :
                        lePlateau.partie.creerMur(clientID,msg_recu[1])
                        nbCoups=0
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joue " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 3 :
                        lePlateau.partie.supprimerMur(clientID,msg_recu[1])
                        nbCoups=0
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joue " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")

                    if retour == 4 : # Abandon du joueur
                        lePlateau.partie.tuerJoueur(joueurActuel)
                        lePlateau.partie.messageNbVies(joueurActuel,clients_connectes)
                        print(str(lePlateau.partie.nomJoueur(joueurActuel)) + " vient d'abandonner")
                        lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + str(lePlateau.partie.nomJoueur(joueurActuel)) + " vient d'abandonner")



                    #lePlateau.partie.afficherCartePartie()
                    lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + str(lePlateau.partie.nomJoueur(joueurActuel)) + " a joue")
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
                            lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + "C'est a " + lePlateau.partie.nomJoueur(joueurActuel) + " de jouer")
                            print(lePlateau.partie.carteAvecRobot())
                        else : # Tout le monde est mort
                            lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[FIN]")
                            print("Tout le monde est mort")
                            serveur_lance=False



            #print("Nombre de joueurs = " + str(lePlateau.partie.nbJoueurs()))

print("fin du jeu")
connexion_principale.close()




