from Organes import Organe
class OrganesDAO:
    def __init__(self, db):
        self.db = db

    def get_all_organes(self):
        sql = "SELECT * FROM organes"
        rows = self.db.query(sql)
        organes = [Organe(row['id'], row['nomOrgane']) for row in rows]
        return organes
    
    def insert_organe(self, nomOrgane):
        sql = "INSERT INTO organes (nomOrgane) VALUES (%s)" #%s valeur à insérer
        params = (nomOrgane,) #Paramètre a ajouter, on le fait séparément pour éviter les injections SQL
        self.db.cursor.execute(sql, params)
        self.db.conn.commit() #Important car on modifie la bdd
        print(f"L'organe'{nomOrgane}' a bien été inséré.")
    
    def update_organe(self, id, nouveau_nom):
        sql = "UPDATE organes SET nomOrgane = %s WHERE id = %s"
        params = (nouveau_nom, id)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'organe d'id {id} a comme nouveau nom :'{nouveau_nom}'.")

    def delete_organe(self, id):
        sql = "DELETE FROM organes WHERE id = %s"
        params = (id,)
        self.db.cursor.execute(sql, params)
        self.db.conn.commit()
        print(f"L'organe d'id {id} a été supprimé.")