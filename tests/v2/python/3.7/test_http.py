import requests
from tests.common import E2ETestBase


class TestHttp(E2ETestBase):

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

    def test_dataclasses_trigger(self):
        function_address = f'{self.function_app_url}/api/DataclassesTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'dataclasses-trigger 3')
