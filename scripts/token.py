import click
from ape.cli import NetworkBoundCommand, network_option

from src.account import load_account
from src.log import check_live
from src.token import deploy_or_fetch_token


@click.command(cls=NetworkBoundCommand)
@click.option(
    "--account",
    help="Alias of the deployer account.  To use a test account (e.g. on foundry), use TEST::0, TEST::1, etc",
)
@click.option("--name", default="Test Token")
@click.option("--symbol", default="TST")
@click.option("--supply", type=int, default=10**9 * 10**18)
@click.option("--token-address")
@network_option()
def cli(
    network: str, account: str, name: str, symbol: str, supply: int, token_address: str
) -> None:
    """Deploy a test token

    Example:
        ape run token --account <account alias> --name HarryPotterObamaSonic10Inu --symbol BITCOIN --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc
    """
    check_live()
    deploy_or_fetch_token(
        sender=load_account(account),
        name=name,
        symbol=symbol,
        initial_supply=supply,
        token_address=token_address,
    )
