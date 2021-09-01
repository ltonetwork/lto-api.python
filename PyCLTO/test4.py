
import json

data = {
  "type": 15,
  "version": 1,
  "id": "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon",
  "sender": "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ",
  "senderPublicKey": "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne",
  "fee": 35000000,
  "timestamp": 1610397549043,
  "anchors": [
    "5SbkwAekNbaG8P1mTDdAE88mpWtCdET9vTmV2v9vQsCK"
  ],
  "proofs": [
    "4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"
  ],
  "height": 1069662
}

from PyCLTO import PyCLTO as pyclto
ret = pyclto().fromData(data)
