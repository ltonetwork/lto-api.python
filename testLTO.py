import random
import string

import unittest
import PyCLTO

class LTOTest(unittest.TestCase):

    def gen_random_str(self, stringLength=30):
        """ Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(stringLength))

    def test_reading_chain_info(self):
        pl = PyCLTO.PyCLTO()
        print(pl)
        output = pl.getChain()
        print(output)
        #self.assertIn("mainnet", str(output))
        self.assertIn("testnet", str(output))
        output = pl.getNode()
        print(output)

        #self.assertIn("https://mainnet.lto.network", str(output))
        self.assertIn("https://testnet.lto.network", str(output))
        output = pl.height()
        self.assertEqual(True, type(output) is int)


        # previous: 3Jhkp3Xtg2wyT6NoEtJB2VQPAHiYuqYUVBp
        output = pl.Address('3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du')
        self.assertIn("3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du", str(output))

if __name__ == '__main__':
    unittest.main()
