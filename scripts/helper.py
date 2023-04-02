from typing import Any, Dict

from brownie import Contract, Token, accounts, network
from brownie.utils import color
from eth_account import Account


def info(text: str, col: str = "cyan") -> None:
    print(f"{color(col)}{text}{color}")


def warn(text: str, col: str = "magenta") -> None:
    print(f"{color(col)}{text}{color}")


def check_live() -> None:
    """Ask for confirmation to proceed on live chain."""
    if not network.show_active() == "development":
        warn(
            f"WARNING: You are on live chain {network.show_active()}. Continue? [y/N]:"
        )
        if input().lower() != "y":
            exit(1)


def fetch_contract(address: str = None, label: str = "contract") -> Contract:
    """Fetch contract from explorer."""
    if not address:
        address = input("Enter {label} address: ")
    info(f"FETCHING {label.upper()} {address} FROM EXPLORER")
    contract = Contract.from_explorer(address)
    info(f"{label.upper()} {contract._name} LOADED")
    return contract


def load_account(account_file: str = None) -> Account:
    """Load account from keyfile."""
    if not account_file:
        account_file = input("Enter account name: ")
    info(f"LOADING ACCOUNT {account_file} ON NETWORK {network.show_active()}")
    return accounts.load(account_file)


def build_tx_params(account: Account, type: int) -> Dict[str, Any]:
    """Build transaction params for account and type"""
    tx_params: Dict[str, Any] = {"from": account}
    if type:
        tx_params["type"] = type
    return tx_params


def deploy_or_fetch_token(
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    initial_supply: int = 10**9 * 10**18,
    tx_params: Dict[str, Any] = None,
    token_address: str = None,
) -> Contract:
    """Deploy given token, or fetch it if the token address is given."""
    if not token_address:
        info(f"DEPLOYING TEST TOKEN")
        token = Token.deploy(name, symbol, decimals, initial_supply, tx_params)
    else:
        info(f"FETCHING TOKEN {token_address} FROM EXPLORER")
        token = Contract.from_explorer(token_address)
    info(f"TOKEN ADDRESS: {token.address}")
    return token


def approve_token_if_needed(
    token: Contract, spender: str, amount: int, tx_params: Dict[str, Any]
) -> None:
    """Approve token if needed."""
    if token.allowance(tx_params["from"], spender) < amount:
        info(f"APPROVING ROUTER TO SPEND TOKENS")
        token.approve(spender, amount, tx_params)
