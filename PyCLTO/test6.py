from PyCLTO.test4 import func


def test_slow_function(mocker):
    mocker.patch('PyCLTO.test5.api_call', return_value=9)
    assert func().slow_function() == 9
