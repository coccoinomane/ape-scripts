import ape
from ape.api.accounts import AccountAPI

from src.log import info


def load_account(account_file: str = None) -> AccountAPI:
    """Load account from alias/keyfile.  To load a test
    account, use TEST::0, TEST::1, etc"""
    if not account_file:
        account_file = input("Enter account name: ")
    info(f"LOADING ACCOUNT {account_file} ON CHAIN {ape.networks.network.chain_id}")
    if account_file.startswith("TEST::"):
        return ape.accounts.test_accounts[int(account_file.split("::")[1])]
    return ape.accounts.load(account_file)
