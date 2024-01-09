# Ape scripts

A collection of useful blockchain scripts written using the Ape Framework

# Install

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
ape plugins install solidity ape-foundry arbitrum polygon etherscan avalanche bsc optimism
```

# Commands

Then call command, for example deploy token on Arbitrum:

```bash
ape run token --account <account alias> --network arbitrum:mainnet:https://arb1.arbitrum.io/rpc 
```

The token command and other commands have arguments.  To see the arguments of a command use the `-h` flag:

```bash
ape run token -h
```


# Custom networks

To use a custom network, just specify it with the `--network` flag:

```bash
ape run token --account <account alias> --network https://rpc.zkfair.io
```

More details here:

- https://docs.apeworx.io/ape/stable/userguides/networks.html#custom-network-connection


# To do

- Find contract creations