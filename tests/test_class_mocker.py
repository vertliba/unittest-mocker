from unittest import TestCase
from unittest.mock import MagicMock

import tests.dummy_class as dummy_class
from tests.dummy_class import DummyClass
from unittest_mocker import Mocker, activate_mocker


class ClassMockerTestCase(TestCase):

    @activate_mocker
    def test_init_mocked_by_default(self, mocker: Mocker) -> None:
        dummy_mock = mocker.patch_class.object(dummy_class, 'DummyClass')
        DummyClass(init_param='mocked_init_param')

        dummy_mock.mocks['__init__'].assert_called_once_with(init_param='mocked_init_param')
        self.assert_method_is_mocked(dummy_mock, '__init__')

    @activate_mocker
    def test_call_mocked_if_no_methods_passed(self, mocker: Mocker):
        dummy_mock = mocker.patch_class.object(dummy_class, 'DummyClass')

        DummyClass()(call_param='mocked_call_param')

        dummy_mock.mocks['__call__'].assert_called_once_with(call_param='mocked_call_param')
        self.assert_method_is_mocked(dummy_mock, '__call__')

    @activate_mocker
    def test_call_not_mocked_if_other_methods_passed(self, mocker: Mocker):
        dummy_mock = mocker.patch_class.object(dummy_class, 'DummyClass', methods=['some_method'])

        DummyClass()(call_param='mocked_call_param')

        self.assert_method_is_not_mocked(dummy_mock, '__call__')

    @activate_mocker
    def test_mock_custom_methods(self, mocker: Mocker):
        dummy_mock = mocker.patch_class.object(dummy_class, 'DummyClass', methods=['some_method', 'some_other_method'])
        dummy_mock.mocks['some_method'].return_value = 'some_method_mocked'
        dummy_mock.mocks['some_other_method'].return_value = 'some_other_method_mocked'

        cls = DummyClass()

        assert cls.some_method(some_method_param=1) == 'some_method_mocked'  # type: ignore
        assert cls.some_other_method(some_other_method_param=2) == 'some_other_method_mocked'
        dummy_mock.mocks['some_method'].assert_called_once_with(some_method_param=1)
        dummy_mock.mocks['some_other_method'].assert_called_once_with(some_other_method_param=2)

    @activate_mocker
    def test_mock_by_name_without_object_works_too(self, mocker: Mocker):
        dummy_mock = mocker.patch_class('tests.dummy_class.DummyClass', methods=['some_method', 'some_other_method'])
        dummy_mock.mocks['some_method'].return_value = 'some_method_mocked'

        cls = DummyClass()

        assert cls.some_method(some_method_param=1) == 'some_method_mocked'  # type: ignore
        dummy_mock.mocks['some_method'].assert_called_once_with(some_method_param=1)

    @activate_mocker
    def test_initialized_with(self, mocker: Mocker) -> None:
        dummy_mock = mocker.patch_class.object(dummy_class, 'DummyClass')

        DummyClass('arg_param_value', kwarg_param='kwarg_value')  # type: ignore

        dummy_mock.assert_initialized_with('arg_param_value', kwarg_param='kwarg_value')
        with self.assertRaises(AssertionError):
            dummy_mock.assert_initialized_with(wong_param='wrong_value')

    def assert_method_is_not_mocked(self, dummy_mock, method_name):
        self.assertNotIsInstance(getattr(DummyClass, method_name), MagicMock)
        assert method_name not in dummy_mock.mocks

    def assert_method_is_mocked(self, dummy_mock, method_name):
        self.assertIsInstance(getattr(DummyClass, method_name), MagicMock)
        assert method_name in dummy_mock.mocks


class ClassMockerValidationTestCase(TestCase):
    @activate_mocker
    def test___init___in_methods(self, mocker: Mocker):
        expected_msg = "You shouldn't pass '__init__' method to mock. '__init__' method is always mocked"

        with self.assertRaisesRegex(ValueError, expected_msg):
            mocker.patch_class.object(dummy_class, 'DummyClass', methods=['__init__'])

    @activate_mocker
    def test__methods_is_not_iterable_and_string(self, mocker: Mocker):
        expected_msg = "`method` argument must be Iterable."

        with self.assertRaisesRegex(ValueError, expected_msg):
            mocker.patch_class.object(dummy_class, 'DummyClass', methods='some_method')

        with self.assertRaisesRegex(ValueError, expected_msg):
            mocker.patch_class.object(dummy_class, 'DummyClass', methods=123)

    @activate_mocker
    def test_target_must_be_a_class(self, mocker: Mocker):
        expected_msg = "Target must be a class"

        with self.assertRaisesRegex(ValueError, expected_msg):
            mocker.patch_class.object(DummyClass, 'dummy_var')
