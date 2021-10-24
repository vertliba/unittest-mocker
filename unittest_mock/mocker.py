from __future__ import annotations

from functools import wraps
from typing import Protocol, Generic, TypeVar, Callable, Any
from unittest.mock import patch

from unittest_mock.class_patcher import ClassPatcher
from unittest_mock.standart_patcher import standard_patcher


def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:
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
    except (TypeError, ValueError):
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

    def get_full_path(self, attribute, target):
        target = f'{target.__module__}.{target.__qualname__}.{attribute}'
        return target


class Mocker:
    def __init__(self):
        self.mocks = []

    @property
    def patch(self):
        return _SegregatePatcher(patcher=standard_patcher)

    @property
    def patch_class(self):
        return _SegregatePatcher(patcher=ClassPatcher)


class DecoratedTest(Protocol):
    def __call__(self, *args: Any, mocker: Mocker, **kwargs: Any) -> None: ...


def activate_mocker(test_func: DecoratedTest):
    @wraps(test_func)
    def wrapper(*args, **kwargs):
        _mocker = Mocker()
        test_func(*args, mocker=_mocker, **kwargs)
        patch.stopall()

    return wrapper
