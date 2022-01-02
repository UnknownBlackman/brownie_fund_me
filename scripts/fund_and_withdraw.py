## Script to fund and withdraw from our address
from brownie import FundMe
from scripts.important_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    print(f"The entrance fee is {entrance_fee}")

    print("Funding")
    # Any funding transaction would require the below entrance fee
    fund_me.fund({"from": account, "value": entrance_fee})
    print("Entrance fee funded!")


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()

    print("Withdrawing from account")
    fund_me.withdraw({"from": account})
    print("Withdraw complete")


def main():
    fund()
    withdraw()
