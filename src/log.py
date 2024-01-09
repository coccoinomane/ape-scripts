import ape

from src.constants import APP_NAME


def info(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.info(f"{prefix}{text}")


def warn(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.warning(f"{prefix}{text}")


def debug(text: str = "", prefix: str = f"[{APP_NAME}] ") -> None:
    ape.logging.logger.debug(f"{prefix}{text}")
