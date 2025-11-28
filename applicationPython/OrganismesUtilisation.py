from OrganismesDAO import OrganismesDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    organisme_dao = OrganismesDAO(db)
   
    print("Liste des organismes:")
    organismes = organisme_dao.get_all_organismes()
    for s in organismes:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter un organisme:")
    organisme_dao.insert_organisme("VI")

    print("Modifier nom d'un organisme:")
    organisme_dao.update_organisme(5, "V")

    print("Suppression d'un organisme:")
    organisme_dao.delete_organisme(5)

    db.close()