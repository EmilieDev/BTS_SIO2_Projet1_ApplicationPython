from UtilisateursDAO import UtilisateursDAO
from ConnexionBdd import Database
if __name__ == "__main__":
    db = Database(host="172.27.0.50", user="grp05Admin", password="grp05Mdp", database="grp05ClinPasteur")
   
    utilisateur_dao = UtilisateursDAO(db)
   
    print("Liste des utilisateurs:")
    utilisateurs = utilisateur_dao.get_all_utilisateurs()
    for s in utilisateurs:
        print(s)


    #Test pour les fonctionalités CRUD:
    print("Ajouter un utilisateur:")
    utilisateur_dao.insert_utilisateur("Poisson", "Poisson12345%")

    print("Modifier nom d'un utilisateur:")
    utilisateur_dao.update_utilisateur(2, "Poisson1", "Poisson123456%")

    print("Suppression d'un utilisateur:")
    utilisateur_dao.delete_utilisateur(2)

    db.close()