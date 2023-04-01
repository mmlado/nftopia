import brownie
import pytest

from helper import (
    log_test,
    URI
)


@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    # deploy the contract with the initial value as a constructor argument
    contract = NFTopia.deploy({'from': accounts[0]})

    contract.mint(URI, {'from': accounts[0]})
    
    yield contract


def test_transfer_from(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    
    _test_transfer_from(nftopia_contract.transferFrom, nftopia_contract, alice, alice, bob)


def test_transfer_from_forbidden(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    _test_transfer_from_forbidden(nftopia_contract.transferFrom, nftopia_contract, alice, bob, alice)


def test_transfer_from_not_owner(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    
    with brownie.reverts('Forbidden'):
        nftopia_contract.transferFrom(bob, alice, 0, {'from': bob})


def test_transfer_from_invalid_token(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    
    with brownie.reverts('Invalid token'):
        nftopia_contract.transferFrom(alice, bob, 1, {'from': alice})


def test_safe_transfer_from(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    _test_transfer_from(nftopia_contract.safeTransferFrom, nftopia_contract, alice, alice, bob, '')


def test_safe_transfer_from_forbidden(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    _test_transfer_from_forbidden(nftopia_contract.safeTransferFrom, nftopia_contract, alice, bob, alice, '')


def test_transfer_from_approved(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    charlie = accounts[2]

    nftopia_contract.approve(charlie, 0, {'from': alice})

    _test_transfer_from(nftopia_contract.transferFrom, nftopia_contract, charlie, alice, bob)


def test_transfer_from_approved_forbidden(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    charlie = accounts[2]

    nftopia_contract.approve(charlie, 0, {'from': alice})

    _test_transfer_from_forbidden(nftopia_contract.transferFrom, nftopia_contract, charlie, bob, alice)


def _test_transfer_from(function, nftopia_contract, sender, from_address, to_address, *args):
    from_balance = nftopia_contract.balanceOf(from_address)
    to_balance = nftopia_contract.balanceOf(to_address)

    transaction = function(from_address, to_address, 0, *args, {'from': sender})

    assert (nftopia_contract.balanceOf(from_address) == from_balance - 1)
    assert (nftopia_contract.balanceOf(to_address) == to_balance + 1)
    assert (nftopia_contract.ownerOf(0) == to_address)

    log_test(transaction, 'Transfer', _from=from_address, _to=to_address, _tokenId=0)


def _test_transfer_from_forbidden(function, nftopia_contract, sender, from_account, to_account, *args):
    with brownie.reverts('Forbidden'):
        function(from_account, to_account, 0, *args, {'from': sender})
