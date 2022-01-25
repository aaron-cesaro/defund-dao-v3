from brownie import accounts, network, config
import ipfshttpclient

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def upload_to_ipfs(filepath):
    with ipfshttpclient.connect() as client:
        hash = client.add(filepath)["Hash"]
    filename = filepath.split("/")[-1:][0]
    filename = str(filepath.split("/")[-1:][0]).lower()
    file_uri = "https://ipfs.io/ipfs/{}?filename={}".format(hash, filename)
    print(file_uri)
    return file_uri
