from PyCLTO.coin import pyLTOCoin
from PyCLTO import PyCLTO


class TestCoin:
    pyclto = PyCLTO('T')

    def testConstruct(self):
        pyCoin = pyLTOCoin(self.pyclto)
        assert pyCoin.decimals == 8
        assert self.pyclto == pyCoin.pylto
        assert pyCoin.assetId == ''
        assert pyCoin.issuer == pyCoin.name == pyCoin.description == 'LTO'
        assert pyCoin.reissuable is False
        assert pyCoin.quantity == 500000000e8
        assert pyCoin.__str__() == 'assetId = %s\n' \
                                   'issuer = %s\n' \
                                   'name = %s\n' \
                                   'description = %s\n' \
                                   'quantity = %d\n' \
                                   'decimals = %d' % ('', 'LTO', 'LTO', 'LTO', 500000000e8, 8)

        assert pyCoin.__repr__ == pyCoin.__str__
