from time import time

import ape
import click
from ape.cli import NetworkBoundCommand, network_option

from src.account import load_account
from src.contract import fetch_contract
from src.log import check_live, info
from src.token import approve_token_if_needed, deploy_or_fetch_token


@click.command(cls=NetworkBoundCommand)
@click.argument("router")
@click.option("--account")
@click.option("--token")
@click.option("--ask/--no-ask", default=True, help="Ask before adding liquidity")
@click.option("--value-eth", default=10**13, help="ETH value to add in pair, in wei")
@click.option(
    "--value-token", default=10**18, help="Token value to add in pair, in wei"
)
@network_option()
def cli(
    network: str,
    account: str,
    token: str,
    router: str,
    ask: bool,
    value_eth: int,
    value_token: int,
) -> None:
    """Deploy a test token and and add liquidity for it on a
    Uniswap-like router.

    If you want to skip the deployment of the token, you can pass
    the address of an existing token with the --token option.

    Example:
        # Add liquidity on Arbitrum Sushiswap with wallet 'my-account'
        ape run eth-liq 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506 --account <account alias> --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc
    """
    check_live()
    router_obj = fetch_contract(router, "router")
    account_obj = load_account(account)
    token_contract = deploy_or_fetch_token(token_address=token, sender=account_obj)
    approve_token_if_needed(
        token_contract, router_obj.address, value_token, sender=account_obj
    )

    if ask:
        info(f"ADD LIQUIDITY? [Y/n]:")
        if input().lower() == "n":
            return

    info(f"ADDING LIQUIDITY")
    router_obj.addLiquidityETH(
        token,
        value_token,
        0,
        0,
        account_obj,
        int(time() + 60),
        sender=account_obj,
        value=value_eth,
    )
