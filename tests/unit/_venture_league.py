from eth_typing import Address
import pytest
from brownie import network, exceptions, accounts
from scripts.helpful_scripts import (
    get_account,
    upload_to_ipfs,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import (
    deploy_defund_pass,
    deploy_venture_league,
)


def test_member_not_exists(STANDARD_PASS_IMAGE, LEAGUE_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)

    venture_league = deploy_venture_league(defund_pass.address, LEAGUE_PASS_IMAGE)
    # Act
    member_exists = venture_league.memberExists(accounts[0])
    # Assert
    assert member_exists == False


def test_member_exists_invalid_address(STANDARD_PASS_IMAGE, LEAGUE_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)

    venture_league = deploy_venture_league(defund_pass.address, LEAGUE_PASS_IMAGE)
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.memberExists("0x0000000000000000000000000000000000000000")


def test_find_league_member_not_exists(STANDARD_PASS_IMAGE, LEAGUE_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)

    venture_league = deploy_venture_league(defund_pass.address, LEAGUE_PASS_IMAGE)
    # Act
    member_exists, _ = venture_league.findLeagueMember(accounts[0])
    # Assert
    assert member_exists == False


def test_find_league_member_invalid_address(STANDARD_PASS_IMAGE, LEAGUE_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)

    venture_league = deploy_venture_league(defund_pass.address, LEAGUE_PASS_IMAGE)
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.findLeagueMember("0x0000000000000000000000000000000000000000")
