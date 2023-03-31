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


def test_get_approved_invalid_token(nftopia_contract, accounts):
    with brownie.reverts('Invalid token'):
        nftopia_contract.getApproved(0)


def test_approve(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    nftopia_contract.mint(URI, {'from': alice})

    transaction = nftopia_contract.approve(bob, 0, {'from': alice})

    log_test(transaction, 'Approval', _owner=alice, _approved=bob, _tokenId=0)

    assert nftopia_contract.getApproved(0) == bob


def test_approve_invalid_token(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    with brownie.reverts('Invalid token'):
        nftopia_contract.approve(bob, 0, {'from': alice})


def test_approve_not_owner(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    charlie = accounts[2]

    nftopia_contract.mint(URI, {'from': alice})

    with brownie.reverts('Forbidden'):
        nftopia_contract.approve(charlie, 0, {'from': bob})


def test_approve_owner_approved(nftopia_contract, accounts):
    alice = accounts[0]

    nftopia_contract.mint(URI, {'from': alice})

    with brownie.reverts('Owner can\'t be approved'):
        nftopia_contract.approve(alice, 0, {'from': alice})
