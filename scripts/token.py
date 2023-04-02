from scripts.helper import (
    build_tx_params,
    check_live,
    deploy_or_fetch_token,
    load_account,
)


def main(
    account_file: str,
    tx_type: int = 0,  # TODO: not working?
    token_address: str = None,
) -> None:
    """Deploy a test token"""
    check_live()
    account = load_account(account_file)
    tx_params = build_tx_params(account, tx_type)
    deploy_or_fetch_token(token_address=token_address, tx_params=tx_params)
