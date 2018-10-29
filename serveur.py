import socket
import select, sys,time

from joueur import Joueur
from gestion import lancementServeur,joueurSuivant,nbJoueursAttendu,choixValide,nbCoupsJoue,sensJoue
from carte import Carte
from partie import Partie
from plateau import Plateau

# Definition des variables pour les connexions et le fonctionnement du serveur
hote = ''
port = 12800
NbPtsDeVieInit=100
listeJoueurs=[]
serveur_lance = True
clients_connectes = []
clients_a_lire = []
nbCoups=1

mur="O"
porteOuverte="."
porteFermee="-"
sortie="U"
print("Il faut gérer les fin de vie pour les tilisateurs")


nbJoueurs=nbJoueursAttendu() # On regarde dans paramètres le nombre de joueurs attendus, on sort si problème

# Création du plateau de jeu
lePlateau=Plateau([],Partie(""))
lePlateau.chargerPlateau()
print("Plateau créé, en attente de connexions de " + str(nbJoueurs) + " joueurs\n")

connexion_principale=lancementServeur(hote,port)   # Lancement du serveur

# Le serveur se met en écoute de nouvelles connexions jusqu'à atteindre le nombre attendu
clients_connectes=lePlateau.enAttenteConnexionJoueurs(int(nbJoueurs),connexion_principale,NbPtsDeVieInit)

lePlateau.listerCartes()
lePlateau.choisirCartePartie()
lePlateau.partie.initialiserTailleMaxGrille()
print("Taille de la grille : " + str(lePlateau.partie.tailleGrille[0]) + " par " +  str(lePlateau.partie.tailleGrille[1]))

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
joueurActuel=0

# On donne la main au premier joueur (on peut le faire via un random pour le premier)
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
                    print("On peut jouer le coup - " + str(lePlateau.partie.nomJoueur(joueurActuel)) + " (" + str(clientID) + ") : " + str(msg_recu) )
                    retour=choixValide(msg_recu)
                    if retour == 1 :
                        nbCoups=nbCoupsJoue(msg_recu)
                        sens=sensJoue(msg_recu)
                        for i in range(0,int(nbCoups)) :
                            lePlateau.partie.jouerUnCoup(clientID,sens)
                        lePlateau.partie.messageNbVies(joueurActuel,clients_connectes)

                    if retour == 2 :
                        lePlateau.partie.creerMur(clientID,msg_recu[1])
                        nbCoups=0
                    if retour == 3 :
                        lePlateau.partie.supprimerMur(clientID,msg_recu[1])
                        nbCoups=0
                    print(str(lePlateau.partie.nomJoueur(joueurActuel)) + "a joué " + str(msg_recu) + " (il lui reste " + str(lePlateau.partie.nbPtsJoueur(joueurActuel)) + " points)")


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
                        joueurActuel=joueurSuivant(joueurActuel,int(nbJoueurs))
                        lePlateau.partie.donnerLaMain(joueurActuel,clients_connectes)
                        lePlateau.partie.messageAuxPassifs(joueurActuel,clients_connectes,"[MSG]" + "C'est à " + lePlateau.partie.nomJoueur(joueurActuel) + " de jouer")
                        print(lePlateau.partie.carteAvecRobot())



            #print("Nombre de joueurs = " + str(lePlateau.partie.nbJoueurs()))

print("fin du jeu")
connexion_principale.close()




