from Organismes import Organisme
class OrganismesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_organismes(self):
        sql = "SELECT * FROM organismes"
        rows = self.db.query(sql)
        organismes = [Organisme(row['id'], row['nomOrganisme']) for row in rows]
        return organismes
    
    def insert_organisme(self, nomOrganisme):
        sql = "INSERT INTO organismes (nomOrganisme) VALUES (%s)" #%s valeur à insérer
        params = (nomOrganisme,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"L'organisme '{nomOrganisme}' a bien été inséré.")
    
    def update_organisme(self, id, nouveau_nom):
        sql = "UPDATE organismes SET nomOrganisme = %s WHERE id = %s"
        params = (nouveau_nom, id)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'organisme d'id {id} a comme nouveau nom :'{nouveau_nom}'.")

    def delete_organisme(self, id):
        sql = "DELETE FROM organismes WHERE id = %s"
        params = (id,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'organisme d'id {id} a été supprimé.")