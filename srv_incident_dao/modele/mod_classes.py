class Incident:
    def __init__(self, id, nom, prenom, type_incident,priorite, statut, description, date_incident, date_cloture, description_admin):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.type_incident = type_incident
        self.priorite = priorite
        self.statut = statut
        self.description = description
        self.date_incident = date_incident
        self.date_cloture = date_cloture
        self.description_admin = description_admin
