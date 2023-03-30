URI = 'ipfs://'
ZERO_ADDRESS = '0x'+'0'*40

def log_test(transaction, name, **kwargs):
    print(kwargs)
    assert(len(transaction.events) == 1)
    event = transaction.events[name]
    for key, value in kwargs.items():
        assert(event[key] == value)
