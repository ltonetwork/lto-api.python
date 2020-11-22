# lto-api.python
Python client library for interacting with LTO Network


## Initiate library
pl = PyCLTO.PyCLTO()
pl.NODE = "https://testnet.ltonode.turtlenetwork.eu"
pl.setChain("testnet")

## Initiate addresses
addr1 = pl.Address(seed="seedhere")

addr2 = pl.Address(seed="seed2here")

## Mass transaction
transfers = [
{ 'recipient': addr1.address, 'amount': 1 },
{ 'recipient': addr2.address, 'amount': 1 },
]
addr1.massTransferLTO(transfers)

## Sponsor transaction
addr1.sponsor(addr2)

## Cancel sponsor transaction
addr1.cancelSponsor(addr2)

## Lease transaction
tx = addr1.lease(addr2,1)
print(tx)

## Lease cancel transaction
addr1.leaseCancel(tx['id'])
