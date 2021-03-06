from typing import List
import requests
import filecmp
import os
from os import path
from tests.common import E2ETestBase


class TestV2Python36Http(E2ETestBase):

    def test_numpy_trigger(self):
        function_address = f'http://{self.function_app_url}/api/NumpyTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'numpy-trigger 7')

    def test_plain_text_trigger(self):
        function_address = f'http://{self.function_app_url}/api/PlainTextTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'plain-text-trigger')

    def test_dataclasses_trigger_should_fail(self):
        # Import dataclass will fail in Python 3.6, cause it is introduced in 3.7
        function_address = f'http://{self.function_app_url}/api/DataclassesTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 500)

    def test_raw_body_trigger(self):
        function_address = f'http://{self.function_app_url}/api/RawBodyTrigger'
        image_file = self.test_root / 'resources/functions.png'
        with open(image_file, 'rb') as image:
            img = image.read()
            img_len = len(img)

            resp = requests.post(function_address, data=img)

        received_body_len = int(resp.headers['body-len'])
        self.assertEqual(received_body_len, img_len)

        body = resp.content
        try:
            received_img_file = self.test_root / 'received_img.png'
            with open(received_img_file, 'wb') as received_img:
                received_img.write(body)
            self.assertTrue(filecmp.cmp(received_img_file, image_file))
        finally:
            if (os.path.exists(received_img_file)):
                os.remove(received_img_file)

    def test_keyword_async_trigger(self):
        function_address = f'http://{self.function_app_url}/api/KeywordAsyncTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'async 9')

    def test_external_packages_trigger(self):
        function_address = f'http://{self.function_app_url}/api/ExternalPackagesTrigger'

        resp = requests.get(function_address)

        self.assertEqual(resp.status_code, 200)

        for package in resp.text.split(sep=','):
            (package_name, package_path) = package.split(sep='=')
            self.assertIsNotNone(package_name)
            self.assertIsNotNone(package_path)
