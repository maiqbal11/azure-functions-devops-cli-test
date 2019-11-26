import requests
from tests.common import E2ETestBase


class TestV2Node10Http(E2ETestBase):
    def test_plain_text_trigger(self):
        function_address = f'{self.function_app_url}/api/PlainTextTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'plain-text-trigger')
