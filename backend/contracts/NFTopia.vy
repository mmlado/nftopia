# @version ^0.3.0


from vyper.interfaces import ERC165
from vyper.interfaces import ERC721


interface ERC721Metadata:
    def name() -> String[64]: view

    def symbol() -> String[32]: view

    def tokenURI(_tokenId: uint256) -> String[128]: view


interface Ownable:
    def owner() -> address: view
    
    def renounceOwnership(): nonpayable
    
    def transferOwnership(_newOwner: address): nonpayable


implements: ERC165
implements: ERC721
implements: ERC721Metadata
implements: Ownable


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


event OwnershipTransferred:
    _previousOwner: address
    _newOwner: address


event PriceChanged:
    _previousPrice: uint256
    _newPrice: uint256

ERC165_INTERFACE_ID: constant(bytes4) = 0x01ffc9a7
ERC721_INTERFACE_ID: constant(bytes4) = 0x80ac58cd
ERC721_METADATA_INTERFACE_ID: constant(bytes4) =0x5b5e139f


owner_of_nft: HashMap[uint256, address]
id_to_url: HashMap[uint256, String[64]]
token_count: HashMap[address, uint256]
number_of_tokens: uint256
approvals: HashMap[uint256, address]
operator: HashMap[address, HashMap[address, bool]]
price: public(uint256)
owner: public(address)

name: public(String[64])
symbol: public(String[32])


@external
def __init__(_name: String[64], _symbol: String[32], _price: uint256):
    self.name = _name
    self.symbol = _symbol
    self.price = _price
    self._transfer_ownership(msg.sender)


@view
@external
def supportsInterface(interface_id: bytes4) -> bool:
    return interface_id in [
        ERC165_INTERFACE_ID,
        ERC721_INTERFACE_ID,
        ERC721_METADATA_INTERFACE_ID
    ]


@view
@external
def balanceOf(_owner: address) -> uint256:
    assert _owner != empty(address), "Zero address"
    
    return self.token_count[_owner]


@view
@external
def ownerOf(_tokenId: uint256) -> address:
    owner: address = self.owner_of_nft[_tokenId]
    
    assert owner != empty(address), "Invalid token"
    
    return owner


@view
@external
def tokenURI(_tokenId: uint256) -> String[128]:
    assert self.owner_of_nft[_tokenId] != empty(address), "Invalid token"

    return self.id_to_url[_tokenId]


@view
@external
def getApproved(_tokenId: uint256) -> address:
    assert self.owner_of_nft[_tokenId] != empty(address), "Invalid token"

    return self.approvals[_tokenId]


@view
@external
def isApprovedForAll(_owner: address, _operator: address) -> bool:
    return self.operator[_owner][_operator]


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
    sender: address = msg.sender
    owner: address = self.owner_of_nft[_tokenId]
    
    assert owner != empty(address), "Invalid token"
    assert sender == owner or self.operator[owner][sender], "Forbidden"
    assert _approved != owner, "Owner can't be approved"
    
    self.approvals[_tokenId] = _approved

    log Approval(owner, _approved, _tokenId)


@external
def setApprovalForAll(_operator: address, _approved: bool):
    sender: address = msg.sender
    assert _operator != sender, "Owner"

    self.operator[sender][_operator] = _approved

    log ApprovalForAll(sender, _operator, _approved)


@external
def renounceOwnership():
    assert msg.sender == self.owner, "Forbidden"

    self._transfer_ownership(empty(address))
    

@external
def transferOwnership(_newOwner: address):
    assert _newOwner != empty(address), "Zero address" 
    assert msg.sender == self.owner, "Forbidden"
    assert _newOwner != self.owner, "Already Owner"
    
    self._transfer_ownership(_newOwner)


@external
@payable
def mint(_url: String[64]):
    assert msg.value == self.price, "Not enough value"
    to: address = msg.sender
    token_id: uint256 = self.number_of_tokens
    
    self.owner_of_nft[token_id] = to
    self.id_to_url[token_id] = _url
    self.token_count[to] += 1
    self.number_of_tokens += 1
    
    log Transfer(empty(address), to, token_id)


@external
def withdraw():
    current_balance: uint256 = self.balance
    assert current_balance > 0, "No balance"
    
    send(self.owner, current_balance)

@external
def setPrice(_price: uint256):
    assert msg.sender == self.owner, "Forbidden"
    
    old_price: uint256 = self.price

    self.price = _price

    log PriceChanged(old_price, _price)

@external
def burn(_token_id: uint256):
    owner: address = self.owner_of_nft[_token_id]
    assert owner != empty(address)

    sender: address = msg.sender
    assert sender in [self.owner_of_nft[_token_id], self.approvals[_token_id]] or self.operator[owner][sender], "Forbidden" 

    self.owner_of_nft[_token_id] = empty(address)
    self.token_count[owner] = unsafe_sub(self.token_count[owner], 1)

    self.approvals[_token_id] = empty(address)

    log Transfer(owner, empty(address), _token_id)


@internal
def _transfer(_from: address, _to: address, _token_id: uint256, _sender: address):
    owner: address = self.owner_of_nft[_token_id]
    assert owner != empty(address), "Invalid token"
    assert owner == _from, "Forbidden"

    assert _sender in [self.owner_of_nft[_token_id], self.approvals[_token_id]] or self.operator[owner][_sender], "Forbidden" 

    self.owner_of_nft[_token_id] = _to
    self.token_count[_from] = unsafe_sub(self.token_count[_from], 1)
    self.token_count[_to] = unsafe_add(self.token_count[_to], 1)

    self.approvals[_token_id] = empty(address)

    log Transfer(owner, _to, _token_id)


@internal
def _transfer_ownership(_new_owner: address):
    old_owner: address = self.owner

    self.owner = _new_owner   
    
    log OwnershipTransferred(old_owner, _new_owner)