
import json

data = {
  "type": 9,
  "version": 1,
  "recipient": "3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1",
  "id": "BLMA4vkfe2S5UFHnoPyTh8SJmpTA1deh5SnWk1bdfjhq",
  "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
  "senderPublicKey": "4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz",
  "timestamp": 1519862400,
  "fee": 500000000,
  "proofs": [
    "2AKUBja93hF8AC2ee21m9AtedomXZNQG5J3FZMU85avjKF9B8CL45RWyXkXEeYb13r1AhpSzRvcudye39xggtDHv"
  ]
}

from PyCLTO import PyCLTO as pyclto
ret = pyclto().fromData(data)
print(ret.type)