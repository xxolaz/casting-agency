import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

# --- Define tokens for each role ---
CASTING_ASSISTANT_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxQzZKRkVpMzJMckozQ1RHcVM5TCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jZjdpaWd4ZnRxdGxteHBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2ODc1NGMzMDY3NWYwMWQyNWQ5OTlkMjEiLCJhdWQiOiJodHRwczovL2Nhc3RpbmctYXBpIiwiaWF0IjoxNzUyNTE5MDMxLCJleHAiOjE3NTI2MDU0MzEsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIHBvc3Q6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJzQlVjbTdlc0ZKbm1DS0NxbXJQc3cwcXZTcXZoU2poSCJ9.wAFdv4vjKpjByOAGf-JFbsUoTi4A6TQM5GMzMQSgYH315VpAKSny8vrjXM4du1npoGq_3xz094vK1FzkUKn7q_q_ZdN24k1_JxcI7n6p5gHfqY-rd5MQ6sLHwy9TIT9-Goq1moqo4LxYQas3867EF1sW2YPTI3dkEmbBbYZgyMxeI7mFr5yxV_-kuRsckYBguEUonT8GSD4zhGhduIkSs5y26tifj-Wgt7AZi4eOqW2ezsY7uijfDp9l99u-qroVvKdL5k1tt9Kmh4b8CIReM3i7et6_SojW9raraRPfstDl1zvI392AxyLNVH3x2-M9zLCwqgST-7DowHSCUlLJ8g"
CASTING_DIRECTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxQzZKRkVpMzJMckozQ1RHcVM5TCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jZjdpaWd4ZnRxdGxteHBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2ODc1NGMzYzJjYjc0MThjYWE3Y2RiMGQiLCJhdWQiOiJodHRwczovL2Nhc3RpbmctYXBpIiwiaWF0IjoxNzUyNTE4OTk1LCJleHAiOjE3NTI2MDUzOTUsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIHBvc3Q6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJzQlVjbTdlc0ZKbm1DS0NxbXJQc3cwcXZTcXZoU2poSCJ9.TcwACteOj5GcTMKjwsAYDzoOME8NFyOjKpj_n7SHhH1XBMuK8rMPt5j_uPsoTU0yyUl7ENkfdNp9hoIaGY5FuxNrSH2UPx1KMc-pDTl0rJC0pyZKw049I8jv-wWddvZwwqibdO7hQrJnHpR9aMZEuHtY9FfuFKp6Ix8PRGHe0LdbNMWKwuGZJz5wyIaez26-wx3VYQKpXn23GD_NVk6QclVzqhVjYTsgfKJF7Na85lDsdluLYo2ZgIoKv7_KjnrzLvn_n2N88rHwJ7cUW-tTjmWjzgDJLxy7bwszVeFovEPe-k1hArUFxQVTMDLlN1l3XHZR2OHuScHmT8sTf-g9KA"
EXECUTIVE_PRODUCER_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxQzZKRkVpMzJMckozQ1RHcVM5TCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jZjdpaWd4ZnRxdGxteHBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2ODc1NGM0YzY3NWYwMWQyNWQ5OTlkMmIiLCJhdWQiOiJodHRwczovL2Nhc3RpbmctYXBpIiwiaWF0IjoxNzUyNTE4ODY1LCJleHAiOjE3NTI2MDUyNjUsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIHBvc3Q6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJzQlVjbTdlc0ZKbm1DS0NxbXJQc3cwcXZTcXZoU2poSCJ9.Lt2ZFWjXmbnnWNoR9Jg4xhRB7Cyg7xD0pp6_cH9XXIGIWTpcX1jnTaKz0kYaJpa02g2v1OxObg5g0LEuHJqESXJOTvXElmmz-YbiLwli9g_PMh_krrPIERoRpkM2OTS61StcQZA7YHhEPV-GVx5pD5DgKfNkVqR83CHJhCcTE4LBs92J7OslJT5GWc0-a6gzYQTxOcsgtudziHLQGA88GMamzSIrZHwNhHoTNxqTSEl74fZFxBdEj0K-6u3NA7dwjuvQJSMy7Q2MsA5jrhNdcEBR1kWeyNWaGygHVS2wzNY_Z-ijd_EpBQ7uG8YBFu76q3jA1iwgmcQHH_Pa8nLKqA"


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # --- Test Cases ---

    # Example Success Test
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Example Error Test
    def test_404_get_actors_not_found(self):
        res = self.client().get('/actors/9999', headers={'Authorization': CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Example RBAC Test (Failure)
    def test_rbac_assistant_cannot_create_actor(self):
        res = self.client().post('/actors',
                                 json={'name': 'New Guy', 'age': 25, 'gender': 'Male'},
                                 headers={'Authorization': CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403) # Forbidden
        self.assertEqual(data['success'], False)

    # Example RBAC Test (Success)
    def test_rbac_director_can_create_actor(self):
        res = self.client().post('/actors',
                                 json={'name': 'New Gal', 'age': 30, 'gender': 'Female'},
                                 headers={'Authorization': CASTING_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests executable
if __name__ == "__main__":
    unittest.main()