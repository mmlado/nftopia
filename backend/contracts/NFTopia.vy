# @version ^0.3.0

from vyper.interfaces import ERC721

implements: ERC721

event Transfer:
    _from: address
    _to: address
    _tokenId: uint256

event Approval:
    _owner: address
    _approved: address
    _tokenId: uint256

event ApprovalForAll:
    _owner: address
    _operator: address
    _approved: bool

ERC721_INTERFACE_ID: constant(bytes4) = 0x80ac58cd

owner_of_nft: HashMap[uint256, address]
token_count: HashMap[address, uint256]
number_of_tokens: uint256

@external
def __init__():
    pass

@view
@external
def supportsInterface(interface_id: bytes4) -> bool:
    return interface_id in [
        ERC721_INTERFACE_ID
    ]

@view
@external
def balanceOf(_owner: address) -> uint256:
    assert _owner != ZERO_ADDRESS
    
    return self.token_count[_owner]

@view
@external
def ownerOf(_tokenId: uint256) -> address:
    owner: address = self.owner_of_nft[_tokenId]
    
    assert owner != ZERO_ADDRESS
    
    return owner

@view
@external
def getApproved(_tokenId: uint256) -> address:
    return ZERO_ADDRESS

@view
@external
def isApprovedForAll(_owner: address, _operator: address) -> bool:
    return True

@external
@payable
def transferFrom(_from: address, _to: address, _tokenId: uint256):
    pass

@external
@payable
def safeTransferFrom(_from: address, _to: address, _tokenId: uint256, _data: Bytes[1024]):
    pass

@external
@payable
def approve(_approved: address, _tokenId: uint256):
    pass

@external
def setApprovalForAll(_operator: address, _approved: bool):
    pass

@external
def mint(_url: String[200]) -> bool:
    self.owner_of_nft[self.number_of_tokens] = msg.sender
    self.token_count[msg.sender] += 1
    self.number_of_tokens += 1
    return True