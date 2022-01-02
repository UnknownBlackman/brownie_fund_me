from brownie import FundMe, network, config, MockV3Aggregator
from scripts.important_scripts import get_account, deploy_mock, local_blockchain_env


def deploy_fund_me():
    account = get_account()

    ## To get the price feed if we're not on a development network like rinkeby.
    if network.show_active() not in local_blockchain_env:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks deployed!")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(fund_me.address)
    return fund_me

def main():
    deploy_fund_me()
