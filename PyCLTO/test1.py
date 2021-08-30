import copy

from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Transfer import Transfer
from PyCLTO.PublicNode import PublicNode
from time import time

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
node = PublicNode('https://testnet.lto.network')

account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
account2 = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 300000000)
transaction.timestamp = 1629883934685
transaction.signWith(account2)

print(account2.verifySignature(transaction.toBinary(), transaction.proofs[0]))

print(transaction.proofs)
transaction.signWith(account)
print(transaction.proofs)

#transaction.broadcastTo(node)

def removeInitialProofsFromAccount(proofs, proof):
    proofs_copy = copy.copy(proofs)
    for x in proofs:
        if x != proof:
            proofs_copy.remove(x)
    return proofs_copy



newProofs = removeInitialProofsFromAccount(transaction.proofs, transaction.proofs[1])
print(newProofs)
print(transaction.proofs)