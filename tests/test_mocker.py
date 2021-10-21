from unittest import TestCase
from unittest_mock import activate_mocker


class Dummy:
    dummy_var = 'original'

    def dummy_func(self):
        return 1


class MockerTestCase(TestCase):
    @activate_mocker
    def test_patch_callable(self, mocker):
        mocker.patch.object(Dummy, 'dummy_func', return_value=2)

        assert Dummy().dummy_func() == 2

    @activate_mocker
    def test_patch_without_object(self, mocker):
        """Call `mocker.patch()` instead of `mocker.patch.object` works to."""
        mocker.patch('test_mocker.Dummy.dummy_func', return_value=2)

        assert Dummy().dummy_func() == 2

    @activate_mocker
    def test_patch_variable(self, mocker):
        mocker.patch.object(Dummy, 'dummy_var', 11)

        assert Dummy().dummy_var == 11

    @activate_mocker
    def test_assert_methods(self, mocker):
        mock = mocker.patch.object(Dummy, 'dummy_func')

        with self.assertRaises(AssertionError):
            mock.assert_called_once()
            Dummy.dummy_func.assert_called_once()  # noqa

        Dummy().dummy_func()

        mock.assert_called_once()
        Dummy.dummy_func.assert_called_once()  # noqa

    def test_mockers_stop(self):
        """After mocked method finished mocks stop."""

        @activate_mocker
        def func_with_mocker(mocker):
            mocker.patch.object(Dummy, 'dummy_var', 'mocked')

            assert Dummy.dummy_var == 'mocked'  # mock is active

        func_with_mocker()

        assert Dummy.dummy_var == 'original'  # mock is stopped
