import ape

from src.log import info, warn


def check_live() -> None:
    """Ask for confirmation to proceed on live chain."""
    if not ape.networks.network.name in ["local", "testnet"]:
        warn(f"You are on live chain {ape.networks.network.chain_id}. Continue? [y/N]:")
        if input().lower() != "y":
            exit(1)
    info(
        f"CONNECTED TO {ape.networks.network.name} CHAIN {ape.networks.network.chain_id}"
    )
