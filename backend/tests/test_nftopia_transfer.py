import brownie
import pytest

from helper import (
    log_test,
    URI
)

@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield NFTopia.deploy({'from': accounts[0]})

def test_transfer_from(nftopia_contract, accounts):
    _test_transfer_from(nftopia_contract.transferFrom, nftopia_contract, accounts)

def test_transfer_from_not_owner(nftopia_contract, accounts):
    _test_transfer_from_not_owner(nftopia_contract.transferFrom, nftopia_contract, accounts)

def test_safe_transfer_from(nftopia_contract, accounts):
    _test_transfer_from(nftopia_contract.safeTransferFrom, nftopia_contract, accounts, '')

def test_safe_transfer_from_not_owner(nftopia_contract, accounts):
    _test_transfer_from_not_owner(nftopia_contract.safeTransferFrom, nftopia_contract, accounts, '')

def _test_transfer_from(function, nftopia_contract, accounts, *args): 
    alice = accounts[0]
    bob = accounts[1]
    nftopia_contract.mint(URI, {'from': alice})

    alice_balance = nftopia_contract.balanceOf(alice)
    bob_balance = nftopia_contract.balanceOf(bob)
    
    if args:
        transaction = function(alice, bob, 0, *args)
    else:
        transaction = function(alice, bob, 0)

    assert(nftopia_contract.balanceOf(alice) == alice_balance - 1)
    assert(nftopia_contract.balanceOf(bob) == bob_balance + 1)
    assert(nftopia_contract.ownerOf(0) == bob)
    
    log_test(transaction, 'Transfer', _from = alice, _to = bob, _tokenId = 0)

def _test_transfer_from_not_owner(function, nftopia_contract, accounts, *args):
    alice = accounts[0]
    bob = accounts[1]
    nftopia_contract.mint(URI, {'from': alice})

    with brownie.reverts('Forbidden'):
        if args:
            function(bob, alice, 0, *args, {'from': bob})
        else:
            function(bob, alice, 0, {'from': bob})