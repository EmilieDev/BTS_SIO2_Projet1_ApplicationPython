from OrganesDAO import OrganesDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    organe_dao = OrganesDAO(db)
   
    print("Liste des organes:")
    organes = organe_dao.get_all_organes()
    for s in organes:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter un organe:")
    organe_dao.insert_organe("TEST")

    print("Modifier nom d'un organe:")
    organe_dao.update_organe(6, "TEST2")

    print("Suppression d'un organe:")
    organe_dao.delete_organe(6)

    db.close()