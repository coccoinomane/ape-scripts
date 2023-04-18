# /usr/bin/env python3

from web3 import Web3

# import telegram
# Set up Telegram bot
# tg = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
# chat_id = 'YOUR_TELEGRAM_CHAT_ID'

# Set up Web3 provider
w3 = Web3(
    Web3.HTTPProvider(
        "https://rpc.ankr.com/arbitrum/45753670464b5e52b7216fa762245dfb2c4b77c7a58ff3524b847fc46a84ab91"
    )
)

# Define the address to monitor
address_to_monitor = "0xa8cA50F1cD2Ad81aed4151c8D6C8B6E13C26a411"

# Get the current block number
current_block_number = w3.eth.blockNumber

# Continuously check for new blocks
while True:
    # Get the latest block number
    latest_block_number = w3.eth.blockNumber

    # Check if a new block has been mined
    if latest_block_number > current_block_number:
        # Update the current block number
        current_block_number = latest_block_number

        # Get the latest block
        latest_block = w3.eth.get_block(current_block_number)

        # Check if the address has deployed a new contract in the latest block
        print(latest_block)
        for tx_hash in latest_block["transactions"]:
            transaction = w3.eth.get_transaction(tx_hash)  # type: ignore
            print(transaction)
            if transaction["to"] == None and transaction["from"] == address_to_monitor:
                message = f"The address {address_to_monitor} has deployed a new contract in block {current_block_number}."
                print(message)
                # tg.send_message(chat_id=chat_id, text=message)
