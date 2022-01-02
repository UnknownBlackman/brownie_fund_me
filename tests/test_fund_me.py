from _pytest.config import exceptions
from scripts.important_scripts import get_account, local_blockchain_env
from scripts.deploy import deploy_fund_me
from brownie import accounts, network, FundMe, config
import pytest

# The withdraw test seems to work.
# Note: The funding tests seems to work now. The owner test still is not working.


def test_fund_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    # To check that the right account was funded
    assert fund_me.addressToAmt(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmt(account.address) == 0


def test_owner_can_withdraw():

    if network.show_active() not in local_blockchain_env:
        pytest.skip("Test is not on local network!")

    fund_me = deploy_fund_me()
    not_owner = accounts.add()

    # We want to raise an exception if an account thats not the owner tries to withdraw
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": not_owner})


def test_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    tx4 = fund_me.withdraw({"from": account})
    tx4.wait(1)
    assert fund_me.addressToAmt(account.address) == 0
