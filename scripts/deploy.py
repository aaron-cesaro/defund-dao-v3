from brownie import (
    network,
    config,
    DefundPass,
    DefundPassManager,
    VentureLeague,
    DeFundToken,
    DeFundGovernance,
)
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_defund_pass():
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(DefundPass) > 0
    ):
        return DefundPass[-1]
    else:
        print("Deploying DeFund Pass contract......")
        defund_pass = DefundPass.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_pass


def deploy_defund_pass_manager(address):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and len(
        DefundPassManager
    ):
        return DefundPassManager[-1]
    else:
        print("Deploying DeFund Pass Manager contract......")
        defund_pass = DefundPassManager.deploy(
            address,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_pass


def deploy_venture_league(address, league_img, roles):
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(VentureLeague) > 0
    ):
        return VentureLeague[-1]
    else:
        print("Deploying Venture League contract......")
        venture_league = VentureLeague.deploy(
            address,
            league_img,
            roles,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return venture_league


def deploy_defund_token():
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(DeFundToken) > 0
    ):
        return DeFundToken[-1]
    else:
        print("Deploying DeFund Token contract......")
        defund_token = DeFundToken.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_token


def deploy_defund_governance(address):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and len(
        DeFundGovernance
    ):
        return DeFundGovernance[-1]
    else:
        print("Deploying DeFund PGovernance contract......")
        defund_governance = DeFundGovernance.deploy(
            address,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_governance
