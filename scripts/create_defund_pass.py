from scripts.helpful_scripts import get_account, upload_to_ipfs, OPENSEA_FORMAT
from scripts.deploy import deploy_defund_pass, deploy_defund_pass_manager


def main():
    add_standard_member()


def add_standard_member():
    account = get_account()
    defund_pass = deploy_defund_pass()
    defund_pass_manager = deploy_defund_pass_manager(defund_pass.address)
    if defund_pass.owner() != defund_pass_manager.address:
        tx_ownership = defund_pass.transferOwnership(
            defund_pass_manager.address, {"from": account, "gas_price": "2 gwei"}
        )
        tx_ownership.wait(1)
    badge_awardee = "0xBB293e429F420757aF10c8B12456B70E61ae3CfC"
    token_image = upload_to_ipfs("./img/{}.jpeg".format("venture"))
    tx = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account, "gas_price": "2 gwei"}
    )
    token_id = defund_pass_manager.membersIds(badge_awardee)
    tx.wait(1)
    print(f"Token URI: {tx.info()}")
    print(f"Opensea URL: {OPENSEA_FORMAT.format(defund_pass.address, token_id)}")
