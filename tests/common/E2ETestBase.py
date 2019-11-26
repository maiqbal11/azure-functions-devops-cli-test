from typing import Optional
from unittest import TestCase
import os
import importlib


class E2ETestBase(TestCase):
    def __init__(self, *args, **kwargs):
        super(E2ETestBase, self).__init__(*args, **kwargs)
        self._module_path = importlib.import_module(self.__module__).__file__

        self.stamp_address = os.getenv('StampAddress')
        self.host_version: str = None  # v2
        self.language: str = None  # python
        self.worker_version: str = None  # 3.6
        self.function_app_name: str = None  # v2_python_36
        self._populate_function_app_meta()

    # This is used for testing locally, by setting environment variable
    # FunctionAppUrl = http://localhost:7071
    @property
    def function_app_url(self) -> str:
        if os.getenv('FunctionAppUrl'):
            return os.environ['FunctionAppUrl']

        return f'http://{self.function_app_name}.{self.stamp_address}'

    def _populate_function_app_meta(self):
        paths = os.path.abspath(self._module_path).split(os.path.sep)

        # Get the last index of tests folder
        # e.g. ./project/tests/v2/dotnet/2/test_http.py
        paths.reverse()
        tests_index: int = paths.index('tests')
        self._host_version = paths[tests_index - 1]
        self._language = paths[tests_index - 2]
        self._worker_version = paths[tests_index - 3]

        # Sanitize worker version
        sanitized_worker_version: str = self._worker_version.replace('.', '')
        self._function_app_name = (
            f'{self._host_version}_{self._language}_{sanitized_worker_version}'
        )
