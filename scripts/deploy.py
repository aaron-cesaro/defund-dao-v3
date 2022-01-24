from brownie import DeFundPass, network, config
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_defund_pass():
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(DeFundPass) > 0
    ):
        return DeFundPass[-1]
    else:
        defund_pass = DeFundPass.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
        return defund_pass
