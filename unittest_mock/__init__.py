from unittest.mock import patch, MagicMock


class _Patch:
    def __call__(self, *args, **kwargs) -> MagicMock:
        _mock = patch(*args, **kwargs)
        return _mock.start()

    def object(self, *args, **kwargs) -> MagicMock:
        _mock = patch.object(*args, **kwargs)
        return _mock.start()


class _Mocker:
    def __init__(self):
        self.mocks = []

    @property
    def patch(self):
        return _Patch()


def activate_mocker(test_func):
    def _test_func(*args, **kwargs):
        _mocker = _Mocker()
        test_func(*args, **kwargs, mocker=_mocker)
        patch.stopall()

    return _test_func
