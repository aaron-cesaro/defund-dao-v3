from brownie import DefundPass, DefundPassManager, network, config
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
            {"from": account, "gas_price": "2 gwei"},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_pass


def deploy_defund_pass_manager(address):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and (
        len(DefundPassManager) > 0 and len(DefundPass) > 0
    ):
        return DefundPassManager[-1]
    else:
        defund_pass = DefundPassManager.deploy(
            address,
            {"from": account, "gas_price": "2 gwei"},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_pass
