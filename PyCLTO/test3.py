from PyCLTO import test2
import unittest
from unittest import mock


class AccountTest(unittest.TestCase):

    @mock.patch(target='PyCLTO.test2.isMac', return_value=True)
    def test_isMac(self, mock):
        assert test2.isMac() == True


if __name__ == '__main__':
    unittest.main()
