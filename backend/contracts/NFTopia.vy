# @version ^0.3.0

from vyper.interfaces import ERC721

implements: ERC721

# Interface for the contract called by safeTransferFrom()
interface ERC721Receiver:
    def onERC721Received(
        _operator: address,
        _from: address,
        _tokenId: uint256,
        _data: Bytes[1024]
    ) -> bytes4: view

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
id_to_url: HashMap[uint256, String[50]]
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
    assert _owner != ZERO_ADDRESS, "Zero address"
    
    return self.token_count[_owner]

@view
@external
def ownerOf(_tokenId: uint256) -> address:
    owner: address = self.owner_of_nft[_tokenId]
    
    assert owner != ZERO_ADDRESS, "No owner"
    
    return owner

@view
@external
def tokenURI(_tokenId: uint256) -> String[50]:
    assert self.owner_of_nft[_tokenId] != ZERO_ADDRESS, "No owner"

    return self.id_to_url[_tokenId]

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
    self._transfer(_from, _to, _tokenId, msg.sender)

@external
@payable
def safeTransferFrom(_from: address, _to: address, _tokenId: uint256, _data: Bytes[1024]):
    self._transfer(_from, _to, _tokenId, msg.sender)
    
    if _to.is_contract:
        return_value: bytes4 = ERC721Receiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data)
        assert return_value == method_id("onERC721Received(address,address,uint256,bytes)", output_type=bytes4)

@external
@payable
def approve(_approved: address, _tokenId: uint256):
    pass

@external
def setApprovalForAll(_operator: address, _approved: bool):
    pass

@external
def mint(_url: String[50]) -> bool:
    to: address = msg.sender
    token_id: uint256 = self.number_of_tokens
    
    self.owner_of_nft[token_id] = to
    self.id_to_url[token_id] = _url
    self.token_count[to] += 1
    self.number_of_tokens += 1
    
    log Transfer(ZERO_ADDRESS, to, token_id)

    return True

@internal
def _transfer(_from: address, _to: address, _token_id: uint256, _sender: address):
    assert _from == _sender
    assert self.owner_of_nft[_token_id] == _sender

    self.owner_of_nft[_token_id] = _to
    self.token_count[_from] -= 1
    self.token_count[_to] += 1

    log Transfer(_from, _to, _token_id)