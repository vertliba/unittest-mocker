from __future__ import annotations
import inspect
from typing import Iterable
from unittest.mock import MagicMock, patch


class ClassPatcher:
    mocks: dict[str, MagicMock]

    def __init__(self, target, attribute, methods: Iterable = ['__call__']):
        if not isinstance(methods, Iterable) or isinstance(methods, str):
            raise ValueError("`method` argument must be Iterable.")
        if '__init__' in methods:
            raise ValueError("You shouldn't pass '__init__' method to mock. '__init__' method is always mocked")

        self.target_qual_name = getattr(target, attribute)
        self.mock_methods(methods)
        self.mock_init()

    def mock_methods(self, methods):
        self.mocks = {}
        if not inspect.isclass(self.target_qual_name):
            raise ValueError('Target must be a class')
        for method in methods:
            self.mocks[method] = patch.object(self.target_qual_name, method).start()

    def mock_init(self):
        self.mocks['__init__'] = patch.object(self.target_qual_name, '__init__').start()
        self.mocks['__init__'].return_value = None

    def assert_initialized_with(self, *args, **kwargs):
        self.mocks['__init__'].assert_called_once_with(*args, **kwargs)
