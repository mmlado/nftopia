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


def test_mint(nftopia_contract, accounts):
    assert(nftopia_contract.balanceOf(accounts[0]) == 0)

    transaction = nftopia_contract.mint(URI)

    assert(len(transaction.events) == 1)
    assert(transaction.events[0]['_from'] == ZERO_ADDRESS)
    assert(transaction.events[0]['_to'] == accounts[0])
    assert(transaction.events[0]['_tokenId'] == 0)

    assert(nftopia_contract.tokenURI(0)) == URI
    assert(nftopia_contract.balanceOf(accounts[0]) == 1)
    assert(nftopia_contract.ownerOf(0) == accounts[0])
