from brownie import DefundPass, PassManager, network, config
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_defund_pass():
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(DefundPass) > 0
    ):
        return DefundPass[-1]
    else:
        defund_pass = DefundPass.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
        return defund_pass


def deploy_pass_manager(address):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and (
        len(PassManager) > 0 and len(DefundPass) > 0
    ):
        return PassManager[-1]
    else:
        defund_pass = PassManager.deploy(
            address,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
        return defund_pass
