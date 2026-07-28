from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
TX_DIR = BASE_DIR / "data" / "raw" / "transactions"
RESULT_DIR = BASE_DIR / "results" / "tracking"
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def _load_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def _clean_address(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def _normalize_eth_value(value):
    """
    Etherscan normal/internal tx value is usually in Wei.
    Convert Wei to ETH.
    """
    try:
        return float(value) / 10**18
    except Exception:
        return 0.0


def _normalize_token_value(row):
    """
    ERC20 value needs tokenDecimal.
    """
    try:
        value = float(row.get("value", 0))
        decimals = int(row.get("tokenDecimal", 18))
        return value / (10 ** decimals)
    except Exception:
        return 0.0


def run_one_hop_tpp_tracking(
    address: str,
    beta: float = 0.01,
    omega: int = 1000
):
    """
    Simplified TPP-based tracking for one crawled heist address.

    beta  = dirty amount threshold
    omega = transaction count threshold for unknown service provider
    """

    address = address.strip().lower()

    normal_file = TX_DIR / f"{address}_normal.csv"
    internal_file = TX_DIR / f"{address}_internal.csv"
    erc20_file = TX_DIR / f"{address}_erc20.csv"

    normal_df = _load_csv_if_exists(normal_file)
    internal_df = _load_csv_if_exists(internal_file)
    erc20_df = _load_csv_if_exists(erc20_file)

    results = []
    candidate_layering_addresses = set()
    integration_addresses = set()

    # Process normal ETH transactions
    if not normal_df.empty and "from" in normal_df.columns and "to" in normal_df.columns:
        normal_df["from_clean"] = normal_df["from"].apply(_clean_address)
        normal_df["to_clean"] = normal_df["to"].apply(_clean_address)
        normal_df["amount_normalized"] = normal_df["value"].apply(_normalize_eth_value)

        outgoing_normal = normal_df[
            (normal_df["from_clean"] == address) &
            (normal_df["amount_normalized"] > beta)
        ]

        for _, row in outgoing_normal.iterrows():
            to_addr = row["to_clean"]
            if to_addr:
                candidate_layering_addresses.add(to_addr)
                results.append({
                    "source": address,
                    "target": to_addr,
                    "transaction_type": "normal_eth",
                    "amount": row["amount_normalized"],
                    "hash": row.get("hash", ""),
                    "timeStamp": row.get("timeStamp", ""),
                    "label": "candidate_layering"
                })

    # Process internal ETH transactions
    if not internal_df.empty and "from" in internal_df.columns and "to" in internal_df.columns:
        internal_df["from_clean"] = internal_df["from"].apply(_clean_address)
        internal_df["to_clean"] = internal_df["to"].apply(_clean_address)

        if "value" in internal_df.columns:
            internal_df["amount_normalized"] = internal_df["value"].apply(_normalize_eth_value)
        else:
            internal_df["amount_normalized"] = 0.0

        outgoing_internal = internal_df[
            (internal_df["from_clean"] == address) &
            (internal_df["amount_normalized"] > beta)
        ]

        for _, row in outgoing_internal.iterrows():
            to_addr = row["to_clean"]
            if to_addr:
                candidate_layering_addresses.add(to_addr)
                results.append({
                    "source": address,
                    "target": to_addr,
                    "transaction_type": "internal_eth",
                    "amount": row["amount_normalized"],
                    "hash": row.get("hash", ""),
                    "timeStamp": row.get("timeStamp", ""),
                    "label": "candidate_layering"
                })

    # Process ERC20 token transactions
    if not erc20_df.empty and "from" in erc20_df.columns and "to" in erc20_df.columns:
        erc20_df["from_clean"] = erc20_df["from"].apply(_clean_address)
        erc20_df["to_clean"] = erc20_df["to"].apply(_clean_address)
        erc20_df["amount_normalized"] = erc20_df.apply(_normalize_token_value, axis=1)

        outgoing_erc20 = erc20_df[
            (erc20_df["from_clean"] == address) &
            (erc20_df["amount_normalized"] > beta)
        ]

        for _, row in outgoing_erc20.iterrows():
            to_addr = row["to_clean"]
            if to_addr:
                candidate_layering_addresses.add(to_addr)
                results.append({
                    "source": address,
                    "target": to_addr,
                    "transaction_type": "erc20",
                    "amount": row["amount_normalized"],
                    "tokenSymbol": row.get("tokenSymbol", ""),
                    "contractAddress": row.get("contractAddress", ""),
                    "hash": row.get("hash", ""),
                    "timeStamp": row.get("timeStamp", ""),
                    "label": "candidate_layering"
                })

    # Simple unknown service-provider detection using transaction count
    all_targets = [r["target"] for r in results]
    target_counts = pd.Series(all_targets).value_counts().to_dict()

    for addr, count in target_counts.items():
        if count > omega:
            integration_addresses.add(addr)

    for r in results:
        if r["target"] in integration_addresses:
            r["label"] = "integration_unknown_service"

    result_df = pd.DataFrame(results)

    output_file = RESULT_DIR / f"{address}_one_hop_tpp_result.csv"
    result_df.to_csv(output_file, index=False)

    return {
        "address": address,
        "beta": beta,
        "omega": omega,
        "normal_transactions_loaded": int(len(normal_df)),
        "internal_transactions_loaded": int(len(internal_df)),
        "erc20_transactions_loaded": int(len(erc20_df)),
        "candidate_layering_count": len(candidate_layering_addresses),
        "integration_count": len(integration_addresses),
        "tracked_transaction_count": int(len(result_df)),
        "output_file": str(output_file),
        "candidate_layering_preview": list(candidate_layering_addresses)[:20],
        "integration_preview": list(integration_addresses)[:20],
    }