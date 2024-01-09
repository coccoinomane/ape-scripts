import click
from ape.cli import network_option
from ape.cli.commands import ConnectedProviderCommand

from src.account import load_account
from src.network import check_live
from src.token import deploy_or_fetch_token


@click.command(cls=ConnectedProviderCommand)
@click.option(
    "--account",
    help="Alias of the deployer account.  To use a test account (e.g. on foundry), use TEST::0, TEST::1, etc",
)
@click.option("--name", default="Test Token")
@click.option("--symbol", default="TST")
@click.option(
    "--supply", type=int, default=10**9, help="Supply in units of the token (not wei)"
)
@click.option(
    "--token-address", help="If provided, return info about an existing token"
)
@click.option(
    "--legacy",
    is_flag=True,
    help="If provided, send legacy transactions (pre EIP-1559)",
)
@network_option()
def cli(
    network: str,
    account: str,
    name: str,
    symbol: str,
    supply: int,
    token_address: str,
    legacy: bool,
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
        type=0 if legacy else None,
    )
