from typing import Any, List, cast

import ape
import click
from ape.cli import NetworkBoundCommand, network_option
from web3 import Web3
from web3.types import TxData

from src.log import debug, info


@click.command(cls=NetworkBoundCommand)
@click.option("--from-address")
@click.option("--to-address")
@click.option("--start-block", "--from-block")
@click.option("--end-block", "--to-block")
@click.option("--n-blocks", default=10, help="Number of blocks to scan")
@network_option()
def cli(
    network: str,
    from_address: str,
    to_address: str,
    start_block: Any,
    end_block: Any,
    n_blocks: int,
) -> None:
    """Scan the blockchain for transactions between two addresses.

    ADDRESSES
    - If you specify only --from-address, all transactions from that address will be scanned.
    - If you specify only --to-address, all transactions to that address will be scanned.
    - If you specify both --from-address and --to-address, all transactions between those two
      addresses will be scanned.

    BLOCKS
    - If you specify only --n-blocks, the latest n blocks will be scanned.
    - If you specify --start-block, the --n-blocks after that block will be scanned.
    - If you specify --end-block, the --n-blocks before that block will be scanned.
    - If you specify --start-block and --end-block, the blocks between those two blocks will be scanned.
    - Blocks can be specified by block number or block hash.

    EXAMPLE
    # Scan 10 blocks starting from block 120,000 on Arbitrum mainnet for txs between two addresses
    ape run scan-txs --from-address 0x57bF2482d7f75B201213AF47A6de5598f34d4Cd0 --to-address 0xB26F5f76afbFD070a18b6535EDd630b3E05726D5 --from-block 120000 --n-blocks 10 --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc

    """
    latest_block = ape.networks.active_provider.get_block("latest").number

    # Check that either from_address or to_address is specified
    if not from_address and not to_address:
        raise click.BadParameter("Must specify from_address and/or to_address")

    # n_blocks must be a positive integer
    if not isinstance(n_blocks, int) or n_blocks < 1:
        raise click.BadParameter("n_blocks must be a positive integer")

    # If start_block and end_block are not specified, we want to scan the latest n blocks
    if not start_block and not end_block:
        start_block = latest_block - n_blocks + 1
        end_block = latest_block
    # If only start_block is specified, we want to scan n blocks from start_block
    elif start_block and not end_block:
        start_block = ape.networks.active_provider.get_block(start_block).number
        end_block = start_block + n_blocks - 1
    # If only end_block is specified, we want to scan n blocks before end_block
    elif not start_block and end_block:
        end_block = ape.networks.active_provider.get_block(end_block).number
        start_block = end_block - n_blocks + 1
    # If both start_block and end_block are specified, we want to scan the blocks in that range
    elif start_block and end_block:
        start_block = ape.networks.active_provider.get_block(start_block).number
        end_block = ape.networks.active_provider.get_block(end_block).number
    else:
        raise click.BadParameter("Invalid combination of arguments")

    click.confirm(
        f"Scanning {end_block-start_block+1} blocks {start_block} to {end_block} for transactions from {from_address} to {to_address}. Continue?",
        default=True,
        abort=True,
    )

    w3 = cast(Web3, ape.networks.active_provider.web3)  # type: ignore

    txs = []

    for block_number in range(start_block, end_block + 1):
        block = w3.eth.get_block(block_number, full_transactions=True)
        block_txs = cast(List[TxData], block["transactions"])
        debug(
            f"Processing {len(block_txs)} transactions in block {block_number} [{block_number-start_block+1} of {end_block-start_block+1}]"
        )
        for tx in block_txs:
            if to_address:
                if tx["to"] and tx["to"].lower() == to_address.lower():
                    txs.append(tx)
                    if not from_address:
                        info(f"Found tx: {tx['hash'].hex()}")
                        continue

            if from_address:
                if tx["from"] and tx["from"].lower() == from_address.lower():
                    txs.append(tx)
                    if not to_address:
                        info(f"Found tx: {tx['hash'].hex()}")
                        continue

                if to_address:
                    if tx["to"] and tx["to"].lower() == to_address.lower():
                        txs.append(tx)
                        info(f"Found tx: {tx['hash'].hex()}")
                        continue

    if txs:
        info()
    info(f"SUMMARY")
    info(f"Found {len(txs)} transactions from {from_address} to {to_address}")
    for tx in txs:
        info(tx["hash"].hex())
