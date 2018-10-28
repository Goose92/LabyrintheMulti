# -*-coding:Utf-8 -*


import socket,string
from gestion import flush_input

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
numID=connexion_avec_serveur.getsockname()[1]
print("Vous êtes connectés avec le serveur labyrinthe sur le port " + str((port)) + " et votre ID est " + str(numID))

nomJoueur=input("Votre nom : ")
nomJoueur="[NOM]"+nomJoueur
msg_a_envoyer = nomJoueur.encode()
connexion_avec_serveur.send(msg_a_envoyer)

EtatCommunication="PASSIF"
ordreRecu=False
print("En attente des autres joueurs")

while msg_a_envoyer != b"fin":
    if EtatCommunication=="ACTIF" :
        #print("Je suis en ACTIF, je peux donc envoyer")
        flush_input() # je vide le cache
        msg_a_envoyer = input(nomJoueur + " ("+ str(numID) + ") : ")
        msg_a_envoyer = msg_a_envoyer.encode()
        # Peut planter si vous tapez des caractères spéciaux
        try :
            # On envoie le message
            connexion_avec_serveur.send(msg_a_envoyer)
        except :
            print("probleme")
        EtatCommunication="PASSIF"

    if EtatCommunication=="PASSIF" :
        #print("Je suis en PASSIF , j'affiche tout ce que je reçois sans me poser de question")
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
                    print("La carte ....." + message)

print("Fermeture de la connexion")
connexion_avec_serveur.close()
