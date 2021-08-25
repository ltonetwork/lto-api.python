from PyCLTO.test2 import get_op_sys


''' def test_get_op_sys():
    assert get_op_sys() == 'Mac' '''

def test_get_op_sys(mocker):
    # Mock the slow function and return True always
    mocker.patch('lto-api.is_mac', return_value=True)
    assert get_op_sys() == 'Mac'



