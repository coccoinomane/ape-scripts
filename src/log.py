import ape

from src.constants import APP_NAME


def info(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.info(f"{prefix}{text}")


def warn(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.warning(f"{prefix}{text}")


def debug(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.debug(f"{prefix}{text}")


def check_live() -> None:
    """Ask for confirmation to proceed on live chain."""
    if not ape.networks.network.name in ["local", "testnet"]:
        warn(f"You are on live chain {ape.networks.network.chain_id}. Continue? [y/N]:")
        if input().lower() != "y":
            exit(1)
    info(
        f"CONNECTED TO {ape.networks.network.name} CHAIN {ape.networks.network.chain_id}"
    )
