from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

decimals = 8
start_price = 200000000000
local_blockchain_env = ["development", "ganache-local"]
forked_local_env = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in local_blockchain_env
        or network.show_active() in forked_local_env
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks..")

    # First check if the mock contract is deployed so we dont deploy again
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            decimals, Web3.toWei(start_price, "ether"), {"from": get_account()}
        )
