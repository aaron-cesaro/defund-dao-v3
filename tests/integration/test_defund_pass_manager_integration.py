import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import (
    get_account,
    upload_to_ipfs,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import deploy_defund_pass, deploy_defund_pass_manager


def test_token_uri_is_not_empty(IMAGE_PATH):
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
    assert token_uri != ""
