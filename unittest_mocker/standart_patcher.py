from unittest.mock import patch


def standard_patcher(target, attribute, *args, **kwargs):
    return patch.object(target, attribute, *args, **kwargs).start()
