from PyCLTO.LTONetworkCLI import HandleDefaultNew as handle
from PyCLTO.Transactions.Association import Association
from PyCLTO.Transactions.RevokeAssociation import RevokeAssociation

def func(args, associationType, recipient, hash):

    if not recipient or not hash or args[1] not in ['issue', 'revoke'] or not associationType:
        raise Exception('Incorrect association syntax')

    associationType = associationType[0]
    recipient = recipient[0]
    hash = hash[0]

    if args[1] == 'issue':
        transaction = Association(recipient=recipient, associationType=associationType, anchor=hash)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())
    else:
        # revoke case
        transaction = RevokeAssociation(recipient=recipient, associationType=associationType, anchor=hash)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())