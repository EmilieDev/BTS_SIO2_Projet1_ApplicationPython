import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
)
from ConnexionBdd import Database
from Accueil import FenetreAccueil

class PageConnexionCompte(QWidget):
    def __init__(self, db): #Initialise l'objet. Super() permet de sortir de la fonction
        super().__init__() # appelle le constructeur de la classe QWidget pour initialiser la fenêtre, c'est similaire à QWidget.__init__(self) sauf que c'est mieux pour l'héritage multiple
        self.db = db #On passe la bdd ici
        self.setWindowTitle("Connexion a un compte")
        self.setGeometry(500, 200, 400, 300)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Connexion à un compte") #Titre
        layout.addWidget(self.label) #Ajoute le label au layout principal créé au dessus

        self.text_input_saisi_username = QLineEdit() #Création du champ de saisi pour l'username
        self.text_input_saisi_username.setPlaceholderText("Nom d'utilisateur") #Affichage d'un text en gris si vide
        layout.addWidget(self.text_input_saisi_username) #Ajoute au layout principal

        #Pour le mdp:
        self.text_input_saisi_password = QLineEdit()
        self.text_input_saisi_password.setPlaceholderText("Mot de passe")
        self.text_input_saisi_password.setEchoMode(QLineEdit.Password) #Cache le mdp avec des *
        layout.addWidget(self.text_input_saisi_password)

        #Creation du bouton de connexion
        self.button_connexion = QPushButton("Se connecter")
        self.button_connexion.clicked.connect(self.connexion) #Quand bouton cliqué, on appelle la fonction connexion()
        layout.addWidget(self.button_connexion)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre

    def connexion(self):
        username = self.text_input_saisi_username.text().strip()
        #self.text_input_saisi_username.text() récupère le texte contenu dans le champ de texte
        #.strip() retire les espaces au début et à la fin du texte
        password = self.text_input_saisi_password.text()

        if not username or not password: #si l'username our le mdp sont vides:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.") #Message d'erreur apparaît
            return

        try:
            #Vérifie si nom d'utilisateur déjà existant
            result = self.db.query("SELECT motDePasse FROM Utilisateurs WHERE nomUtilisateur = %s", (username,)) #Récupère le mdp associé au nom
            if not result: #S'il n'y a pas de résultat (pas d'utilisateurs qui ont ce login)
                QMessageBox.warning(self, "Erreur", "Utilisateur introuvable.")
                return
            
            mdp_bdd = result[0]['motDePasse'] #Récupère le mdp du premier enregistrement (normalement le seul enregistrement car on vérifie lors de la création d'un compte que le nom d'utilisateur n'est pas déjà utilisé)
            if password != mdp_bdd:
                QMessageBox.warning(self, "Erreur", "Mot de passe incorrect.")
                return

            #Si login correct
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.fen_pageAccueil = FenetreAccueil()
            self.fen_pageAccueil.show()
            self.close() #Ferme la fenêtre de connexion

        except Exception as e: 
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")




    def closeEvent(self, event): #Méthode typique dans PyQt qui est appelée automatiquement lors de la fermeture de la fenêtre, elle ferme la connexion à la bdd
        self.db.close() #Ferme la connexion MySQL en exécutant le code de la classe Database (la méthode close())
        event.accept() #Confirme a PyQt la fermeture de la fenêtre

#Pour tester le programme
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
    app = QApplication(sys.argv) #QApplication est l'objet principal de PyQt qui gère tous les évenements (clics, entrées clavier,...)
    #sys.argv permet de passer des arguments à PyQT depuis la ligne de commande (ces arguments sont passés par sys.argv automatiquement, ce sont des arguments comme des options de debugging, des styles de l'application,...)
    fen = PageConnexionCompte(db) #Création d'une instance
    fen.show()
    sys.exit(app.exec()) #Quitte le programme proprement après la fermeture de la fenêtre
