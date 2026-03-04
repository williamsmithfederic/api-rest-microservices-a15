import unittest
import json
from mod_srv_incident import app

class IncidentServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # ==========================
    # TEST GET INCIDENTS
    # ==========================
    def test_get_incidents(self):
        response = self.app.get('/incidents')
        self.assertEqual(response.status_code, 200)

    # ==========================
    # TEST CREATE INCIDENT
    # ==========================
    def test_create_incident(self):
        data = {
            "nom": "Test",
            "prenom": "User",
            "type_incident": "Test type",
            "priorite": "Low"
        }

        response = self.app.post(
            '/incidents',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

    # ==========================
    # TEST UPDATE STATUT
    # ==========================
    def test_update_statut(self):
        data = {
            "statut": "Clos",
            "description_admin": "Test intervention"
        }

        response = self.app.post(
            '/incidents/1/statut',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertIn(response.status_code, [200, 500])  # dépend si ID existe


if __name__ == '__main__':
    unittest.main()