
import json

data = {
    "type": 16,
    "version": 1,
    "party": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
    "associationType": 1,
    "hash": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
    "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
    "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
    "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
    "timestamp": 1610404930000,
    "fee": 100000000,
    "proofs": [
        "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
    ],
    "height": 1225712
}

from PyCLTO import PyCLTO as pyclto
ret = pyclto().fromData(data)


for key in data:
    if data[key] == ret.__getattr__(key):
        print(True)
    else:
        print(key, ' ', False)



# for cancel lease


