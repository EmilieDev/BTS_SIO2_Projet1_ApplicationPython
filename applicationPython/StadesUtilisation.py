from StadesDAO import StadesDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    stade_dao = StadesDAO(db)
   
    print("Liste des stades:")
    stades = stade_dao.get_all_stades()
    for s in stades:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter un stade:")
    stade_dao.insert_stade("VI")

    print("Modifier nom d'un stade:")
    stade_dao.update_stade(5, "V")

    print("Suppression d'un stade:")
    stade_dao.delete_stade(5)

    db.close()