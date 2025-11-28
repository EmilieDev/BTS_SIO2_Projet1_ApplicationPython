class Organisme:
    def __init__(self, id, nomOrg):
        self.id = id
        self.nomOrg = nomOrg

    def __str__(self):
        return f"{self.nomOrg} (id: {self.id})"