import unittest
import requests
import os


class TestHttp(unittest.TestCase):
    def setUp(self):
        self.stamp_address = os.environ['StampAddress']
        self.function_app_name = 'v2_python_36'

        # Replace with http://localhost:7071 when testing locally at ease
        self.function_app_url = f'http://{self.function_app_name}.{self.stamp_address}'

    def test_numpy_trigger(self):
        function_address = f'{self.function_app_url}/api/NumpyTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'numpy-trigger 7')

    def test_plain_text_trigger(self):
        function_address = f'{self.function_app_url}/api/PlainTextTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'plain-text-trigger')
