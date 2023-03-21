# @version ^0.3.0

owner: address

@external
def __init__():
    assert msg.sender != ZERO_ADDRESS
    self.owner = msg.sender

@view
@external
def isOwner() -> bool:
    assert msg.sender != ZERO_ADDRESS
    return self.owner == msg.sender
