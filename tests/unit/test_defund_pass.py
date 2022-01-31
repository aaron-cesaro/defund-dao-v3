from queue import Empty
import pytest
from brownie import network, exceptions
from web3 import Web3
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_defund_pass


def test_contract_is_paused_after_minting(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    state_before_minting = defund_pass.paused()
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    state_after_minting = defund_pass.paused()
    # Assert
    assert state_after_minting == state_before_minting


def test_contract_is_paused_after_burning(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    state_before_minting = defund_pass.paused()
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    state_after_minting = defund_pass.paused()
    tx_burn = defund_pass.burnPass(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    state_after_burning = defund_pass.paused()
    # Assert
    assert state_after_minting == state_before_minting == state_after_burning


def test_badge_is_minted_successfully(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    assert defund_pass.balanceOf(pass_buyer) > 0
    assert defund_pass.ownerOf(tx_award.return_value) == pass_buyer


def test_badge_is_burned_successfully(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    tx_burn = defund_pass.burnPass(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    # Assert
    assert defund_pass.balanceOf(pass_buyer) == 0
    with pytest.raises(exceptions.VirtualMachineError):
        assert defund_pass.ownerOf(tx_award.return_value)


def test_token_uri_is_not_empty(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    assert defund_pass.tokenURI(tx_award.return_value) is not Empty


def test_token_uri_is_set_correctly(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    print(f"TokenURI: {defund_pass.tokenURI(tx_award.return_value)}")
    assert defund_pass.tokenURI(tx_award.return_value) != ""


def test_member_can_have_just_one_badge(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})


def test_badge_is_approved_by_transaction_sender_after_minting(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    assert defund_pass.getApproved(tx_award.return_value) == account


def test_badge_get_approved_raises_exception_after_burned(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    tx_burn = defund_pass.burnPass(tx_award.return_value, {"from": account})
    tx_burn.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass.getApproved(tx_award.return_value)


def test_badge_cannot_be_transferred_by_owner(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    assert defund_pass.ownerOf(tx_award.return_value) == pass_buyer
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass.safeTransferFrom(
            account, account, tx_award.return_value, {"from": pass_buyer}
        )


def test_badge_cannot_be_burned_by_other_others(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    invalid_burner = get_account(2)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass.burnPass(tx_award.return_value, {"from": invalid_burner})


def test_badge_cannot_be_burned_twice(STANDARD_PASS_IMAGE):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass(STANDARD_PASS_IMAGE)
    pass_buyer = get_account(1)
    # Act
    tx_award = defund_pass.buyPass(pass_buyer, {"from": account, "value": 1})
    tx_award.wait(1)
    tx_burn_1 = defund_pass.burnPass(tx_award.return_value, {"from": account})
    tx_burn_1.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        defund_pass.burnPass(tx_award.return_value, {"from": account})
