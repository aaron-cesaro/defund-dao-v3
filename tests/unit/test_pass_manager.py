from queue import Empty
import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_defund_pass, deploy_pass_manager


def test_add_simple_member(URI):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_pass_manager(defund_pass.address)
    badge_awardee = get_account(1)
    # Act
    tx_add_simple_member = defund_pass_manager.addSimpleMember(
        badge_awardee, URI, {"from": account}
    )
    tx_add_simple_member.wait(1)
    # Assert
    assert tx_add_simple_member.return_value == 1
