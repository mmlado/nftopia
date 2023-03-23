import pytest

ERC721_INTERFACE = 0x80ac58cd

@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield NFTopia.deploy({'from': accounts[0]})

def test_erc721_interface(nftopia_contract, accounts):
    assert nftopia_contract.supportsInterface(ERC721_INTERFACE)

def test_mint(nftopia_contract, accounts):
    assert nftopia_contract.mint("ipfs://")
    assert nftopia_contract.balanceOf(accounts[0]) == 1
    assert nftopia_contract.ownerOf(0) == accounts[0]
