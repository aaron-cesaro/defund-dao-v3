from scripts.helpful_scripts import get_account, OPENSEA_FORMAT
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
    badge_awardee = "0x026FDF9658046Ce5bE38deE958D587E955b856ec"
    token_image = "https://ipfs.io/ipfs/QmTWNnR62R3we6LqSWK3uq1ED8HhVs7KE9XsWD4bvMv9hm?filename=venture.jpeg"
    tx = defund_pass_manager.addStandardMember(
        badge_awardee, token_image, {"from": account, "gas_price": "2 gwei"}
    )
    tx.wait(1)
    print(f"Token URI: {tx.info()}")
    print(f"Opensea URL: {OPENSEA_FORMAT.format(defund_pass.address, 1)}")
