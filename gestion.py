# -*-coding:Utf-8 -*

import socket
import select
import os,sys

def lancementServeur(hote,port) :
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur Labyrinthe est lancée sur le port {}\n".format(port))
    return connexion_principale

def nbJoueursAttendu() :
    # Vérification du nombre d'argument : Il faut qu'il y ait 1 argument numerique indiquant le nb de joueurs
    # Exemple de lancement du programme : python serveur.py 2
    if len(sys.argv) != 2 :  # Il doit y avoir 1 parametres plus le nom du programme cela fait 2
        print("Il n'y a pas assez de parametre. Exemple d'utilisation : Python serveur.py 2")
        exit(0)
    nbJoueurs=sys.argv[1]
    try :
        int(nbJoueurs)
    except ValueError :
        print("L'argument doit être numérique")
        exit(0)
    if int(nbJoueurs)==0 :
        exit(0)
    return(nbJoueurs)

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def joueurSuivant(num,max) :
    suivant=num+1
    if suivant>=max :
       # print("le suivant est :0")
        return 0
    else :
       # print("le suivant est " + str(suivant))
        return suivant

def saisieLigneOK(nb,chaine):
    if len(chaine) == int(nb) :
        if formatLigneOK(chaine) :
            return True
        else :
            print("format de la chaine incorrect")
            return False
    else :
        print("Longueur de la chaine incorrecte")
        return False

def formatLigneOK(chaine) :
    for lettre in chaine:
        if not(lettre =="X" or lettre =="O" or lettre =="." or lettre ==" " or lettre =="U") :
            return False
    return True

def choixValide(direction) :
    if len(direction)==0 :
        return False
    else :
        if direction[0]=="N" or direction[0]=="S" or direction[0]=="E" or direction[0]=="O" :
            nbCoupsDirection=direction[1:]
            if len(direction)==1 :
                nbCoupsDirection=1
            else :
                try :
                    int(nbCoupsDirection)
                except ValueError:
                    #print("Lorsque vous souhaitez des coups multiples, il faut saisir une valeur numérique après la direction")
                    return False
            return True
        else :
            return False
    return False

def nbCoupsJoue(direction) :
    if len(direction)==1 :
        return 1
    else :
        return int(direction[1:])

def sensJoue(direction) :
    return(direction[0])

def supprimerFichierCarte(nom) :
    if os.path.exists(nom) == True :
           os.remove(nom)

def saisieNombre(question ) :
    fin=False
    while fin==False :
        nombre=input(question)
        try :
            int(nombre)
            fin=True
            return int(nombre)
        except ValueError:
            print("Il faut saisir une valeur numerique entière")

