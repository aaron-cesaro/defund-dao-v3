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


def test_has_role(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    # Act
    role_exists, role_index = venture_league.hasRole(VENTURE_LEAGUE_ROLES[0])
    # Assert
    assert role_exists == True
    assert role_index == 0


def test_has_role_not_found(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    role = "RESEARCHER"
    # Act
    role_exists, role_index = venture_league.hasRole(role)
    # Assert
    assert role_exists == False
    assert role_index == -1


def test_has_role_empty_string(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    role = ""
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.hasRole(role)


def test_has_role_wrong_value(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    role = 2342
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.hasRole(role)


def test_add_valid_role(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
    new_role = "RESEARCHER"
    # Act
    tx_add_role = venture_league.addRole(new_role, {"from": account})
    tx_add_role.wait(1)
    role_exists, _ = venture_league.hasRole(new_role)
    # Assert
    assert role_exists == True


def test_add_role_invalid_format(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
    new_role = "s"
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.addRole(new_role)


def test_add_same_role_twice(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
    new_role = "ANALYST"
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        venture_league.addRole(new_role, {"from": account})


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


def test_member_exists_invalid_address(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
        venture_league.memberExists("0x0000000000000000000000000000000000000000")


def test_find_league_member_not_exists(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
    member_exists, _ = venture_league.findLeagueMember(accounts[0])
    # Assert
    assert member_exists == False


def test_find_league_member_invalid_address(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
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
        venture_league.findLeagueMember("0x0000000000000000000000000000000000000000")
