from SpecialitesDAO import SpecialitesDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    specialite_dao = SpecialitesDAO(db)
   
    print("Liste des spécialités:")
    specialites = specialite_dao.get_all_specialites()
    for s in specialites:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter une spécialité:")
    specialite_dao.insert_specialite("VI")

    print("Modifier nom d'une specialité:")
    specialite_dao.update_specialite(5, "V")

    print("Suppression d'une spécialite:")
    specialite_dao.delete_specialite(5)

    db.close()