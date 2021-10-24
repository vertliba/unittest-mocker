from unittest.mock import patch


def _patch(*args, mock_with_object=False, **kwargs):
    mock_method = patch.object if mock_with_object else patch
    _mock = mock_method(*args, **kwargs)
    return _mock.start()
