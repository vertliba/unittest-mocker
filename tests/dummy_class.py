class DummyClass:
    dummy_var = 'original'

    def __init__(self, init_param=0):
        pass

    def __call__(self, call_param=0):
        return 'not_mocked_call'

    def some_method(self, some_method_param):
        return 'not_mocked_some_method'

    def some_other_method(self, some_other_method_param):
        return 'not_mocked_some_other_method'
