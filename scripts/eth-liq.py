from time import time

from brownie import Contract, Token, accounts, network
from brownie.utils import color


def main(
    router_address: str,
    account: str,
    token_address: str = None,
    value_eth: int = 10**13,
    value_token: int = 10**18,
) -> None:
    """
    Deploy a test token and and add liquidity for it on a
    Uniswap-like router.

    Example:
        # Add liquidity on Arbitrum Sushiswap with wallet 'my-account'
        brownie run eth-liq main 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506 my-account --network arbitrum-main
    """
    # Check whether the user is going live
    if not network.show_active() == "development":
        warn(
            f"WARNING: You are on live chain {network.show_active()}. Continue? [y/N]:"
        )
        if input().lower() != "y":
            return

    info(f"FETCHING ROUTER {router_address} FROM EXPLORER")
    router = Contract.from_explorer(router_address)
    info(f"ROUTER {router._name} LOADED")
    info(f"LOADING ACCOUNT {account} ON NETWORK {network.show_active()}")
    accounts.load(account)
    if not token_address:
        info(f"DEPLOYING TEST TOKEN")
        token = Token.deploy("Test token", "TST", 18, 1e9 * 1e18, {"from": accounts[0]})
    else:
        info(f"FETCHING TOKEN {token_address} FROM EXPLORER")
        token = Contract.from_explorer(token_address)
    info(f"APPROVING ROUTER TO SPEND TOKENS")
    token.approve(router_address, value_token, {"from": accounts[0]})
    info(f"ADDING LIQUIDITY")
    router.addLiquidityETH(
        token,
        value_token,
        0,
        0,
        accounts[0],
        time() + 60,
        {"from": accounts[0], "value": value_eth},
    )


def info(text: str, col: str = "cyan") -> None:
    print(f"{color(col)}{text}{color}")


def warn(text: str, col: str = "magenta") -> None:
    print(f"{color(col)}{text}{color}")
