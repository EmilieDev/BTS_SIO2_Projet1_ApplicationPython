import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, QComboBox, QDateEdit, QRadioButton, QGroupBox, QButtonGroup
)
from PyQt5.QtCore import QDate
from ConnexionBdd import Database

class PageAjoutEtude(QWidget):
    def __init__(self, db): #Initialise l'objet
        super().__init__() # appelle le constructeur de la classe QWidget pour initialiser la fenêtre, c'est similaire à QWidget.__init__(self) sauf que c'est mieux pour l'héritage multiple
        self.db = db  # Ajout de la base de données
        self.setWindowTitle("Ajout patient")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Ajout d'un nouveau patient :") #Titre
        layout.addWidget(self.label) #Ajoute le label au layout principal créé au dessus

        self.text_input_saisi_nom_patient = QLineEdit() #Création du champ de saisi pour nom d'étude
        self.text_input_saisi_nom_patient.setPlaceholderText("Nom ") #Affichage d'un text en gris si vide
        layout.addWidget(self.text_input_saisi_nom_patient) #Ajoute au layout principal

        self.text_input_saisi_prenom_patient = QLineEdit()
        self.text_input_saisi_prenom_patient.setPlaceholderText("Prénom ")
        layout.addWidget(self.text_input_saisi_prenom_patient)


        self.sexe_label = QLabel("Sexe :")
        layout.addWidget(self.sexe_label)

        #Boutons sexe:
        sexe_box = QGroupBox() #Création de la boite qui va contenir les boutons
        sexe_layout = QVBoxLayout() #Pour affichage des boutons l'un en dessous de l'autre

        #Création des boutons
        self.radio_feminin = QRadioButton("Féminin")
        self.radio_masculin = QRadioButton("Masculin")

        #Ajout des boutons au layout principal
        sexe_layout.addWidget(self.radio_feminin)
        sexe_layout.addWidget(self.radio_masculin)
        
        #Ajoute les boutons dans la boite
        sexe_box.setLayout(sexe_layout)
        layout.addWidget(sexe_box)

        self.sexe_group = QButtonGroup() #Créer un groupe des deux boutons (permet de dire qu'un seul peut être selectionné)
        self.sexe_group.addButton(self.radio_feminin) #Ajoute les deux boutons au groupe
        self.sexe_group.addButton(self.radio_masculin)


        self.text_input_saisi_num_dossier = QLineEdit()
        self.text_input_saisi_num_dossier.setPlaceholderText("Numéro de dossier: ")
        layout.addWidget(self.text_input_saisi_num_dossier)



        self.date_naissance_label = QLabel("Date de naissance :")
        layout.addWidget(self.date_naissance_label)
        self.date_naissance = QDateEdit()
        self.date_naissance.setCalendarPopup(True)
        self.date_naissance.setDate(QDate.currentDate())
        layout.addWidget(self.date_naissance)


        #Creation du bouton de création d'un patient
        self.button_creation_patient = QPushButton("Ajouter")
        self.button_creation_patient.clicked.connect(self.creation_patient) #Quand bouton cliqué, on appelle la fonction creation_patient
        layout.addWidget(self.button_creation_patient)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre



    #Fonction se lance quand clique sur bouton Valider
    def creation_patient(self):
        nomPatient = self.text_input_saisi_nom_patient.text().strip()
        #self.text_input_saisi_nom_patient() récupère le texte contenu dans le champ de texte
        #.strip() retire les espaces au début et à la fin du texte
        prenomPatient = self.text_input_saisi_prenom_patient.text()
        numDossier = self.text_input_saisi_num_dossier.text()
        
        #Récupération du sexe
        if self.radio_feminin.isChecked():
            sexe = "F"
        elif self.radio_masculin.isChecked():
            sexe = "M"
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un sexe.")
            return
        
        #Pour les dates des calendriers
        dateNaissance = self.date_naissance.date().toString("yyyy-MM-dd") #Converti la date en str + avec un type de format (format attendu par MySQL)

        #Conditions a respecter pour créer une étude
        if not nomPatient or not prenomPatient or not numDossier: #si le nom ou la description sont vides:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.") #Message d'erreur apparaît
            return


        #Si respecte tous ces if :
        try:
            #Vérifie si numéro de dossier déjà existant
            result = self.db.query("SELECT COUNT(*) AS nb FROM Patients WHERE numDossierClinique = %s", (numDossier,))
            if result[0]['nb'] > 0: #S'il y a au moin sun resultat, cela signifie qu'il existe un patient avec ce num de dossier
                QMessageBox.warning(self, "Erreur", "Ce numéro de dossier existe déjà.")
                return

            self.db.cursor.execute( #On ajoute le nouveau patient
                "INSERT INTO Patients (nomPat, prenomPat, dateNaisPat, sexe, numDossierClinique) VALUES (%s, %s, %s, %s, %s)", (nomPatient, prenomPatient, dateNaissance, sexe, numDossier)
            )
            self.db.conn.commit() #Enregistre dans la bdd l'insertion
            QMessageBox.information(self, "Succès ", "Patient créé avec succès !")

            #Efface le contenu des champs de saisi
            self.text_input_saisi_nom_patient.clear()
            self.text_input_saisi_prenom_patient.clear()
            self.date_naissance.setDate(QDate.currentDate())#Pour remettre la date par défaut dans champ de saisie après l'ajout
            self.text_input_saisi_num_dossier.clear()

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
