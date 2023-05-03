# Ape scripts

A collection of useful blockchain scripts written using the Ape Framework

# Quick start

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Then add an account:

```bash
ape accounts import <account alias>
```

You might need to install ape plugins:

```bash
ape plugins install solidity arbitrum polygon etherscan avalanche bsc optimism
```

Then call command, for example deploy token on Arbitrum:

```bash
ape run token --account <account alias> --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc 
```

# To do

- Find contract creations