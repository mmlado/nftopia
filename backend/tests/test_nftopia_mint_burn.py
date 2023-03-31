import brownie
import pytest

from helper import (
    log_test,
    URI,
    ZERO_ADDRESS
)


@pytest.fixture
def nftopia_contract(NFTopia, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield NFTopia.deploy({'from': accounts[0]})


def test_mint(nftopia_contract, accounts):
    assert (nftopia_contract.balanceOf(accounts[0]) == 0)

    transaction = nftopia_contract.mint(URI)

    log_test(transaction, 'Transfer', _from=ZERO_ADDRESS, _to=accounts[0], _tokenId=0)

    assert (nftopia_contract.tokenURI(0) == URI)
    assert (nftopia_contract.balanceOf(accounts[0]) == 1)
    assert (nftopia_contract.ownerOf(0) == accounts[0])


def test_burn(nftopia_contract, accounts):
    nftopia_contract.mint(URI)

    transaction = nftopia_contract.burn(0)

    log_test(transaction, 'Transfer', _from=accounts[0], _to=ZERO_ADDRESS, _tokenId=0)

    assert (nftopia_contract.balanceOf(accounts[0]) == 0)

    with brownie.reverts('Invalid token'):
        nftopia_contract.tokenURI(0)


def test_burn_not_owner(nftopia_contract, accounts):
    nftopia_contract.mint(URI, {'from': accounts[0]})

    with brownie.reverts('Forbidden'):
        nftopia_contract.burn(0, {'from': accounts[1]})
