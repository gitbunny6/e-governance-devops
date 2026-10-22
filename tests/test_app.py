import unittest
from app.app import app


class EGovernanceAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_services_endpoint(self):
        response = self.client.get("/api/services")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_create_application_missing_name(self):
        response = self.client.post(
            "/api/applications",
            json={"service_id": 1}
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()