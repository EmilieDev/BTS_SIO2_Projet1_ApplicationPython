import re
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
)
from ConnexionBdd import Database

def mot_de_passe_valide(password: str):
    if len(password) < 12:
        return False, "Le mot de passe doit être composé d au moins 12 caractères."
    if not re.search("[A-Z]", password):
        return False, "Le mot de passe doit avoir au moins une majuscule."
    if not re.search("[a-z]", password):
        return False, "Le mot de passe doit avoir au moins une minuscule."
    if not re.search("[0-9]", password):
        return False, "Le mot de passe doit avoir au moins un chiffre."
    if not re.search("[<>!§:/;.,?%^$*&}{#~|@()]", password):
        return False, "Le mot de passe doit avoir au moins un caractère spécial."
    return True, "Mot de passe valide."

class PageCreationCompte(QWidget):
    def __init__(self, db): #Initialise l'objet
        super().__init__() # appelle le constructeur de la classe QWidget pour initialiser la fenêtre, c'est similaire à QWidget.__init__(self) sauf que c'est mieux pour l'héritage multiple
        self.db = db
        self.setWindowTitle("Création d'un compte")
        self.setGeometry(500, 200, 400, 300)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Créer un nouveau compte") #Titre
        layout.addWidget(self.label) #Ajoute le label au layout principal créé au dessus

        self.text_input_saisi_username = QLineEdit() #Création du champ de saisi pour l'username
        self.text_input_saisi_username.setPlaceholderText("Nom d'utilisateur") #Affichage d'un text en gris si vide
        layout.addWidget(self.text_input_saisi_username) #Ajoute au layout principal

        #On fait pareil avec le mdp (2x car il faut aussi le confirmer une deuxième fois):
        self.text_input_saisi_password = QLineEdit()
        self.text_input_saisi_password.setPlaceholderText("Mot de passe")
        self.text_input_saisi_password.setEchoMode(QLineEdit.Password) #Cache le mdp avec des *
        layout.addWidget(self.text_input_saisi_password)

        self.text_input_saisi_password_confirme = QLineEdit()
        self.text_input_saisi_password_confirme.setPlaceholderText("Confirmez le mot de passe")
        self.text_input_saisi_password_confirme.setEchoMode(QLineEdit.Password) #Cache le mdp avec des *
        layout.addWidget(self.text_input_saisi_password_confirme)

        #Creation du bouton de création du compte
        self.button_creation_compte = QPushButton("Créer le compte")
        self.button_creation_compte.clicked.connect(self.creation_compte) #Quand bouton cliqué, on appelle la fonction creation_compte
        layout.addWidget(self.button_creation_compte)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre


    def creation_compte(self):
        username = self.text_input_saisi_username.text().strip()
        #self.text_input_saisi_username() récupère le texte contenu dans le champ de texte
        #.strip() retitre les espaces au début et à la fin du texte
        password = self.text_input_saisi_password.text()
        confirm = self.text_input_saisi_password_confirme.text()

        #Vérification de l'utilisateur et du mot de passe s'ils sont conformes pour être créés
        if not username or not password: #si l'username our le mdp sont vides:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.") #Message d'erreur apparaît
            return
        if password != confirm : #mdp différent de la confirmation du mdp
            QMessageBox.warning(self, "Erreur", "Vous avez saisis 2 mots de passe différents.")
            return

        valide, message = mot_de_passe_valide(password) #Appelle la foncton avec le mdp entré
        #valide va stocké True ou False si le mdp respecte les rêgles imposées
        #message va stocker un message explicatif
        if valide == False:
            QMessageBox.warning(self, "Mot de passe invalide : ", message)
            return

        #Si le mdp respecte tous ces if :
        try:
            #Vérifie si nom d'utilisateur déjà existant
            result = self.db.query("SELECT COUNT(*) AS nb FROM Utilisateurs WHERE nomUtilisateur = %s", (username,))
            if result[0]['nb'] > 0: #S'il y a au moin sun resultat, cela signifie qu'il existe déjà un compte avec ce nom d'utilisateur
                QMessageBox.warning(self, "Erreur", "Ce nom d'utilisateur existe déjà.")
                return

            self.db.cursor.execute( #On ajoute le nouvel utilisateur (j'ai créé la table utilisateurs)
                "INSERT INTO Utilisateurs (nomUtilisateur, motDePasse) VALUES (%s, %s)", (username, password)
            )
            self.db.conn.commit() #Enregistre dans la bdd l'insertion
            QMessageBox.information(self, "Succès ", "Compte créé avec succès !")

            #Efface le contenu des champs de saisi
            self.text_input_saisi_username.clear()
            self.text_input_saisi_password.clear()
            self.text_input_saisi_password_confirme.clear()

        except Exception as e: #Permet de detecter les erreurs du try et de les définir
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def closeEvent(self, event): #Méthode typique dans PyQt qui est appelée automatiquement lors de la fermeture de la fenêtre, elle ferme la connexion à la bdd
        self.db.close() #Ferme la connexion MySQL en exécutant le code de la classe Database (la méthode close())
        event.accept() #Confirme a PyQt la fermeture de la fenêtre


if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
    app = QApplication(sys.argv) #QApplication est l'objet principal de PyQt qui gère tous les évenements (clics, entrées clavier,...)
    #sys.argv permet de passer des arguments à PyQT depuis la ligne de commande (ces arguments sont passés par sys.argv automatiquement, ce sont des arguments comme des options de debugging, des styles de l'application,...)
    fen = PageCreationCompte(db) #Création d'une instance
    fen.show()
    sys.exit(app.exec()) #Quitte le programme proprement après la fermeture de la fenêtre