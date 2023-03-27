import brownie
import pytest

ERC721_INTERFACE = 0x80ac58cd
URI = "ipfs://"
ZERO_ADDRESS = "0x"+"0"*40

@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield NFTopia.deploy({'from': accounts[0]})


def test_erc721_interface(nftopia_contract, accounts):
    assert nftopia_contract.supportsInterface(ERC721_INTERFACE)

def test_balance_of(nftopia_contract, accounts):
    with brownie.reverts("Zero address"):
        nftopia_contract.balanceOf(ZERO_ADDRESS)

    assert(nftopia_contract.balanceOf(accounts[0]) == 0)

def test_token_uri(nftopia_contract, accounts):
    with brownie.reverts("No owner"):
        nftopia_contract.tokenURI(0)

def test_transfer_from(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    nftopia_contract.mint(URI, {'from': alice})

    transaction = nftopia_contract.transferFrom(alice, bob, 0)
    
    _test_transfer(transaction, alice, bob, 0)

def test_mint(nftopia_contract, accounts):
    assert(nftopia_contract.balanceOf(accounts[0]) == 0)

    transaction = nftopia_contract.mint(URI)

    _test_transfer(transaction, ZERO_ADDRESS, accounts[0], 0)

    assert(nftopia_contract.tokenURI(0) == URI)
    assert(nftopia_contract.balanceOf(accounts[0]) == 1)
    assert(nftopia_contract.ownerOf(0) == accounts[0])

def _test_transfer(transaction, from_address, to_address, token_id):
    assert(len(transaction.events) == 1)
    event = transaction.events['Transfer']
    assert(event['_from'] == from_address)
    assert(event['_to'] == to_address)
    assert(event['_tokenId'] == token_id)
