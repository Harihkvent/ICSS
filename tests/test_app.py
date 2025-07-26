import unittest
import json
from bot import app

class TestChatAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_chat_endpoint(self):
        response = self.client.post("/chat", json={"query": "Hello"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)

if __name__ == "__main__":
    unittest.main()
