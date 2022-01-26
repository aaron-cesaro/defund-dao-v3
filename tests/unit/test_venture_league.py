from eth_typing import Address
from eth_utils import address
import pytest
from brownie import network, exceptions, accounts
from scripts.helpful_scripts import (
    get_account,
    upload_to_ipfs,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import (
    deploy_defund_pass,
    deploy_defund_pass_manager,
    deploy_venture_league,
)


def test_get_role_not_exists(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    # Act
    invalid_role = venture_league.getRole(accounts[0])
    # Assert
    assert invalid_role == ""


def test_get_role_invalid_address(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.getRole("0x0000000000000000000000000000000000000000")


def test_member_not_exists(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    # Act
    member_exists = venture_league.memberExists(accounts[0])
    # Assert
    assert member_exists == False
