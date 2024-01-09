from typing import Any

import ape
from ape.api.accounts import AccountAPI
from ape.contracts import ContractInstance

from src.log import info


def deploy_or_fetch_token(
    sender: AccountAPI,
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    initial_supply: int = 10**9,
    token_address: str = None,
    **tx_params: Any,
) -> ContractInstance:
    """Deploy given token, or fetch it if the token address is given.

    Supply is given in units of the token (not wei)."""
    if not token_address:
        info(f"DEPLOYING TEST TOKEN")
        token = ape.project.get_contract("TokenInitialHolder").deploy(
            name,
            symbol,
            decimals,
            initial_supply * 10**decimals,
            sender.address,
            publish=False,
            sender=sender,
            **tx_params,
        )
    else:
        info(f"FETCHING TOKEN {token_address} FROM EXPLORER")
        token = ape.Contract(token_address)
    if token_address:
        info(f"TOKEN NAME: {token.name()} ({token.symbol()})")
    else:
        info(f"TOKEN ADDRESS: {token.address}")
    return token


def approve_token_if_needed(
    token: ContractInstance,
    spender: str,
    amount: int,
    **tx_params: Any,
) -> None:
    """Approve token if needed."""
    if token.allowance(tx_params["sender"], spender) < amount:
        info(f"APPROVING ROUTER TO SPEND TOKENS")
        token.approve(spender, amount, **tx_params)
