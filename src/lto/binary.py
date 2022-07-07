import base64
import base58


class Binary(bytes):
    def base58(self):
        return base58.b58encode(self)

    def base64(self):
        return base64.b64encode(self)

    @staticmethod
    def frombase58(cls):
        return Binary(base58.b58decode(cls))

    @staticmethod
    def frombase64(cls):
        return Binary(base64.b64decode(cls))
