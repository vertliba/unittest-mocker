from unittest import TestCase

from tests.dummy_class import DummyClass
from unittest_mock import activate_mocker


class MockerTestCase(TestCase):
    @activate_mocker
    def test_patch_callable(self, mocker):
        mocker.patch.object(DummyClass, 'some_method', return_value=2)

        assert DummyClass().some_method() == 2

    @activate_mocker
    def test_patch_without_object(self, mocker):
        """Call `mocker.patch()` instead of `mocker.patch.object` works too."""
        mocker.patch('tests.dummy_class.DummyClass.some_method', return_value=2)

        assert DummyClass().some_method() == 2

    @activate_mocker
    def test_patch_variable(self, mocker):
        mocker.patch.object(DummyClass, 'dummy_var', 11)

        assert DummyClass().dummy_var == 11

    @activate_mocker
    def test_assert_methods(self, mocker):
        mock = mocker.patch.object(DummyClass, 'some_method')

        with self.assertRaises(AssertionError):
            mock.assert_called_once()
            DummyClass.some_method.assert_called_once()  # noqa

        DummyClass().some_method()

        mock.assert_called_once()
        DummyClass.some_method.assert_called_once()  # noqa

    def test_mockers_stop(self):
        """After mocked method finished mocks stop."""

        @activate_mocker
        def func_with_mocker(mocker):
            mocker.patch.object(DummyClass, 'dummy_var', 'mocked')

            assert DummyClass.dummy_var == 'mocked'  # mock is active

        func_with_mocker()

        assert DummyClass.dummy_var == 'original'  # mock is stopped
