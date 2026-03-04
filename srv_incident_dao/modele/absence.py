class Absence:
    def __init__(
        self,
        id,
        nom,
        prenom,
        type_absence,
        date_debut,
        date_fin,
        description,
        date_declaration
    ):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.type_absence = type_absence
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.description = description
        self.date_declaration = date_declaration

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "type_absence": self.type_absence,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "description": self.description,
            "date_declaration": self.date_declaration
        }
