from brownie import (
    network,
    config,
    DefundPass,
    VentureLeague,
    DeFundToken,
    DeFundGovernance,
)
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def main():
    deploy_defund_pass(
        "https://ipfs.io/ipfs/QmTWNnR62R3we6LqSWK3uq1ED8HhVs7KE9XsWD4bvMv9hm?filename=venture.jpeg"
    )


def deploy_defund_pass(pass_image):
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(DefundPass) > 0
    ):
        return DefundPass[-1]
    else:
        print("Deploying DeFund Pass contract......")
        defund_pass = DefundPass.deploy(
            pass_image,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_pass


def deploy_venture_league(address, league_img):
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


def deploy_defund_governance(token_address, pass_address):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and len(
        DeFundGovernance
    ):
        return DeFundGovernance[-1]
    else:
        print("Deploying DeFund PGovernance contract......")
        defund_governance = DeFundGovernance.deploy(
            token_address,
            pass_address,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
    return defund_governance
