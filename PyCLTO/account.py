import base64
import os
from datetime import time

import nacl.bindings

import PyCLTO.crypto as crypto
import struct
import json
import base58
import logging


class pyAccount(object):
    def __init__(self, address, publicKey, privateKey='', seed='', nonce=0):
        self.address = address
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.seed = seed
        self.nonce = nonce



    def sendLTO(self, recipient, amount, attachment='', txFee=0, timestamp=0):
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)

        elif amount <= 0:
            msg = 'Amount must be > 0'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < amount + txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)

        else:
            if txFee == 0:
                txFee = self.pyclto.DEFAULT_TX_FEE
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\4' + \
                    b'\2' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", txFee) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)
            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "type": 4,
                "version": 2,
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": txFee,
                "timestamp": timestamp,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature,
                "proofs": [signature]
            })

            return self.pyclto.wrapper('/transactions/broadcast', data)


    def massTransferLTO(self, transfers, attachment='', timestamp=0,baseFee=0):
        if baseFee == 0:
            baseFee = self.pyclto.DEFAULT_BASE_FEE

        txFee = baseFee + int(len(transfers)*baseFee/10)
        totalAmount = 0

        for i in range(0, len(transfers)):
            totalAmount += transfers[i]['amount']

        if not self.privateKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif len(transfers) > 100:
            msg = 'Too many recipients'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < totalAmount + txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            transfersData = b''
            for i in range(0, len(transfers)):
                transfersData += base58.b58decode(transfers[i]['recipient']) + struct.pack(">Q", transfers[i]['amount'])
            sData = b'\x0b' + \
                    b'\1' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">H", len(transfers)) + \
                    transfersData + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)

            signature = crypto.sign(self.privKey, sData)

            data = json.dumps({
                "type": 11,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "fee": txFee,
                "timestamp": timestamp,
                "transfers": transfers,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature,
                "proofs": [
                    signature
                ]
            })

            return self.pyclto.wrapper('/transactions/broadcast', data)

    def lease(self, recipient, amount, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_LEASE_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif amount <= 0:
            msg = 'Amount must be > 0'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < amount + txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x08' + \
                    b'\2' + \
                    b'\0' + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp)
            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "version": 2,
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature,
                "type": 8,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req

    def leaseCancel(self, leaseId, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_LEASE_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x09' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp) + \
                    base58.b58decode(leaseId)
            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "txId": leaseId,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature,
                "type": 9
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            if self.pyclto.OFFLINE:
                return req
            elif 'leaseId' in req:
                return req['leaseId']

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
            signature = crypto.sign(self.privKey, sData)

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

    def anchor(self, anchor, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_LEASE_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)

        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x0f' + \
                    b'\1' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">H", 1) + \
                    struct.pack(">H", len(crypto.str2bytes(anchor))) + \
                    crypto.str2bytes(anchor) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)
            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "type": 15,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "anchors": [
                    base58.b58encode(crypto.str2bytes(anchor))
                ],
                "fee": txFee,
                "timestamp": timestamp,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req

    def invokeAssociation(self,party, type, anchor, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_LEASE_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)

        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x10' + \
                    b'\1' + \
                    crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(party.address) + \
                    struct.pack(">i", type) + \
                    b'\1' + \
                    struct.pack(">H", len(crypto.str2bytes(anchor))) + \
                    crypto.str2bytes(anchor) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)

            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "type": 16,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "party": party.address,
                "associationType": type,
                "hash":  base58.b58encode(crypto.str2bytes(anchor)),
                "fee": txFee,
                "timestamp": timestamp,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req

    def revokeAssociation(self,party, type, anchor, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_LEASE_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)

        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x11' + \
                    b'\1' + \
                    crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(party.address) + \
                    struct.pack(">i", type) + \
                    b'\1' + \
                    struct.pack(">H", len(crypto.str2bytes(anchor))) + \
                    crypto.str2bytes(anchor) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)

            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "type": 17,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "party": party.address,
                "associationType": type,
                "hash": base58.b58encode(crypto.str2bytes(anchor)),
                "fee": txFee,
                "timestamp": timestamp,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req

    def sponsor(self, recipient, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_SPONSOR_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x12' + \
                    b'\1' + \
                    crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)

            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "version": 1,
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature,
                "type": 18,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req

    def cancelSponsor(self, recipient, txFee=0, timestamp=0):
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_SPONSOR_FEE
        if not self.privKey:
            msg = 'Private key required'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        elif not self.pyclto.OFFLINE and self.balance() < txFee:
            msg = 'Insufficient LTO balance'
            logging.error(msg)
            self.pyclto.throw_error(msg)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x13' + \
                    b'\1' + \
                    crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)

            signature = crypto.sign(self.privKey, sData)
            data = json.dumps({
                "version": 1,
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature,
                "type": 19,
                "proofs": [
                    signature
                ]
            })
            req = self.pyclto.wrapper('/transactions/broadcast', data)
            return req


