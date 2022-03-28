# lto-api.python
Python client library for interacting with LTO Network


## Accounts

### Create an account
The chain_id is 'L' for the mainnet and 'T' testnet

```python
from lto.accounts.ed25519 import AccountFactory

account = AccountFactory(chain_id).create()
```
### Create an account from seed

```python
from lto.accounts.ed25519 import AccountFactory

account = AccountFactory(chain_id).create_from_seed(seed)
```

### Create an account from public key

```python
from lto.accounts.ed25519 import AccountFactory

account = AccountFactory(chain_id).create_from_public_key(public_key)
```

### Create an account from private key

```python
from lto.accounts.ed25519 import AccountFactory

account = AccountFactory(chain_id).create_from_private_key(private_key)
```

## Executing Transactions

### Create transaction
First a transaction needs to be created.

```python
from src.LTO.Transactions.Transfer import Transfer
transaction = Transfer(recipient, amount)
```

The Transaction needs then to be signed.  In order to sign a transaction an account is needed.

### Sign transaction

```python
transaction.sign_with(account)
```
### Broadcast transaction

For last the transaction needs to be broadcasted to the node. In order to do so we need to connect to the node using the PublicNode class.

```python
from src.LTO.PublicNode import PublicNode
node = PublicNode(url)
```
The url refers to the node, there are many nodes available, here there are two examples, one for the mainnet and one for the testnet

* https://nodes.lto.network
* https://testnet.lto.network

```python
transaction.broadcast_to(node)
```

## Transactions

### Transfer Transaction

```python
from lto.transactions import Transfer

transaction = Transfer(recipient, amount)
```

### Mass Transfer Transaction

```python
from lto.transactions import MassTransfer

transaction = MassTransfer(transfers)
```
### Anchor Transaction

```python
from lto.transactions import Anchor

transaction = Anchor(anchor)
```
### Lease Transaction

```python
from lto.transactions import Lease

transaction = Lease(recipient, amount)
```
### Cancel Lease Transaction

```python
from lto.transactions import CancelLease

transaction = CancelLease(lease_id)
```

### SetScript Transaction

```python
from lto.transactions import SetScript

transaction = SetScript(script)
```

### Sponsorship transaction

```python
from lto.transactions import Sponsorship

transaction = Sponsorship(recipient)
```

### Cancel Sponsorship transaction

```python
from lto.transactions import CancelSponsorship

transaction = CancelSponsorship(recipient)
```

### Association transaction

```python
from lto.transactions import Association

transaction = Association(recipient, association_type, anchor)
```
### Revoke Association transaction

```python
from lto.transactions import RevokeAssociation

transaction = RevokeAssociation(recipient, association_type, anchor)
```
