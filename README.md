# lto-api.python
Python client library for interacting with LTO Network


## Initiate library
```
pl = PyCLTO.PyCLTO()
pl.NODE = "https://testnet.ltonode.turtlenetwork.eu"
pl.setChain("testnet")
```

## Initiate addresses
```
addr1 = pl.Address(seed="seedhere")
addr2 = pl.Address(seed="seed2here")
addr3 = pl.Address(seed="scripted account seed here")
addrByPK = pl.Address(privateKey="3ezEY84xHWaXEKWPoLjK3UYwy9PZ1qPhqehVms6AdM4nirUWnnDgXHFm4xCyq9DpWd9HqAFfZwio8GogdQwwdLJi")
```

## Mass transaction
```
transfers = [
{ 'recipient': addr1.address, 'amount': 1 },
{ 'recipient': addr2.address, 'amount': 1 },
]
addr1.massTransferLTO(transfers)
```

## Sponsorship transaction
```
addr1.sponsorship(addr2)
```

## Cancel sponsorship transaction
```
addr1.cancelSponsorship(addr2)
```

## Lease transaction
```
tx = addr1.lease(addr2,1)
```

## Lease cancel transaction
```
addr1.leaseCancel(tx['id'])
```

## Set script transaction
```
script = 'match tx { \n' + \
'  case _ => true\n' + \
'}'
addr3.setScript(script)
```

## Create an anchor transaction
```
anchor = PyCLTO.crypto.bytes2str(PyCLTO.crypto.sha256(""))
print(addr1.anchor(anchor))
```

## Create and revoke an association
```
anchor = PyCLTO.crypto.bytes2str(PyCLTO.crypto.sha256(""))

print(addr1.invokeAssociation(addr2,2,anchor))
print(addr1.revokeAssociation(addr2,2,anchor))
```
