from queue import Empty
import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_league_badge


def test_contract_is_paused_after_minting(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    state_before_minting = league_badge.paused()
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    state_after_minting = league_badge.paused()
    # Assert
    assert state_after_minting == state_before_minting


def test_contract_is_paused_after_burning(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    state_before_minting = league_badge.paused()
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    state_after_minting = league_badge.paused()
    tx_burn = league_badge._burn(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    state_after_burning = league_badge.paused()
    # Assert
    assert state_after_minting == state_before_minting == state_after_burning


def test_badge_id_is_incremented_correctly():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee_1 = get_account(1)
    badge_awardee_2 = get_account(2)
    # Act
    tx_award_1 = league_badge.safeMint(badge_awardee_1, {"from": account})
    tx_award_1.wait(1)
    tx_award_2 = league_badge.safeMint(badge_awardee_2, {"from": account})
    tx_award_2.wait(1)
    # Assert
    assert tx_award_2.return_value == tx_award_1.return_value + 1


def test_badge_is_minted_successfully(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    assert league_badge.balanceOf(badge_awardee) > 0
    assert league_badge.ownerOf(tx_award.return_value) == badge_awardee


def test_badge_is_burned_successfully(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    tx_burn = league_badge._burn(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    # Assert
    assert league_badge.balanceOf(badge_awardee) == 0
    with pytest.raises(exceptions.VirtualMachineError):
        assert league_badge.ownerOf(tx_award.return_value)


def test_token_uri_is_not_empty(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    assert league_badge.tokenURI(tx_award.return_value) is not Empty


def test_token_uri_is_set_correctly(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    print(f"TokenURI: {league_badge.tokenURI(tx_award.return_value)}")
    assert league_badge.tokenURI(tx_award.return_value) == URI


def test_member_can_have_just_one_badge(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        league_badge.safeMint(badge_awardee, URI, {"from": account})


def test_badge_is_approved_by_transaction_sender_after_minting(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    assert league_badge.getApproved(tx_award.return_value) == account


def test_badge_get_approved_raises_exception_after_burned(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    tx_burn = league_badge._burn(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        league_badge.getApproved(tx_award.return_value)


def test_badge_cannot_be_transferred_by_owner(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    assert league_badge.ownerOf(tx_award.return_value) == badge_awardee
    with pytest.raises(exceptions.VirtualMachineError):
        league_badge.safeTransferFrom(
            account, account, tx_award.return_value, {"from": badge_awardee}
        )


def test_badge_cannot_be_burned_by_owner(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tx_transfer = league_badge._burn(tx_award.return_value, {"from": badge_awardee})
        tx_transfer.wait(1)


def test_badge_cannot_be_burned_twice(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_badge = deploy_league_badge()
    badge_awardee = get_account(1)
    # Act
    tx_award = league_badge.safeMint(badge_awardee, URI, {"from": account})
    tx_award.wait(1)
    tx_burn_1 = league_badge._burn(tx_award.return_value, {"from": account})
    tx_burn_1.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        league_badge._burn(tx_award.return_value, {"from": account})
