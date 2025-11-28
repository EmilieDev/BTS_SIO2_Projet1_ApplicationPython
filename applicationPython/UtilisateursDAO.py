from Utilisateurs import Utilisateur
class UtilisateursDAO:
    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self):
        sql = "SELECT * FROM Utilisateurs"
        rows = self.db.query(sql)
        utilisateurs = [Utilisateur(row['identifiant'], row['nomUtilisateur'], row['motDePasse']) for row in rows]
        return utilisateurs
    
    def insert_utilisateur(self, username, password):
        sql = "INSERT INTO Utilisateurs (nomUtilisateur, motDePasse) VALUES (%s, %s)" #%s valeur à insérer
        params = (username, password,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"L'utilisateur' '{username} {password}' a bien été inséré.")
    
    def update_utilisateur(self, identifiant, nouvel_username, nouveau_mdp):
        sql = "UPDATE Utilisateurs SET nomUtilisateur = %s, motDePasse = %s WHERE identifiant = %s"
        params = (nouvel_username, nouveau_mdp, identifiant)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'utilisateur' d'id {identifiant} a comme nouveau username et mot de passe :'{nouvel_username} {nouveau_mdp}'.")

    def delete_utilisateur(self, identifiant):
        sql = "DELETE FROM Utilisateurs WHERE identifiant = %s"
        params = (identifiant,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'utilisateur d'id {identifiant} a été supprimé.")