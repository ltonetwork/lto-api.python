
import json

data = {
    "id": "5a1ZVJTu8Y7mPA6BbkvGdfmbjvz9YSppQXPnb5MxihV5",
    "type": 4,
    "version": 2,
    "sender": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
    "senderPublicKey": "9NFb1rvMyr1k8f3wu3UP1RaEGsozBt9gF2CmPMGGA42m",
    "fee": 100000000,
    "timestamp": 1609639213556,
    "amount": 100000000000,
    "recipient": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
    "attachment": "9Ajdvzr",
    "proofs": [
        "3ftQ2ArKKXw655WdHy2TK1MGXeyzKRqMQYwFidekkyxLpzFGsTziSFsbM5RCFxrn32EzisMgPWtQVQ4e5UqKUcES"
    ],
    "height": 1212761
}

from PyCLTO import PyCLTO as pyclto
ret = pyclto().fromData(data)
print(ret)
print(ret.id)