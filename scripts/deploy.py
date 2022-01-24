from brownie import LeagueBadge, network, config
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_league_badge():
    account = get_account()
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        and len(LeagueBadge) > 0
    ):
        return LeagueBadge[-1]
    else:
        league_badge = LeagueBadge.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "publish_source", False
            ),
        )
        return league_badge
