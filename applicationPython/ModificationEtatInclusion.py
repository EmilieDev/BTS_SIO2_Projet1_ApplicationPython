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
        self.setWindowTitle("Modifier état inclusion d'un patient dans un protocole")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Modification de l'état d'inclusion d'un patient dans un protocole:") #Titre
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

        #EtatInclusion
        #Petit texte avant les listes
        self.etat_inclusion_label = QLabel("Etat inclusion :")
        layout.addWidget(self.etat_inclusion_label)
        #Création de la liste déroulante pour les maladies (vide pour l'instant)
        self.etat_inclusionComboBox = QComboBox()
        layout.addWidget(self.etat_inclusionComboBox)
        #Ajout dans la liste chaque maladie via la bdd
        try:
            result = self.db.query("SELECT id, libelleEtat FROM EtatInclusion")
            for row in result:
                self.etat_inclusionComboBox.addItem(row['libelleEtat'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les maladies : {e}")


        #Creation du bouton de validation de modification
        self.button_modifier_etat_inclusion = QPushButton("Valider")
        self.button_modifier_etat_inclusion.clicked.connect(self.modifier_etat_inclusion) #Quand bouton cliqué, on appelle la fonction modifier_etat_inclusion
        layout.addWidget(self.button_modifier_etat_inclusion)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre



    #Fonction se lance quand clique sur bouton Valider
    def modifier_etat_inclusion(self):

        #Pour les listes déroulantes:
        idEtude = self.EtudeComboBox.currentData() #récupère l'id
        idPatient = self.patientComboBox.currentData()
        idEtatInclusion = self.etat_inclusionComboBox.currentData()

        #Vérifie que les listes ne sont pas vides
        if idEtude is None or idPatient is None or idEtatInclusion is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une étude, un patient et un type d'état d'inclusion.")
            return

        #Si respecte tous ces if :
        try:
            #Vérifie que l'état n'a pas déjà cette valeur
            result = self.db.query("SELECT COUNT(*) AS nb FROM DetailEtude WHERE idPatient = %s AND idEtude = %s AND idEtatInclusion = %s", (idPatient, idEtude, idEtatInclusion))
            if result[0]['nb'] != 0:
                QMessageBox.warning(self, "Erreur","L'état d'inclusion du patient a déjà cette valeur.")
                return
            
            #Vérifie si le patient est dans cette étude
            result = self.db.query("SELECT COUNT(*) AS nb FROM DetailEtude WHERE idPatient = %s AND idEtude = %s", (idPatient, idEtude))

            if result[0]['nb'] == 0:
                QMessageBox.warning(self, "Erreur", "Ce patient est n'est pas inscrit dans ce protocole, inscrivez le avant de modifier son état d'inclusion.")
                return


            self.db.cursor.execute( #On ajoute lla nouvelle étude
                "UPDATE DetailEtude SET idEtatInclusion = %s WHERE idPatient = %s AND idEtude = %s", (idEtatInclusion, idPatient, idEtude)
            )
            self.db.conn.commit() #Enregistre dans la bdd l'insertion
            QMessageBox.information(self, "Succès ", " La modification de l'état a été faite avec succès !")


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
