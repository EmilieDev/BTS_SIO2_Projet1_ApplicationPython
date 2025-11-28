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
        self.setWindowTitle("Ajouter une étude")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout() #Le layout principal, tout sera créé dessus

        self.label = QLabel("Ajout d'une nouvelle étude :") #Titre
        layout.addWidget(self.label) #Ajoute le label au layout principal créé au dessus

        self.text_input_saisi_nom_etude = QLineEdit() #Création du champ de saisi pour nom d'étude
        self.text_input_saisi_nom_etude.setPlaceholderText("Nom ") #Affichage d'un text en gris si vide
        layout.addWidget(self.text_input_saisi_nom_etude) #Ajoute au layout principal

        self.text_input_saisi_description_etude = QLineEdit()
        self.text_input_saisi_description_etude.setPlaceholderText("Description ")
        layout.addWidget(self.text_input_saisi_description_etude)


        #LISTES DEROULANTES:
        #Protocole
        #Petit texte avant les listes
        self.protocole_label = QLabel("Protocole :")
        layout.addWidget(self.protocole_label)
        #Création de la liste déroulante pour les protocoles des études(vide pour l'instant)
        self.protocoleEtudeComboBox = QComboBox()
        layout.addWidget(self.protocoleEtudeComboBox)
        #Ajout dans la liste chaque protocole via la bdd
        try:
            result = self.db.query("SELECT id, libelleProtocole FROM Protocole")
            for row in result:
                self.protocoleEtudeComboBox.addItem(row['libelleProtocole'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les types d'études : {e}")


        #Type étude
        #Petit texte avant les listes
        self.type_label = QLabel("Type :")
        layout.addWidget(self.type_label)
        #Création de la liste déroulante pour les types d'études(vide pour l'instant)
        self.typeEtudeComboBox = QComboBox()
        layout.addWidget(self.typeEtudeComboBox)
        #Ajout dans la liste chaque type via la bdd
        try:
            result = self.db.query("SELECT id, libelleEtu FROM TypeEtudes")
            for row in result:
                self.typeEtudeComboBox.addItem(row['libelleEtu'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les types d'études : {e}")

        #Organisme
        #Petit texte avant les listes
        self.organisme_label = QLabel("Organisme :")
        layout.addWidget(self.organisme_label)
        #Création de la liste déroulante pour les organismes associés aux études (vide pour l'instant)
        self.organismeEtudeComboBox = QComboBox()
        layout.addWidget(self.organismeEtudeComboBox)
        #Ajout dans la liste chaque organismes via la bdd
        try:
            result = self.db.query("SELECT id, nomOrg FROM Organismes")
            for row in result:
                self.organismeEtudeComboBox.addItem(row['nomOrg'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les organismes des études : {e}")

        #Médecins référents
        #Petit texte avant les listes
        self.med_responsable_label = QLabel("Médecin responsable :")
        layout.addWidget(self.med_responsable_label)
        #Création de la liste déroulante pour les id des médecins référents(vide pour l'instant)
        self.medReferentsComboBox = QComboBox()
        layout.addWidget(self.medReferentsComboBox)
        #Ajout dans la liste chaque medecins référents via la bdd
        try:
            result = self.db.query("SELECT id, nomSoignant FROM Personnel WHERE idRole=2") #l'idRole=2 correspond au médecins référents
            for row in result:
                self.medReferentsComboBox.addItem(row['nomSoignant'], row['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les medecins référents : {e}")

        #Calendriers pour Date début et Date fin
        #Date début
        self.date_debut_label = QLabel("Date début :")
        layout.addWidget(self.date_debut_label)
        self.date_debut = QDateEdit()
        self.date_debut.setCalendarPopup(True) #Affiche le calendrier
        self.date_debut.setDate(QDate.currentDate()) #QDate.currentDate renvoit la date actuelle,
        #avec setDate ça permet de mettre par défaut la date actuelle dans le champ de saisie
        layout.addWidget(self.date_debut)

        #Date fin
        self.date_fin_label = QLabel("Date fin :")
        layout.addWidget(self.date_fin_label)
        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        layout.addWidget(self.date_fin)


        #Creation du bouton de création d'étude
        self.button_creation_etude = QPushButton("Ajouter")
        self.button_creation_etude.clicked.connect(self.creation_etude) #Quand bouton cliqué, on appelle la fonction creation_etude
        layout.addWidget(self.button_creation_etude)

        self.setLayout(layout) #Attribut le rôle de layout principal afin que les widgets ajoutés à layout soient affichés dans la fenêtre



    #Fonction se lance quand clique sur bouton Valider
    def creation_etude(self):
        nomEtude = self.text_input_saisi_nom_etude.text().strip()
        #self.text_input_saisi_nom_etude() récupère le texte contenu dans le champ de texte
        #.strip() retire les espaces au début et à la fin du texte
        descriptionEtude = self.text_input_saisi_description_etude.text()

        #Pour les listes déroulantes:
        idTypeEtude = self.typeEtudeComboBox.currentData() #récupère l'id
        idOrganismeEtude = self.organismeEtudeComboBox.currentData()
        idMedResponsable = self.medReferentsComboBox.currentData()
        idProtocoleEtude = self.protocoleEtudeComboBox.currentData()

        #Pour les dates des calendriers
        dateDebut = self.date_debut.date().toString("yyyy-MM-dd") #Converti la date en str + avec un type de format (format attendu par MySQL)
        dateFin = self.date_fin.date().toString("yyyy-MM-dd")


        #Conditions a respecter pour créer une étude
        if not nomEtude or not descriptionEtude: #si le nom ou la description sont vides:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.") #Message d'erreur apparaît
            return


        #Si respecte tous ces if :
        try:
            #Vérifie si l'étude déjà existante
            result = self.db.query("SELECT COUNT(*) AS nb FROM Etudes WHERE nomEtu = %s", (nomEtude,))
            if result[0]['nb'] > 0: #S'il y a au moin sun resultat, cela signifie qu'il existe déjà un compte avec ce nom d'utilisateur
                QMessageBox.warning(self, "Erreur", "Cette étude existe déjà.")
                return

            self.db.cursor.execute( #On ajoute lla nouvelle étude
                "INSERT INTO Etudes (nomEtu, descEtude, idTypeEtude, idOrganisme, dateDebEtu, dateFinEtu, idMedResponsable, idProtocole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nomEtude, descriptionEtude, idTypeEtude, idOrganismeEtude, dateDebut, dateFin, idMedResponsable, idProtocoleEtude)
            )
            self.db.conn.commit() #Enregistre dans la bdd l'insertion
            QMessageBox.information(self, "Succès ", "Etude créée avec succès !")

            #Efface le contenu des champs de saisi
            self.text_input_saisi_nom_etude.clear()
            self.text_input_saisi_description_etude.clear()
            self.date_debut.setDate(QDate.currentDate())#Pour remettre la date par défaut dans champ de saisie après l'ajout
            self.date_fin.setDate(QDate.currentDate())

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
