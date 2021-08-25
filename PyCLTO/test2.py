from time import sleep


def is_mac():
    sleep(5)
    return True


def get_op_sys():
    return 'Mac' if is_mac() else 'Windows'
