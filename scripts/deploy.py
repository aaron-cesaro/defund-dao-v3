from brownie import DefundPass, DefundPassManager, VentureLeague, network, config
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
