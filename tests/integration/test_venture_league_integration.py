from queue import Empty
import pytest
from brownie import network, exceptions
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


def test_add_venture_league_member(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    role = 0  # Analyst
    # Act
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, league_image, {"from": account}
    )
    tx_add_standard_member.wait(1)
    tx_add_venture_league_member = venture_league.addLeagueMember(badge_awardee, role)
    tx_add_venture_league_member.wait(1)
    # Assert
    assert defund_pass_manager.isMember(badge_awardee) is True
    assert badge_awardee == defund_pass_manager.ownerOf(
        tx_add_venture_league_member.return_value
    )
    assert venture_league.memberExists(badge_awardee)
    assert venture_league.getRole(badge_awardee) == VENTURE_LEAGUE_ROLES[role]


def test_remove_venture_league_member(IMAGE_PATH, VENTURE_LEAGUE_ROLES):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    league_image = upload_to_ipfs(IMAGE_PATH.format("venture"))
    venture_league = deploy_venture_league(
        defund_pass_manager.address, league_image, VENTURE_LEAGUE_ROLES
    )
    role = 0  # Analyst
    # Act
    tx_add_standard_member = defund_pass_manager.addStandardMember(
        badge_awardee, league_image, {"from": account}
    )
    tx_add_standard_member.wait(1)
    tx_add_venture_league_member = venture_league.addLeagueMember(badge_awardee, role)
    tx_add_venture_league_member.wait(1)
    tx_remove_venture_league_member = venture_league.removeLeagueMember(badge_awardee)
    tx_remove_venture_league_member.wait(1)
    # Assert
    assert defund_pass_manager.isMember(badge_awardee) is False
    assert not venture_league.memberExists(badge_awardee)
    assert venture_league.getRole(badge_awardee) == ""
    with pytest.raises(exceptions.VirtualMachineError):
        badge_awardee == defund_pass_manager.ownerOf(
            tx_add_venture_league_member.return_value
        )
