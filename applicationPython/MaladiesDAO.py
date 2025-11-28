from Maladies import Maladie
class MaladiesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_maladies(self):
        sql = "SELECT * FROM maladies"
        rows = self.db.query(sql)
        maladies = [Maladie(row['id'], row['nomMaladie']) for row in rows]
        return maladies
    
    def insert_maladie(self, nomMaladie):
        sql = "INSERT INTO maladies (nomMaladie) VALUES (%s)" #%s valeur à insérer
        params = (nomMaladie,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"La maladie'{nomMaladie}' a bien été insérée.")
    
    def update_maladie(self, id, nouveau_nom):
        sql = "UPDATE maladies SET nomMaladie = %s WHERE id = %s"
        params = (nouveau_nom, id)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"La maladie d'id {id} a comme nouveau nom :'{nouveau_nom}'.")

    def delete_maladie(self, id):
        sql = "DELETE FROM maladies WHERE id = %s"
        params = (id,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"La maladie d'id {id} a été supprimé.")