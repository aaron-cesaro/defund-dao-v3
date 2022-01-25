import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import (
    get_account,
    upload_to_ipfs,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import deploy_defund_pass, deploy_defund_pass_manager


def test_add_simple_member(IMAGE_PATH):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    # Act
    token_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account}
    )
    tx_add_standard_member.wait(1)

    # Assert
    assert defund_pass_manager.isMember(badge_awardee) is True
    assert badge_awardee == defund_pass_manager.ownerOf(
        tx_add_standard_member.return_value
    )


def test_cannot_add_simple_member_twice(IMAGE_PATH):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    # Act
    token_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account}
    )
    tx_add_standard_member.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass_manager.addStandardMember(
            badge_awardee, token_image, {"from": account}
        )


def test_add_league_member(IMAGE_PATH):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    token_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    league = "Venture"
    role = "Analyst"
    # Act
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account}
    )
    tx_add_standard_member.wait(1)
    tx_add_league_member = defund_pass_manager.addLeagueMember(
        badge_awardee, token_image, league, role, {"from": account}
    )
    tx_add_league_member.wait(1)
    # Assert
    assert defund_pass_manager.isMember(badge_awardee) is True
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass_manager.ownerOf(tx_add_standard_member.return_value)
    assert (
        defund_pass_manager.ownerOf(tx_add_league_member.return_value) == badge_awardee
    )
    assert (
        defund_pass_manager.membersIds(badge_awardee)
        == tx_add_league_member.return_value
    )


def test_add_league_member_when_not_already_member(IMAGE_PATH):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    token_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    league = "Venture"
    role = "Analyst"
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass_manager.addLeagueMember(
            badge_awardee, token_image, league, role, {"from": account}
        )


def test_token_uri(TOKEN_URI, IMAGE_PATH):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    # Act
    token_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account}
    )
    tx_add_standard_member.wait(1)
    token_uri = defund_pass.tokenURI(tx_add_standard_member.return_value)
    print(f"TokenURI: {token_uri}")
    # Assert
    assert token_uri == TOKEN_URI
