from time import time
from typing import Any, Dict

from brownie import Contract, Token, accounts, network
from scripts.helper import (
    approve_token_if_needed,
    build_tx_params,
    check_live,
    deploy_or_fetch_token,
    fetch_contract,
    info,
    load_account,
)


def main(
    router_address: str,
    account_file: str,
    tx_type: int = 0,  # TODO: not working?
    token_address: str = None,
    ask_before_liq: bool = True,
    value_eth: int = 10**13,
    value_token: int = 10**18,
) -> None:
    """Deploy a test token and and add liquidity for it on a
    Uniswap-like router.

    Example:
        # Add liquidity on Arbitrum Sushiswap with wallet 'my-account'
        brownie run eth-liq main 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506 my-account --network arbitrum-main
    """
    check_live()
    router = fetch_contract(router_address, "router")
    account = load_account(account_file)
    tx_params = build_tx_params(account, tx_type)
    token = deploy_or_fetch_token(token_address=token_address, tx_params=tx_params)
    approve_token_if_needed(token, router, value_token, tx_params)

    if ask_before_liq:
        info(f"ADD LIQUIDITY? [Y/n]:")
        if input().lower() == "n":
            return

    info(f"ADDING LIQUIDITY")
    router.addLiquidityETH(
        token,
        value_token,
        0,
        0,
        accounts[0],
        time() + 60,
        tx_params | {"value": value_eth},
    )
