# -*-coding:Utf-8 -*

import unittest

from gestion import choixValide

# Cette classe est un groupe de tests. Son nom DOIT commencer par 'Test' et la classe DOIT hériter de unittest.TestCase.
# Pour l'exercice, je n'ai testé que la fonction "choixValide pour montrer ma compréhension des tests unitaires
# On peut le généraliser autres fonctions sur le même principe

class TestFonctionChoixValide(unittest.TestCase):
    # Chaque méthode dont le nom commence par 'test_' est un test.
    def test_ChoixValideS4(self):
        commande="S4"
        retour = choixValide(commande)
        self.assertEqual(retour, True)

    def test_ChoixValideS44(self):
        commande="S44"
        retour = choixValide(commande)
        self.assertEqual(retour, True)

    def test_ChoixValideN(self):
        commande="N"
        retour = choixValide(commande)
        self.assertEqual(retour, True)

    def test_ChoixValideO1(self):
        commande="O1"
        retour = choixValide(commande)
        self.assertEqual(retour, True)

    def test_ChoixValideS44D(self):
        commande="S44D"
        retour = choixValide(commande)
        self.assertEqual(retour, False)

    def test_ChoixValideG(self):
        commande="G"
        retour = choixValide(commande)
        self.assertEqual(retour, False)

    def test_ChoixValideG4(self):
        commande="G4"
        retour = choixValide(commande)
        self.assertEqual(retour, False)

    def test_ChoixValide4(self):
        commande="4"
        retour = choixValide(commande)
        self.assertEqual(retour, False)

# Ceci lance le test si on exécute le script directement.
if __name__ == '__main__':
    unittest.main()