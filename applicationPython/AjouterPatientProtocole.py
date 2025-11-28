import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, QComboBox, QDateEdit
)
from PyQt5.QtCore import QDate
from ConnexionBdd import Database

class PageAjoutEtude(QWidget):
    def __init__(self, db): #Initialise l'objet
        super().__init__() # appelle le constructeur de la classe QWidget pour initialiser la fenêtre, c'est similaire à QWidget.__init__(self) sauf que c'est mieux pour l'héritage multiple
        self.db = db  # Ajout de la base de données
        self.setWindowTitle("Ajouter un patient dans un protocole")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Ajout d'un patient dans un protocole:") #Titre
        layout.addWidget(self.label) #Ajoute le label au layout principal créé au dessus

        #LISTES DEROULANTES:
        #Etude
        #Petit texte avant les listes
        self.etude_label = QLabel("Etude :")
        layout.addWidget(self.etude_label)
        #Création de la liste déroulante pour les études(vide pour l'instant)
        self.EtudeComboBox = QComboBox()
        layout.addWidget(self.EtudeComboBox)
        #Ajout dans la liste chaque étude via la bdd
        try:
            result = self.db.query("SELECT id, nomEtu FROM Etudes")
            for row in result:
                self.EtudeComboBox.addItem(row['nomEtu'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les d'études : {e}")


        #Patient
        #Petit texte avant les listes
        self.patient_label = QLabel("Patient :")
        layout.addWidget(self.patient_label)
        #Création de la liste déroulante pour les patients(vide pour l'instant)
        self.patientComboBox = QComboBox()
        layout.addWidget(self.patientComboBox)
        #Ajout dans la liste chaque patient via la bdd
        try:
            result = self.db.query("SELECT id, numDossierClinique FROM Patients")
            for row in result:
                self.patientComboBox.addItem(row['numDossierClinique'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les patients : {e}")

        #Maladie
        #Petit texte avant les listes
        self.maladie_label = QLabel("Maladie :")
        layout.addWidget(self.maladie_label)
        #Création de la liste déroulante pour les maladies (vide pour l'instant)
        self.maladieComboBox = QComboBox()
        layout.addWidget(self.maladieComboBox)
        #Ajout dans la liste chaque maladie via la bdd
        try:
            result = self.db.query("SELECT id, nomMaladie FROM Maladies")
            for row in result:
                self.maladieComboBox.addItem(row['nomMaladie'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les maladies : {e}")


        #Creation du bouton d'ajout au protocole
        self.button_ajouter_protocole = QPushButton("Ajouter")
        self.button_ajouter_protocole.clicked.connect(self.ajouter_protocole) #Quand bouton cliqué, on appelle la fonction ajouter_protocole
        layout.addWidget(self.button_ajouter_protocole)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre



    #Fonction se lance quand clique sur bouton Ajouter
    def ajouter_protocole(self):

        #Pour les listes déroulantes:
        idEtude = self.EtudeComboBox.currentData() #récupère l'id
        idPatient = self.patientComboBox.currentData()
        idMaladie = self.maladieComboBox.currentData()

        #Etat inclusion
        idEtatInclusion = 1 #id 1 correspond à "Inclus"

        #Pour date inclusion
        dateInclusion = QDate.currentDate().toString("yyyy-MM-dd") #Converti la date en str + avec un type de format (format attendu par MySQL)


        #Vérifie que les listes ne sont pas vides
        if idEtude is None or idPatient is None or idMaladie is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une étude, un patient et une maladie.")
            return

        #Si respecte tous ces if :
        try:
            #Vérifie que le patient possède bien la maladie
            result = self.db.query("SELECT COUNT(*) AS nb FROM Patients_Maladies WHERE idPatient = %s AND idMaladie = %s", (idPatient, idMaladie))
            if result[0]['nb'] == 0:
                QMessageBox.warning(self, "Erreur","Ce patient n'est pas atteint de cette maladie, impossible d'inclure le patient.")
                return
            
            #Vérifie si le patient est déjà dans cette étude
            result = self.db.query("SELECT COUNT(*) AS nb FROM DetailEtude WHERE idPatient = %s AND idEtude = %s", (idPatient, idEtude))

            if result[0]['nb'] > 0:
                QMessageBox.warning(self, "Erreur", "Ce patient est déjà inscrit dans ce protocole.")
                return


            self.db.cursor.execute( #On ajoute lla nouvelle étude
                "INSERT INTO DetailEtude (idPatient, idEtude, idEtatInclusion, idMaladie, dateInclusion) VALUES (%s, %s, %s, %s, %s)", (idPatient, idEtude, idEtatInclusion, idMaladie, dateInclusion)
            )
            self.db.conn.commit() #Enregistre dans la bdd l'insertion
            QMessageBox.information(self, "Succès ", "Patient ajouté au protocole avec succès !")


        except Exception as e: #Permet de detecter les erreurs du try et de les définir
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")


    def closeEvent(self, event): #Méthode typique dans PyQt qui est appelée automatiquement lors de la fermeture de la fenêtre, elle ferme la connexion à la bdd
        self.db.close() #Ferme la connexion MySQL en exécutant le code de la classe Database (la méthode close())
        event.accept() #Confirme a PyQt la fermeture de la fenêtre

#Pour tester le programme
if __name__ == "__main__":
    try:
        db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
    except Exception as e:
        print("Erreur de connexion :", e)
        sys.exit()
    app = QApplication(sys.argv) #QApplication est l'objet principal de PyQt qui gère tous les évenements (clics, entrées clavier,...)
    #sys.argv permet de passer des arguments à PyQT depuis la ligne de commande (ces arguments sont passés par sys.argv automatiquement, ce sont des arguments comme des options de debugging, des styles de l'application,...)
    fen = PageAjoutEtude(db) #Création d'une instance
    fen.show()
    sys.exit(app.exec_()) #Quitte le programme proprement après la fermeture de la fenêtre
    
    #NE PAS OUBLIER DE : rendre la connexion persistance entre les onglets
