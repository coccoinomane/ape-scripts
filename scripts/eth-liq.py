from time import time

import ape

from src.account import load_account
from src.contract import fetch_contract
from src.log import check_live, info
from src.token import approve_token_if_needed, deploy_or_fetch_token


def main(
    router_address: str,
    account_file: str,
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
    token = deploy_or_fetch_token(token_address=token_address, sender=account)
    approve_token_if_needed(token, router.address, value_token, sender=account)

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
        ape.accounts[0],
        time() + 60,
        sender=account,
        value=value_eth,
    )
