import ape
from ape.api.accounts import AccountAPI

from src.log import info


def load_account(account_file: str = None) -> AccountAPI:
    """Load account from keyfile."""
    if not account_file:
        account_file = input("Enter account name: ")
    info(f"LOADING ACCOUNT {account_file} ON CHAIN {ape.networks.network.chain_id}")
    return ape.accounts.load(account_file)
