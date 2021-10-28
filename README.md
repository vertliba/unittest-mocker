unittest-mocker
==================

![build](https://github.com/vertliba/unittest-mocker/workflows/build/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/vertliba/unittest-mocker/branch/master/graph/badge.svg)](https://codecov.io/gh/vertliba/unittest-mocker)
[![PyPI version](https://badge.fury.io/py/unittest-mocker.svg)](https://badge.fury.io/py/unittest-mocker)

Inspired by the [pytest-mock](https://github.com/pytest-dev/pytest-mock), but written from scratch for using with
unittest and convenient tool - [**patch_class**](#Class-mocker)

Installation
------------

```shell script
pip install unittest-mocker
```

Usage
-----

### General mocker

```python
@activate_mocker
def test_create_client(self, mocker: Mocker):
    post_mock = mocker.patch('requests.post')
    post_mock.return_value.status_code = 200
    post_mock.return_value.json.return_value = {'msg': done}
    
    send_clients_to_crm()
    
    post_mock.assert_called_once_with(...)
```

or you can put the mocking logic in a separate method:

```python
def mock_post(mocker, status):
    response = requests.Response()
    response.status_code = status
    response.headers = {'Location': '...'}
    response._content = 'some content'
    
    return mocker.patch('requests.post', return_value=response)

@activate_mocker
def test_upload_post_success(mocker):
    mocked_post = mock_post(mocker, 201)
    ...
@activate_mocker
def test_upload_post_error(mocker):
    mocked_post = mock_post(mocker, 500)
    ...
```

#### Details

`mocker.patch` under the hood calls `unittest.mock.patch`
So you can apply any arguments of [the standard mock library](https://docs.python.org/3/library/unittest.mock.html)

The same with `mocker.patch.object`. It has the same parameters as`unittest.mock.patch.object`


### Method `patch_class` 

Basic usage:

```python
from unittest_mocker import activate_mocker, Mocker
from api import ApiClient

@activate_mocker
def test_api_client(self, mocker: Mocker):
    client_mock = mocker.patch_class('api.ApiClient')

    ApiClient(url='example.com')(command='start')
    
    client_mock.assert_initialized_with(url='example.com')
    client_mock.mocks['__call__'].assert_called_once_with(command='start')
```

#### Syntax

```python
# Variant 1
mocker.patch_class(target: str, methods=Optional[list[str]])
# Example:
mock = mocker.patch_class('some_module.SomeClass', methods=['method_1', 'method_2'])

# Variant 2
mocker.patch_class.object(target: Union[module, class], attribute: str, methods=Optional[list[str]])
# Example:
import some_module
mock = mocker.patch_class(some_module, 'SomeClass', methods=['method_1', 'method_2'])
```

All mocked methods are stored in `mock.mocks` dictionary and can be accessed:
```python
mock.mocks['__init__'].assert_called_once_with(...)
```

`patch_class` always patches class's `__init__` method. 

Also, `methods` parameter also defaults to [`__call__`]. So that's correct:

```python
mock = mocker.patch_class('some_module.SomeClass')
...
mock.mocks['__call__'].assert_called_once_with(...)
```

#### Helper `assert_initialized_with`

`mock.assert_initialized_with()` is just shortcut for `mock.mocks['__init__'].assert_called_once_with()`
