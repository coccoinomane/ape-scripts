import ape
from ape.contracts import ContractInstance

from src.constants import APP_NAME
from src.log import info


def fetch_contract(address: str = None, label: str = "contract") -> ContractInstance:
    """Fetch contract from explorer."""
    if not address:
        address = input("Enter {label} address: ")
    info(f"FETCHING {label.upper()} {address} FROM EXPLORER")
    contract = ape.Contract(address)
    info(f"{label.upper()} {contract!r} LOADED")
    return contract
