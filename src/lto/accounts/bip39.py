from mnemonic import Mnemonic


def random_seed(language="english"):
    return Mnemonic(language).generate(strength=256)
