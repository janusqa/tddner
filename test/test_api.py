import unittest
import json
from flask import request
from tddner.app import app


class TestAApi(unittest.TestCase):
    def test_ner_endpoint_given_json_body_returns_200(self):
        app.testing = True
        with app.test_client() as client:
            response = client.post(
                "/ner", json={"sentence": "Steve Malkmus is is a good band."}
            )
            self.assertEqual(response._status_code, 200)

    def test_ner_endpoint_given_json_body_with_known_entities_returns_entity_result_in_response(
        self,
    ):
        app.testing = True
        with app.test_client() as client:
            response = client.post("/ner", json={"sentence": "Kamala Harris."})
            data = json.loads(response.get_data())
            self.assertGreater(len(data["entities"]), 0)
            self.assertEqual(data["entities"][0]["ent"], "Kamala Harris")
            self.assertEqual(data["entities"][0]["label"], "Person")
