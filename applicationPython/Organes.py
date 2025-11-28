class Organe:
    def __init__(self, id, nomOrgane):
        self.id = id
        self.nomOrgane = nomOrgane

    def __str__(self):
        return f"{self.nomOrgane} (id: {self.id})"