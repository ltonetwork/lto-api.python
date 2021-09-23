# lto-api.python
Python client library for interacting with LTO Network


## Accounts

### Create an account
The chainId is 'L' for the MainNet and 'T' TestNet

```python
from src.LTO.AccountFactory import AccountFactory

account = AccountFactory(chainId).create()
```
### Create an account from seed

```python
from src.LTO.AccountFactory import AccountFactory

account = AccountFactory(chaindId).createFromSeed(seed)
```

### Create an account from public key

```python
from src.LTO.AccountFactory import AccountFactory

account = AccountFactory(chainId).createFromPublicKey(publicKey)
```

### Create an account from private key

```python
from src.LTO.AccountFactory import AccountFactory

account = AccountFactory(chainId).createFromPrivateKey(privateKey)
```

## Executing Transactions:
First a transaction needs to be created:
### Ex Transfer Transaction
```
from src.LTO.Transactions.Transfer import Transfer
transaction = Transfer(recipient, amount)
```
The Transaction needs then to be signed. <br/>
In order to sign a transaction an account is needed (check at the beginning of the page the steps to create an account).

### Ex of signinig a transaction
```
transaction.signWith(account)
```
For last the transaction needs to be broadcasted to the node. <br/>
In order to do so we need to connect to the node using the PublicNode class.

```
from src.LTO.PublicNode import PublicNode
node = PublicNode(url)
```
The url refers to the node, there are many nodes available, here there are two examples, one for the MainNet and one for the TestNet <br/>

https://nodes.lto.network <br/>
https://testnet.lto.network

### Ex of broadcasting a transaction
```
transaction.broadcastTo(node)
```

## Transactions
### Transfer Transaction

```python
from src.LTO.Transactions.Transfer import Transfer

transaction = Transfer(recipient, amount)
```

### Mass Transfer Transaction

```python
from src.LTO.Transactions.MassTransfer import MassTransfer

transaction = MassTransfer(transfers)
```
### Anchor Transaction

```python
import Anchor

transaction = Anchor(anchor)
```
### Lease Transaction

```python
from src.LTO.Transactions.Lease import Lease

transaction = Lease(recipient, amount)
```
### Cancel Lease Transaction

```python
from src.LTO.Transactions.CancelLease import CancelLease

transaction = CancelLease(leaseId)
```

### SetScript Transaction

```python
from src.LTO.Transactions.SetScript import SetScript

transaction = SetScript(script)
```

### Sponsorship transaction

```python
from src.LTO.Transactions.Sponsorship import Sponsorship

transaction = Sponsorship(recipient)
```

### Cancel Sponsorship transaction

```python
from src.LTO.Transactions.CancelSponsorship import CancelSponsorship

transaction = CancelSponsorship(recipient)
```

### Association transaction

```python
from src.LTO.Transactions.Association import Association

transaction = Association(recipient, associationType, anchor)
```
### Revoke Association transaction

```python
from src.LTO.Transactions.RevokeAssociation import RevokeAssociation

transaction = RevokeAssociation(recipient, associationType, anchor)
```
