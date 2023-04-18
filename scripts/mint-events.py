from time import time
from typing import Any, Dict

from brownie import Contract, Token, accounts, network
from scripts.helper import fetch_contract, info


def main(
    contract_address: str,
    topic: str,
    from_block: int = 0,
) -> None:
    """Count 'Minted' events on the given NFT contract.

    Example:
        # Count Minted events on Trump Series 2 NFT collection
        brownie run minted-events main 0xBD2433197c2928993dcbd956E6Da0218825CEde6 0xb8859298dac57b2b76cf10b7ec1923055aeb45e7679cf4c43f6461a77c3273ea 41668347 --network polygon-main
    """
    contract = fetch_contract(contract_address, "minter")
    # complete...
