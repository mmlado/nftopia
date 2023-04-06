import brownie
import pytest

from helper import (
    ZERO_ADDRESS
)

ERC721_INTERFACE = 0x80ac58cd
NAME = 'Test'
SYMBOL = 'TEST'


@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    yield NFTopia.deploy(NAME, SYMBOL, 0, {'from': accounts[0]})


def test_erc721_interface(nftopia_contract, accounts):
    assert nftopia_contract.supportsInterface(ERC721_INTERFACE)


def test_balance_of(nftopia_contract, accounts):
    with brownie.reverts('Zero address'):
        nftopia_contract.balanceOf(ZERO_ADDRESS)

    assert nftopia_contract.balanceOf(accounts[0]) == 0


def test_name(nftopia_contract, accounts):
    assert nftopia_contract.name() == NAME


def test_symbol(nftopia_contract, accounts):
    assert nftopia_contract.symbol() == SYMBOL


def test_token_uri_invalid_token(nftopia_contract, accounts):
    with brownie.reverts('Invalid token'):
        nftopia_contract.tokenURI(0)


def test_set_approval_for_all(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    
    assert not nftopia_contract.isApprovedForAll(alice, bob)
    nftopia_contract.setApprovalForAll(bob, True, {'from': alice})
    assert nftopia_contract.isApprovedForAll(alice, bob)

    nftopia_contract.setApprovalForAll(bob, False, {'from': alice})
    assert not nftopia_contract.isApprovedForAll(alice, bob)
