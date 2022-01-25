from queue import Empty
import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_defund_pass, deploy_defund_pass_manager


def test_add_simple_member():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    defund_pass.transferOwnership(defund_pass_manager.address, {"from": account})
    badge_awardee = get_account(1)
    # Act
    token_image = "https://ipfs.io/ipfs/QmTWNnR62R3we6LqSWK3uq1ED8HhVs7KE9XsWD4bvMv9hm?filename=venture.jpeg"
    tokenURI = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account}
    )
    print(f"TokenURI: {tokenURI.return_value}")
    # Assert
    assert tokenURI != ""
