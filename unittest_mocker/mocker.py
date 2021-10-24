from __future__ import annotations

from functools import wraps
from typing import Generic, TypeVar, Callable, Any
from unittest.mock import patch

from unittest_mocker.class_patcher import ClassPatcher
from unittest_mocker.standart_patcher import standard_patcher


def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:  # pragma: no cover
        __import__(import_path)
        return getattr(thing, comp)


def _importer(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = __import__(import_path)

    for comp in components:
        import_path += ".%s" % comp
        thing = _dot_lookup(thing, comp, import_path)
    return thing


def _get_target(target):
    try:
        target, attribute = target.rsplit('.', 1)
    except (TypeError, ValueError):  # pragma: no cover
        raise TypeError("Need a valid target to patch. You supplied: %r" %
                        (target,))
    return _importer(target), attribute


T = TypeVar('T')


class _SegregatePatcher(Generic[T]):
    """Segregate one argument if it is a call without `object`, like `patch(..)` or two arguments if it is a call with `object` like `patch.object(..)`"""
    _patcher: Callable

    def __init__(self, patcher: Callable[[str, str, Any], T]):
        self._patcher = patcher  # type: ignore

    def __call__(self, target, *args, **kwargs) -> T:
        target, attribute = _get_target(target)
        return self._patcher(target, attribute, *args, **kwargs)

    def object(self, target, attribute, *args, **kwargs) -> T:
        return self._patcher(target, attribute, *args, **kwargs)


class Mocker:
    def __init__(self):
        self.mocks = []

    @property
    def patch(self):
        return _SegregatePatcher(patcher=standard_patcher)

    @property
    def patch_class(self):
        return _SegregatePatcher(patcher=ClassPatcher)


def activate_mocker(test_func):
    @wraps(test_func)
    def wrapper(*args, **kwargs):
        _mocker = Mocker()
        test_func(*args, mocker=_mocker, **kwargs)
        patch.stopall()

    return wrapper
