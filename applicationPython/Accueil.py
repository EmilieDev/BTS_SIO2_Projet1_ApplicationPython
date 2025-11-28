from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class FenetreAccueil(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accueil")
        self.setGeometry(500, 200, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("Bienvenue ! Vous êtes connecté.")
        layout.addWidget(label)

        self.setLayout(layout)