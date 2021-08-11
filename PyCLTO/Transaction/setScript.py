import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time


def setScript(self, scriptSource, txFee=0, timestamp=0):
    if txFee == 0:
        txFee = self.pyclto.DEFAULT_SCRIPT_FEE
    script = self.pyclto.wrapper('/utils/script/compile', scriptSource)['script'][7:]  # broadcaster ?
    if not self.privateKey:
        logging.error('Private key required')
    else:
        compiledScript = base64.b64decode(script)
        scriptLength = len(compiledScript)
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        sData = b'\13' + \
                b'\1' + \
                crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                base58.b58decode(self.publicKey) + \
                b'\1' + \
                struct.pack(">H", scriptLength) + \
                compiledScript + \
                struct.pack(">Q", txFee) + \
                struct.pack(">Q", timestamp)
        signature = self.sign(self.privateKey, sData)

        data = json.dumps({
            "type": 13,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "fee": txFee,
            "timestamp": timestamp,
            "script": 'base64:' + script,
            "proofs": [
                signature
            ]
        })

        return self.pyclto.wrapper('/transactions/broadcast', data)