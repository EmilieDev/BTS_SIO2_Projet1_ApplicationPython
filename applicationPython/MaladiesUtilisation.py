from MaladiesDAO import MaladiesDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    maladie_dao = MaladiesDAO(db)
   
    print("Liste des maladies:")
    maladies = maladie_dao.get_all_maladies()
    for s in maladies:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter une maladie:")
    maladie_dao.insert_maladie("test")

    print("Modifier nom d'un stade:")
    maladie_dao.update_maladie(6, "test2")

    print("Suppression d'une maladie:")
    maladie_dao.delete_maladie(6)

    db.close()