class Utilisateur:
    def __init__(self, identifiant, nomUtilisateur, motDePasse):
        self.identifiant = identifiant
        self.nomUtilisateur = nomUtilisateur
        self.motDePasse = motDePasse

    def __str__(self):
        return f"{self.nomUtilisateur} {self.motDePasse} (id: {self.identifiant})"