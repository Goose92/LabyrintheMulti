# -*-coding:Utf-8 -*


import socket,string
from gestion import flush_input,choixValide

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    connexion_avec_serveur.connect((hote, port))
except :
    print("Désolé, il n'y a aucun serveur lancé")
    exit(0)

numID=connexion_avec_serveur.getsockname()[1]
print("Vous êtes connectés avec le serveur labyrinthe sur le port " + str((port)) + " et votre ID est " + str(numID))

nomJoueur=input("Votre nom : ")
nomJoueurTmp="[NOM]"+nomJoueur
msg_a_envoyer = nomJoueurTmp.encode()
connexion_avec_serveur.send(msg_a_envoyer)

EtatCommunication="PASSIF"
ordreRecu=False
print("En attente des autres joueurs")

numJoueur="XXXXX"
partieTerminee=False
while msg_a_envoyer != b"fin" and partieTerminee==False :
    if EtatCommunication=="ACTIF" :
        # Je suis en ACTIF, je peux donc envoyer
        ordreOk=False
        while ordreOk==False :
            flush_input() # je vide le cache
            msg_a_envoyer = input(nomJoueur + " (Robot "+ str(numJoueur) + "), at your command (? pour help) : ")
            if msg_a_envoyer=="?" :
                print("utilisez les cardinaux et un nombre")
            else :
                if msg_a_envoyer=="fin" :
                    ordreOk=True
                else :
                    if choixValide(msg_a_envoyer) :
                        ordreOk=True
                    else :
                        print("Format incorrect, utilisez .....")

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
                            print(message)

print("Fermeture de la connexion")
connexion_avec_serveur.close()
