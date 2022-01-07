# lto-api.python
Python client library for interacting with LTO Network


## Accounts

### Create an account
The chain_id is 'L' for the MainNet and 'T' TestNet

```python
from lto.accounts.account_factory import AccountFactory

account = AccountFactory(chain_id).create()
```
### Create an account from seed

```python
from lto.accounts.account_factory import AccountFactory

account = AccountFactory(chain_id).create_from_seed(seed)
```

### Create an account from public key

```python
from lto.accounts.account_factory import AccountFactory

account = AccountFactory(chain_id).create_from_public_key(public_key)
```

### Create an account from private key

```python
from lto.accounts.account_factory import AccountFactory

account = AccountFactory(chain_id).create_from_private_key(private_key)
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
transaction.sign_with(account)
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
transaction.broadcast_to(node)
```

## Transactions
### Transfer Transaction

```python
from src.lto.transactions.transfer import Transfer

transaction = Transfer(recipient, amount)
```

### Mass Transfer Transaction

```python
from src.lto.transactions.mass_transfer import MassTransfer

transaction = MassTransfer(transfers)
```
### Anchor Transaction

```python
import Anchor

transaction = Anchor(anchor)
```
### Lease Transaction

```python
from src.lto.transactions.lease import Lease

transaction = Lease(recipient, amount)
```
### Cancel Lease Transaction

```python
from src.lto.transactions.cancel_lease import CancelLease

transaction = CancelLease(lease_id)
```

### SetScript Transaction

```python
from src.lto.transactions.set_script import SetScript

transaction = SetScript(script)
```

### Sponsorship transaction

```python
from src.lto.transactions.sponsorship import Sponsorship

transaction = Sponsorship(recipient)
```

### Cancel Sponsorship transaction

```python
from src.lto.transactions.cancel_sponsorship import CancelSponsorship

transaction = CancelSponsorship(recipient)
```

### Association transaction

```python
from src.lto.transactions.association import Association

transaction = Association(recipient, association_type, anchor)
```
### Revoke Association transaction

```python
from src.lto.transactions.revoke_association import RevokeAssociation

transaction = RevokeAssociation(recipient, association_type, anchor)
```
