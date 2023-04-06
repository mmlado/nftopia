import brownie
import pytest


from helper import (
    log_test,
    URI,
    ZERO_ADDRESS
)


PRICE = 10 ** 18

@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    yield NFTopia.deploy('', '', PRICE, {'from': accounts[0]})


def test_price(nftopia_contract, accounts):
    assert nftopia_contract.price() == PRICE


def test_set_price(nftopia_contract, accounts):
    nftopia_contract.setPrice(PRICE - 1)
    assert nftopia_contract.price() == PRICE - 1


def test_withdraw(nftopia_contract, accounts):
    alice = accounts[0]

    balance = alice.balance()
    nftopia_contract.mint(URI, {'from': alice, 'value': PRICE})
    assert alice.balance() == balance - PRICE

    nftopia_contract.withdraw()
    assert alice.balance() == balance


def test_withdraw_no_fuds(nftopia_contract, accounts):
    alice = accounts[0]

    with brownie.reverts('No balance'):
        nftopia_contract.withdraw()


def test_mint(nftopia_contract, accounts):
    alice = accounts[0]
    assert (nftopia_contract.balanceOf(alice) == 0)

    transaction = nftopia_contract.mint(URI, {'from': alice, 'value': PRICE})

    log_test(transaction, 'Transfer', _from=ZERO_ADDRESS, _to=accounts[0], _tokenId=0)

    assert (nftopia_contract.tokenURI(0) == URI)
    assert (nftopia_contract.balanceOf(alice) == 1)
    assert (nftopia_contract.ownerOf(0) == alice)


def test_no_value(nftopia_contract, accounts):
    alice = accounts[0]

    with brownie.reverts('Not enough value'):
        nftopia_contract.mint(URI, {'from': alice})


def test_insuficient_value(nftopia_contract, accounts):
    alice = accounts[0]

    with brownie.reverts('Not enough value'):
        nftopia_contract.mint(URI, {'from': alice, 'value': PRICE - 1})


def test_burn(nftopia_contract, accounts):
    nftopia_contract.mint(URI, {'value': PRICE})
    transaction = nftopia_contract.burn(0)

    log_test(transaction, 'Transfer', _from=accounts[0], _to=ZERO_ADDRESS, _tokenId=0)

    assert (nftopia_contract.balanceOf(accounts[0]) == 0)
    with brownie.reverts('Invalid token'):
        nftopia_contract.tokenURI(0)


def test_burn_approve(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    
    nftopia_contract.mint(URI, {'from': alice, 'value' : PRICE})
    nftopia_contract.approve(bob, 0, {'from': alice})
    transaction = nftopia_contract.burn(0, {'from': bob})

    log_test(transaction, 'Transfer', _from=alice, _to=ZERO_ADDRESS, _tokenId=0)

    assert nftopia_contract.balanceOf(alice) == 0

def test_burn_approval_for_all(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
 
    nftopia_contract.mint(URI, {'from': alice, 'value' : PRICE})
    nftopia_contract.setApprovalForAll(bob, True, {'from': alice})
    transaction = nftopia_contract.burn(0, {'from': bob})

    log_test(transaction, 'Transfer', _from=accounts[0], _to=ZERO_ADDRESS, _tokenId=0)

    assert nftopia_contract.balanceOf(alice) == 0


def test_burn_approval_for_all_forbidden(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]
    charlie = accounts[2]
    
    nftopia_contract.mint(URI, {'from': alice, 'value' : PRICE})
    nftopia_contract.setApprovalForAll(bob, True, {'from': charlie})

    with brownie.reverts('Forbidden'):
        nftopia_contract.burn(0, {'from': bob})


def test_burn_not_owner(nftopia_contract, accounts):
    alice = accounts[0]
    bob = accounts[1]

    nftopia_contract.mint(URI, {'from': alice, 'value' : PRICE})

    with brownie.reverts('Forbidden'):
        nftopia_contract.burn(0, {'from': bob})
