import brownie


from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_defund_token, deploy_defund_governance


def main():
    interact_with_governor()


def interact_with_governor():
    account = get_account()
    defund_token = deploy_defund_token()
    defund_governor = deploy_defund_governance(defund_token.address)
