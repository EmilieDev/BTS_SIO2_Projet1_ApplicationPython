from Specialites import Specialite
class SpecialitesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_specialites(self):
        sql = "SELECT * FROM specialites"
        rows = self.db.query(sql)
        specialites = [Specialite(row['id'], row['nomSpecialite']) for row in rows]
        return specialites
    
    def insert_specialite(self, nomSpecialite):
        sql = "INSERT INTO specialites (nomSpecialite) VALUES (%s)" #%s valeur à insérer
        params = (nomSpecialite,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"La spécialité '{nomSpecialite}' a bien été insérée.")
    
    def update_specialite(self, id, nouveau_nom):
        sql = "UPDATE specialites SET nomSpecialite = %s WHERE id = %s"
        params = (nouveau_nom, id)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"La spécialité d'id {id} a comme nouveau nom :'{nouveau_nom}'.")

    def delete_specialite(self, id):
        sql = "DELETE FROM specialites WHERE id = %s"
        params = (id,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"La spécialité d'id {id} a été supprimée.")