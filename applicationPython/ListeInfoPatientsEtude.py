import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QDialog, QHeaderView
)
from PyQt5.QtCore import QDate
from ConnexionBdd import Database

class PageAjoutEtude(QWidget):
    def __init__(self, db): #Initialise l'objet
        super().__init__() # appelle le constructeur de la classe QWidget pour initialiser la fenêtre, c'est similaire à QWidget.__init__(self) sauf que c'est mieux pour l'héritage multiple
        self.db = db  # Ajout de la base de données
        self.setWindowTitle("Voir liste des patients d'une étude")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Affichage de la liste des patients d'une étude:") #Titre
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




        #Creation du bouton de validation de modification
        self.button_afficher_liste_patients = QPushButton("Afficher")
        self.button_afficher_liste_patients.clicked.connect(self.liste_patients) #Quand bouton cliqué, on appelle la fonction modifier_etat_inclusion
        layout.addWidget(self.button_afficher_liste_patients)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre



    #Fonction se lance quand clique sur bouton Valider
    def liste_patients(self):

        #Pour les listes déroulantes:
        idEtude = self.EtudeComboBox.currentData() #récupère l'id


        #Vérifie que les listes ne sont pas vides
        if idEtude is None :
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une étude.")
            return

        #Si respecte tous ces if :
        try:
            self.db.cursor.execute( #On ajoute lla nouvelle étude
                "SELECT Patients.numDossierClinique, Patients.nomPat, Patients.prenomPat, Patients.dateNaisPat, Patients.sexe, Maladies.nomMaladie, Stades.nomStade FROM DetailEtude JOIN Patients ON Patients.id = DetailEtude.idPatient JOIN Maladies ON Maladies.id = DetailEtude.idMaladie JOIN Patients_Maladies ON Patients_Maladies.idPatient = Patients.id AND Patients_Maladies.idMaladie = DetailEtude.idMaladie JOIN Stades ON Stades.id = Patients_Maladies.idStade WHERE DetailEtude.idEtude = %s", (idEtude,)
            )
            result = self.db.cursor.fetchall()
            if not result: #Pas d'enregistrement trouvé donc pas de patient dans cette étude
                QMessageBox.information(self, "Information", "Aucun patient trouvé pour cette étude.")
                return
            
            tableau = TableauPatients(result) #Appelle la fonction TableauPatients avec les enregistrements stockés dans result
            tableau.exec_()
            
        except Exception as e: #Permet de detecter les erreurs du try et de les définir
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    


    def closeEvent(self, event): #Méthode typique dans PyQt qui est appelée automatiquement lors de la fermeture de la fenêtre, elle ferme la connexion à la bdd
        self.db.close() #Ferme la connexion MySQL en exécutant le code de la classe Database (la méthode close())
        event.accept() #Confirme a PyQt la fermeture de la fenêtre



class TableauPatients(QDialog): #QDialog permet d'ouvrir une autre fenêtre indépendante
    def __init__(self, result): #date est la liste des enregistrements retournés
        super().__init__() #Initalise la fenêtre indépendante
        self.setWindowTitle("Liste des patients")
        self.setGeometry(600, 250, 800, 400)

        layout = QVBoxLayout() ##Le layout principal, tout sera créé dessus


        #Création du tableau
        self.tableau = QTableWidget() #QTableWidget créer un tableau
        self.tableau.setColumnCount(7)
        self.tableau.setHorizontalHeaderLabels([ #Titres horizontaux (colonnes)
            "Numéro dossier",
            "Nom",
            "Prénom",
            "Date de naissance",
            "Sexe",
            "Maladie",
            "Stade"
        ])

        self.tableau.setRowCount(len(result)) #Définit le nombre de lignes du tableau en fonction du nombre d'enregistrements

        #Ajout des enregistrementsdans le tableau
        for index_ligne, patient in enumerate(result): #enumerate parcourt la liste en récupérant l'index de chaque élément
            self.tableau.setItem(index_ligne, 0, QTableWidgetItem(str(patient["numDossierClinique"]))) #QTableWidgetItem est la cellule à insèrer dans le tableau
            self.tableau.setItem(index_ligne, 1, QTableWidgetItem(patient["nomPat"]))
            self.tableau.setItem(index_ligne, 2, QTableWidgetItem(patient["prenomPat"]))
            self.tableau.setItem(index_ligne, 3, QTableWidgetItem(str(patient["dateNaisPat"])))
            self.tableau.setItem(index_ligne, 4, QTableWidgetItem(patient["sexe"]))
            self.tableau.setItem(index_ligne, 5, QTableWidgetItem(patient["nomMaladie"]))
            self.tableau.setItem(index_ligne, 6, QTableWidgetItem(patient["nomStade"]))
            #Il faut forcer le type car QTableWidgetItem attend un str

        layout.addWidget(self.tableau) #Ajoute le label au layout principal créé au dessus (en début de fonction)
        self.setLayout(layout) #Applique le layout à la fenêtre

        #Ajuster la taille des colonnes
        titres_colonnes = self.tableau.horizontalHeader() #Récupère la ligne des titres des colonnes
        titres_colonnes.setSectionResizeMode(QHeaderView.Stretch) #QHeaderView  gère l'apparence des en-tête de colonne
        #setSectionResizeMode est un méthode qui permet de définir comment les colonnes changer de taille (peut être fixe, modifiable avec souris,...)
        #Cette méthode est utilisé avec QHeaderView.Stretch qui répartit automatiquement la largeur des colonnes


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

