import random
import string

import unittest
import PyCLTO

class LTOTest(unittest.TestCase):

    def gen_random_str(self, stringLength=30):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def test_reading_chain_info(self):
        pl = PyCLTO.PyCLTO()

        output = pl.getChain()
        self.assertIn("mainnet", str(output))
        output = pl.getNode()
        self.assertIn("https://nodes.lto.network",str(output))
        output = pl.height()
        self.assertEqual(True,type(output) is int)

        output = pl.Address('3Jhkp3Xtg2wyT6NoEtJB2VQPAHiYuqYUVBp')
        self.assertIn("3Jhkp3Xtg2wyT6NoEtJB2VQPAHiYuqYUVBp", str(output))


if __name__ == '__main__':
    unittest.main()
