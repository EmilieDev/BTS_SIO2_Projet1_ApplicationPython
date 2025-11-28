from Stades import Stade
class StadesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_stades(self):
        sql = "SELECT * FROM stades"
        rows = self.db.query(sql)
        stades = [Stade(row['id'], row['nomStade']) for row in rows]
        return stades
    
    def insert_stade(self, nomStade):
        sql = "INSERT INTO stades (nomStade) VALUES (%s)" #%s valeur à insérer
        params = (nomStade,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"Le stade '{nomStade}' a bien été inséré.")
    
    def update_stade(self, id, nouveau_nom):
        sql = "UPDATE stades SET nomStade = %s WHERE id = %s"
        params = (nouveau_nom, id)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"Le stade d'id {id} a comme nouveau nom :'{nouveau_nom}'.")

    def delete_stade(self, id):
        sql = "DELETE FROM stades WHERE id = %s"
        params = (id,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"Le stade d'id {id} a été supprimé.")