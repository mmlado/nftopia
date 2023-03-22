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
    pass

@view
@external
def ownerOf(_tokenId: uint256) -> address:
    pass

@view
@external
def getApproved(_tokenId: uint256) -> address:
    pass

@view
@external
def isApprovedForAll(_owner: address, _operator: address) -> bool:
    pass

@external
@payable
def transferFrom(_from: address, _to: address, _tokenId: uint256):
    pass

@external
@payable
def safeTransferFrom(_from: address, _to: address, _tokenId: uint256):
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
    return True