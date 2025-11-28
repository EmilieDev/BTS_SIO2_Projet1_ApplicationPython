import sys
import mysql.connector
from ConnexionBdd import Database

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QVBoxLayout, QLabel, QLineEdit

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("affichage liste")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        #Bouton
        self.bouton_connexion = QPushButton("afficher listes")
        self.bouton_connexion.clicked.connect(self.appui_bouton_connexion)

        #Conteneur pour les labels ajoutés
        self.labels_container = QVBoxLayout()
        self.layout.addLayout(self.labels_container)

        self.setLayout(self.layout)
        self.layout.addWidget(self.bouton_connexion)


    def appui_bouton_connexion(self):
        print("test")
        
        self.conn = mysql.connector.connect(user="grp05Admin", password="grp05Mdp", host="172.27.0.50", port=3306, database="grp05ClinPasteur")
        query = ("show tables")

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()
app.exec_()
