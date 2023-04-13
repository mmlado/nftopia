import brownie
import pytest

from helper import (
    log_test,
    ZERO_ADDRESS
)

NAME = 'Test'
SYMBOL = 'TEST'


@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    yield NFTopia.deploy(NAME, SYMBOL, 0, {'from': accounts[0]})


def test_owner(nftopia_contract, accounts):
    assert nftopia_contract.owner() == accounts[0]


def test_renounce_ownership(nftopia_contract, accounts):
    transaction = nftopia_contract.renounceOwnership()

    assert nftopia_contract.owner() == ZERO_ADDRESS

    log_test(transaction, 'OwnershipTransferred', _previousOwner=accounts[0], _newOwner=ZERO_ADDRESS)


def test_renounce_ownership_forbidden(nftopia_contract, accounts):
    with brownie.reverts('Forbidden'):
        nftopia_contract.renounceOwnership({'from': accounts[1]})


def test_transfer_ownership(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    transaction = nftopia_contract.transferOwnership(bob)

    assert nftopia_contract.owner() == bob

    log_test(transaction, 'OwnershipTransferred', _previousOwner=alice, _newOwner=bob)


def test_transfer_ownership_zero_address(nftopia_contract, accounts):
    with brownie.reverts('Zero address'):
        nftopia_contract.transferOwnership(ZERO_ADDRESS)


def test_transfer_ownership_forbidden(nftopia_contract, accounts):
    bob = accounts[1]
    charlie = accounts[2]

    with brownie.reverts('Forbidden'):
        nftopia_contract.transferOwnership(charlie, {'from': bob})


def test_transfer_ownership_already_owner(nftopia_contract, accounts):
    with brownie.reverts('Already Owner'):
        nftopia_contract.transferOwnership(accounts[0])
