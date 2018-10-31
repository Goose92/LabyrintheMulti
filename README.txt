# LabyrintheMulti
Labyrinthe en multi joueurs

Présentation du jeu
    Ce jeu est développé en Python sur un mode  client / serveur.
    Les joueurs sont les clients et ne peuvent se connecter que si un serveur est lancé.
    Le jeu est développé en python 3, d'où l'importance de le lancer via la commande Python3.
    Le but du jeu est d'être le premier à rejoindre la sortie du labyrinthe (représenté par un 'U').
    Le jeu étant en mode console (texte), on ne peut jouer qu'à 9 joueurs maximum (chacun étant représenté par un chiffre de 1 à 9)

Ouverture du jeu sur de nouvelles fonctionnalités :
    Le jeu étant en objet, il est facile de rajouter la notion d'étage dans les labyrinthe. il faut simplement indiquer qu'un tablea est un tableau de tableau (l'étage étant l'indice).
    On peut envisager assez simplement de rajouter une notion d'attaque : par exmeple, un joueur pour tirer au sud (commande tS). Si un joueur se trouve à découvert dans cette direction, il perd un point de vie.
    Actuellement, le jeu s'arrête à la fin de la partie (les clients et le serveur sont déconnectés). il serait possible de recommencer une partie en modifiant le menu principal.

Lancement du serveur
    Le lancement du serveur via une commande comme ci-dessous :
        python3 serveur.py 2
    Dans cet exemple, le serveur est lancé en attendant 2 joueurs (clients)
    Il aurait été possible de faire à la demande du client (via une commande qu'un client pourrait envoyer.
    Dans un premier temps, le serveur a la possibilité de :
        J - Lancer le jeu
        V - Voir les cartes existantes
        E - Editer les cartes
        Q - Quitter leu jeu
    Lors du lancement du jeu, le serveur doit choisir la carte avec laquelle la partie va se dérouler.
    Puis le serveur préparer la partie et attend la connexion de l'ensemble des joueurs.

Lancement des clients
    Chaque client se connecte en lancant la commande :
        python client.py
    Le joueur se voit alors demandé son nom de joueur.
    Il faut ensuite se laisser guider par le serveur qui va alterner les séquences "passif" (on voit les autres jouer)
    et les séquences actif où l'on doit indiquer son coup à jouer.
    chaque joueur se voit créditer de 100 points de vie. Il perd un point à chaque fois qu'il heurte un obstacle (mur, joueur, porte fermée)
    Lorsqu'il n'a plus de point de vie, il devient spectateur jusqu'à la fin du jeu.
    Sur les cartes, les éléments sont les suivants :
        O : un mur
        U : La sortie qu'il faut rejoindre !
        . : Une porte ouverte (que vous pouvez fermer via la commande mX où X est la direction)
        - : une porte fermée (que vous pouvez ouvrir/percer via la commande pX où X est la direction)
        Les joueurs sont représentés par un chiffre (de 1 à 9).

    Les commandes de jeu sont les suivantes :
        Pour se déplacer d'une case vers le nord : N ou N1
        Pour se déplacer d'un x cases vers le nord : Nx (exemple : N4 pour 4 cases) ==> Après N, il faut donc une valeur numérique (sans espace)
        Vous avez la possibilité de faire de même avec le Sud (S), l'Ouest (O) et l'Est (E)
        A proximité direct d'une porte ouverte ('.'), vous pouvez la fermer/murer avec la commande mS (pour une porte qui se trouve au sud)
        A proximité direct d'une porte fermée ('-'), vous pouvez l'ouvrir/percer avec la commande pS (pour une porte qui se trouve au sud)
        Le joueur a également la possibilité d'abandonner via la commande 'A'


Présentation des fichiers et du code :
    Le code est développé en python 3 (certaines commandes fonctionnent mieux ainsi) et en objet.
    le jeu est décomposé en plusieurs objets :
        Plateau : qui est composé d'objets Cartes et d'un objet Partie
        Carte : Est un objet qui permet de manipuler une carte (labyrinthe) et possède un nom
        Partie : Est l'objet qui gère la partie en cours et contient : les joueurs, et différents composants.

