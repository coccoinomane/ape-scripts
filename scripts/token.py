import click
from ape.cli import NetworkBoundCommand, network_option

from src.account import load_account
from src.log import check_live
from src.token import deploy_or_fetch_token


@click.command(cls=NetworkBoundCommand)
@click.option("--account")
@click.option("--token")
@network_option()
def cli(network: str, account: str, token: str) -> None:
    """Deploy a test token

    Example:
        ape run token --account <account alias> --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc
    """
    check_live()
    deploy_or_fetch_token(token_address=token, sender=load_account(account))
