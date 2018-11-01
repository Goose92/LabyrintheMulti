# -*-coding:Utf-8 -*


import socket,string,sys
from gestion import flush_input,choixValide,sensJoue,nbCoupsJoue,gestionVersionPython
from constants import HOTE,PORT,NB_PTS_DE_VIE_INIT

# Si la version Python utilisee est inferieure a 3, on sort (necessaire pour certaines fonctions)
gestionVersionPython()

nbVie=NB_PTS_DE_VIE_INIT

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    connexion_avec_serveur.connect((HOTE, PORT))
except :
    print("Désolé, il n'y a aucun serveur lancé")
    exit(0)

numID=connexion_avec_serveur.getsockname()[1]
print("Vous êtes connectés avec le serveur labyrinthe sur le port " + str((PORT)) + " et votre ID est " + str(numID))

nomJoueur=input("Votre nom : ")
nomJoueurTmp="[NOM]"+nomJoueur
msg_a_envoyer = nomJoueurTmp.encode()
connexion_avec_serveur.send(msg_a_envoyer)

EtatCommunication="PASSIF"
ordreRecu=False
print("En attente des autres joueurs")

numJoueur="XXXXX"

CoupsMutiples=["",int(0)] # Pour se souvenir des coups multiples (buffer)

partieTerminee=False
while msg_a_envoyer != b"fin" and partieTerminee==False :
    if EtatCommunication=="ACTIF" :
        # Je suis en ACTIF, je peux donc envoyer
        ordreOk=False
        while ordreOk==False :

            flush_input() # je vide le cache

            if CoupsMutiples[1]<=int(0) :
                msg_a_envoyer = input(nomJoueur + " [Robot " + str(numJoueur) + "] (Nombre de vies "+ str(nbVie) + "), at your command (? pour l'aide) : ")
                if msg_a_envoyer=="?" :
                    print("Vous pouvez vous déplacer au nord (N), au sud (S), à l'est (E) et à l'ouest (O)")
                    print("Pour vous déplacer au nord sur une seule case : N ou N1 (pour les autres directions : S, E et O")
                    print("Pour vous déplacer au nord sur 3 cases : N3 (pour les autres directions : S3, E3 et O3)")
                    print("Pour murer une porte sur la case au sud (juste à proximité) : mS (pour les autres directions : mE,mN et mO)")
                    print("Pour percer une porte sur la case au sud (juste à proximité) : pS (pour les autres directions : pE,pN et pO)")
                    print("Si vous souhaitez abandonner : A")
                    print("A chaque choc contre un obstacle (mur, joueur, porte fermé, vous perdez un point de vie")
                else :
                    if msg_a_envoyer=="fin" :
                        ordreOk=True
                    else :
                        if choixValide(msg_a_envoyer) :
                            ordreOk=True
                            if len(msg_a_envoyer)>1 :
                                # Coups multiple
                                CoupsMutiples[0]=sensJoue(msg_a_envoyer)
                                CoupsMutiples[1]=nbCoupsJoue(msg_a_envoyer)-1
                                msg_a_envoyer=sensJoue(msg_a_envoyer)
                        else :
                            print("Coup incorrect, consultez l'aide pour plus de précisions (? pour l'aide)")
            else :
                print("Il y a des coups multiples en stock " + str(CoupsMutiples[0]) + str(CoupsMutiples[1]) + " => déplacement automatique")
                msg_a_envoyer=CoupsMutiples[0]
                CoupsMutiples[1]=CoupsMutiples[1]-1
                ordreOk=True

        msg_a_envoyer = msg_a_envoyer.encode()
        # Peut planter si vous tapez des caractères spéciaux
        try :
            # On envoie le message
            connexion_avec_serveur.send(msg_a_envoyer)
        except :
            print("probleme")
        EtatCommunication="PASSIF"

    if EtatCommunication=="PASSIF" :
        # Je suis en PASSIF , j'affiche tout ce que je reçois sans me poser de question
        try :
            msg_recu = connexion_avec_serveur.recv(1024)
        except :
            print("pb")
        message=msg_recu.decode()
        if message=="[ACTIF]" :
            tour=True
            ordreRecu=True
            EtatCommunication="ACTIF"
        else :
            if message=="[PASSIF]" :
                EtatCommunication="PASSIF"
            else :
                if message[:5]=="[MSG]" :
                    print(message[5:])
                else :
                    if message[:7]=="[GAGNE]" :
                        partieTerminee=True
                        print(message[7:])
                    else :
                        if message[:9]=="[DOSSARD]" :
                            numJoueur=message[9:]
                            print("Vous êtes le robot numero " + message[9:])
                        else :
                            if message[:5]=="[FIN]" :
                                partieTerminee=True
                                print("Tout le monde est mort")
                            else :
                                if message[:5]=="[VIE]" :
                                    nbVie=int(message[5:])
                                    if nbVie>0 :
                                        print("Vous avez " + str(nbVie) +  " vies " )
                                    else :
                                        print("Il semble que vous n'ayez plus de vie ...(GAME OVER)")
                                        print("En attente de la fin de partie (vous pouvez suivre la partie, mais sans jouer")
                                else :
                                    print(message)

print("Fermeture de la connexion")
connexion_avec_serveur.close()
